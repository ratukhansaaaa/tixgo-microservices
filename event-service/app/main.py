import os
from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

import httpx
from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="TixGo Event Management Service", version="1.0.0")

IDENTITY_BASE_URL = os.getenv("IDENTITY_BASE_URL", "http://identity:8000")
ATTENDANCE_BASE_URL = os.getenv("ATTENDANCE_BASE_URL", "http://attendance:8000")


# =========================================================
# Models (Swagger/OpenAPI)
# =========================================================
class EventCreateRequest(BaseModel):
    title: str = Field(min_length=1)
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class EventUpdateRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class EventItem(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    location: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    created_by: str
    created_at: datetime


class CheckinViaEventRequest(BaseModel):
    ticket_id: str = Field(min_length=1)


class IdentityMeResponse(BaseModel):
    username: str
    role: str


class AttendanceRecord(BaseModel):
    event_id: str
    ticket_id: str
    checked_in_by: str
    checked_in_at: datetime


class AttendanceResponse(BaseModel):
    event_id: str
    total_checked_in: int
    records: List[AttendanceRecord]


class EventSummaryResponse(BaseModel):
    event: EventItem
    attendance: AttendanceResponse


# =========================================================
# In-memory event store
# =========================================================
EVENTS: Dict[str, dict] = {}


# =========================================================
# Auth helpers (NO ASSUMPTION: matches your Identity)
# Identity:
# - GET /auth/me -> {"username": "...", "role": "..."}
# - Token passed via Authorization: Bearer <token>
# =========================================================
def require_bearer_auth(authorization: Optional[str]) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Authorization harus format: Bearer <token>")
    return f"Bearer {parts[1].strip()}"


async def identity_me(bearer_auth: str) -> IdentityMeResponse:
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            r = await client.get(
                f"{IDENTITY_BASE_URL}/auth/me",
                headers={"Authorization": bearer_auth},
            )
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Identity service unreachable")

    if r.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid/expired token")

    data = r.json()
    return IdentityMeResponse(**data)


def require_admin(user: IdentityMeResponse) -> None:
    if (user.role or "").lower() != "admin":
        raise HTTPException(status_code=403, detail="Admin only")


# =========================================================
# Basic routes
# =========================================================
@app.get("/health")
def health():
    return {"status": "ok", "service": "event-service"}


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html>
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>TixGo Event Service</title>
        <style>
          body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; padding: 24px; }
          .card { max-width: 720px; padding: 18px; border: 1px solid #eee; border-radius: 12px; }
          a { display:inline-block; margin-right: 12px; }
          code { background:#f5f5f5; padding: 2px 6px; border-radius: 6px; }
        </style>
      </head>
      <body>
        <div class="card">
          <h1>TixGo Event Management Service</h1>
          <p>Provides event CRUD and integrates Identity & Attendance services.</p>
          <p>
            <a href="/docs">Swagger UI</a>
            <a href="/redoc">ReDoc</a>
            <a href="/health">Health</a>
          </p>
          <p>Authorization header: <code>Bearer &lt;token&gt;</code></p>
        </div>
      </body>
    </html>
    """


# =========================================================
# Event CRUD
# Policy:
# - committee/admin: list/get
# - admin only: create/update/delete
# =========================================================
@app.get("/events", response_model=List[EventItem])
async def list_events(authorization: Optional[str] = Header(default=None, alias="Authorization")):
    bearer = require_bearer_auth(authorization)
    _ = await identity_me(bearer)
    return list(EVENTS.values())


@app.get("/events/{event_id}", response_model=EventItem)
async def get_event(event_id: str, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    bearer = require_bearer_auth(authorization)
    _ = await identity_me(bearer)

    evt = EVENTS.get(event_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Event not found")
    return evt


@app.post("/events", response_model=EventItem)
async def create_event(payload: EventCreateRequest, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    bearer = require_bearer_auth(authorization)
    user = await identity_me(bearer)
    require_admin(user)

    event_id = str(uuid4())
    evt = {
        "id": event_id,
        "title": payload.title,
        "description": payload.description,
        "location": payload.location,
        "start_time": payload.start_time,
        "end_time": payload.end_time,
        "created_by": user.username,
        "created_at": datetime.now(timezone.utc),
    }
    EVENTS[event_id] = evt
    return evt


@app.put("/events/{event_id}", response_model=EventItem)
async def update_event(event_id: str, payload: EventUpdateRequest, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    bearer = require_bearer_auth(authorization)
    user = await identity_me(bearer)
    require_admin(user)

    evt = EVENTS.get(event_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Event not found")

    updates = payload.model_dump(exclude_unset=True)
    for k, v in updates.items():
        evt[k] = v

    EVENTS[event_id] = evt
    return evt


@app.delete("/events/{event_id}")
async def delete_event(event_id: str, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    bearer = require_bearer_auth(authorization)
    user = await identity_me(bearer)
    require_admin(user)

    if event_id not in EVENTS:
        raise HTTPException(status_code=404, detail="Event not found")

    del EVENTS[event_id]
    return {"status": "deleted", "event_id": event_id}


# =========================================================
# Integration with Attendance
# Attendance service:
# - POST /checkins {event_id, ticket_id} requires Authorization
# - GET /attendance/{event_id} requires Authorization
#
# Policy:
# - committee/admin: can check-in via event service
# - admin only: can view attendance/summary
# =========================================================
@app.post("/events/{event_id}/checkins")
async def checkin_via_event(event_id: str, payload: CheckinViaEventRequest, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    bearer = require_bearer_auth(authorization)
    _ = await identity_me(bearer)  # validate token via identity

    if event_id not in EVENTS:
        raise HTTPException(status_code=404, detail="Event not found")

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            r = await client.post(
                f"{ATTENDANCE_BASE_URL}/checkins",
                headers={"Authorization": bearer},
                json={"event_id": event_id, "ticket_id": payload.ticket_id},
            )
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Attendance service unreachable")

    # forward status code semantics
    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.json().get("detail", "Attendance error"))

    return r.json()


@app.get("/events/{event_id}/attendance", response_model=AttendanceResponse)
async def get_event_attendance(event_id: str, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    bearer = require_bearer_auth(authorization)
    user = await identity_me(bearer)
    require_admin(user)

    if event_id not in EVENTS:
        raise HTTPException(status_code=404, detail="Event not found")

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            r = await client.get(
                f"{ATTENDANCE_BASE_URL}/attendance/{event_id}",
                headers={"Authorization": bearer},
            )
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Attendance service unreachable")

    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.json().get("detail", "Attendance error"))

    return AttendanceResponse(**r.json())


@app.get("/events/{event_id}/summary", response_model=EventSummaryResponse)
async def get_event_summary(event_id: str, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    bearer = require_bearer_auth(authorization)
    user = await identity_me(bearer)
    require_admin(user)

    evt = EVENTS.get(event_id)
    if not evt:
        raise HTTPException(status_code=404, detail="Event not found")

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            r = await client.get(
                f"{ATTENDANCE_BASE_URL}/attendance/{event_id}",
                headers={"Authorization": bearer},
            )
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Attendance service unreachable")

    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.json().get("detail", "Attendance error"))

    attendance = AttendanceResponse(**r.json())
    return {"event": EventItem(**evt), "attendance": attendance}