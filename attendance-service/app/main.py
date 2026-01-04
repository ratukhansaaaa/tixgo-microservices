import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

import jwt
import httpx
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse, JSONResponse, Response
from pydantic import BaseModel, Field

app = FastAPI(
    title="TixGo Attendance Service",
    version="1.0.0"
)

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALG = os.getenv("JWT_ALG", "HS256")

# Internal Event Service URL (Docker network)
EVENT_BASE_URL = os.getenv("EVENT_BASE_URL", "http://event:8000")

# Demo in-memory checkin storage:
# CHECKINS[event_id][ticket_id] = {"checked_in_at": datetime, "checked_in_by": "..."}
CHECKINS: Dict[str, Dict[str, dict]] = {}


def get_bearer_token(authorization: Optional[str]) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Authorization harus format: Bearer <token>")
    return parts[1].strip()


def require_auth(authorization: Optional[str]) -> str:
    token = get_bearer_token(authorization)
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        return str(payload.get("sub"))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token invalid")


# ===== Request Models =====
class CheckinRequest(BaseModel):
    event_id: str = Field(min_length=1)
    ticket_id: str = Field(min_length=1)


# ===== Response Models (untuk Swagger/OpenAPI biar rapi) =====
class CheckinRecord(BaseModel):
    event_id: str
    ticket_id: str
    checked_in_by: str
    checked_in_at: datetime


class CheckinCreateResponse(BaseModel):
    status: str
    record: CheckinRecord


class AttendanceResponse(BaseModel):
    event_id: str
    total_checked_in: int
    records: List[CheckinRecord]


@app.get("/health")
def health():
    return {"status": "ok", "service": "attendance"}


@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <!DOCTYPE html>
    <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>TixGo Attendance Service</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                    background: linear-gradient(135deg, #0d1b3a 0%, #1a2954 100%);
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                    position: relative;
                }
                
                .container {
                    background: rgba(255, 255, 255, 0.15);
                    backdrop-filter: blur(10px);
                    border: 1px solid rgba(255, 255, 255, 0.3);
                    border-radius: 16px;
                    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
                    padding: 40px;
                    max-width: 560px;
                    width: 100%;
                }
                
                h1 {
                    color: #fff;
                    margin-bottom: 10px;
                    font-size: 32px;
                    font-weight: 600;
                }
                
                .subtitle {
                    color: rgba(255, 255, 255, 0.85);
                    margin-bottom: 20px;
                    font-size: 14px;
                }
                
                .links {
                    display: flex;
                    flex-direction: column;
                    gap: 12px;
                }
                
                a {
                    display: block;
                    padding: 12px 16px;
                    border-radius: 8px;
                    text-decoration: none;
                    font-weight: 500;
                    transition: all 0.3s ease;
                    text-align: center;
                }
                
                .btn-primary {
                    background: rgba(255, 255, 255, 0.25);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.4);
                }
                
                .btn-primary:hover {
                    background: rgba(255, 255, 255, 0.35);
                    transform: translateY(-2px);
                    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
                }
                
                .btn-secondary {
                    background: rgba(255, 255, 255, 0.2);
                    color: white;
                    border: 1px solid rgba(255, 255, 255, 0.3);
                }
                
                .btn-secondary:hover {
                    background: rgba(255, 255, 255, 0.3);
                    border-color: rgba(255, 255, 255, 0.5);
                    transform: translateY(-2px);
                }
                
                .info {
                    background: rgba(255, 255, 255, 0.1);
                    border-left: 3px solid rgba(255, 255, 255, 0.5);
                    padding: 12px;
                    border-radius: 6px;
                    margin-top: 18px;
                    font-size: 13px;
                    color: rgba(255, 255, 255, 0.85);
                    line-height: 1.4;
                }
                
                code {
                    background: rgba(255, 255, 255, 0.15);
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: 'Monaco', monospace;
                    color: #fff;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>TixGo Attendance Service</h1>
                <p class="subtitle">Check-in & Attendance + Public Gateway for Event APIs</p>
                <div class="links">
                    <a href="/docs" class="btn-primary">Swagger UI (Interactive)</a>
                    <a href="/redoc" class="btn-secondary">ReDoc</a>
                    <a href="/health" class="btn-secondary">Health Status</a>
                </div>
                <div class="info">
                    <strong>Note:</strong><br/>
                    - Attendance endpoints: <code>/checkins</code>, <code>/attendance/{event_id}</code><br/>
                    - Event endpoints are exposed via this service (proxy): <code>/events</code>, <code>/events/{id}/summary</code>, etc.<br/>
                    - All non-health endpoints require <code>Authorization: Bearer &lt;token&gt;</code> obtained from Identity Service.
                </div>
            </div>
        </body>
    </html>
    """


# =========================================================
# Native Attendance APIs
# =========================================================
@app.post("/checkins", response_model=CheckinCreateResponse)
def create_checkin(
    req: CheckinRequest,
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
):
    checked_in_by = require_auth(authorization)

    event = CHECKINS.setdefault(req.event_id, {})
    if req.ticket_id in event:
        raise HTTPException(status_code=409, detail="Ticket sudah pernah check-in")

    record = {
        "event_id": req.event_id,
        "ticket_id": req.ticket_id,
        "checked_in_by": checked_in_by,
        "checked_in_at": datetime.now(timezone.utc),
    }
    event[req.ticket_id] = record
    return {"status": "checked_in", "record": record}


@app.get("/attendance/{event_id}", response_model=AttendanceResponse)
def get_attendance(
    event_id: str,
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
):
    _ = require_auth(authorization)
    event = CHECKINS.get(event_id, {})
    records: List[dict] = list(event.values())
    return {
        "event_id": event_id,
        "total_checked_in": len(records),
        "records": records,
    }


# =========================================================
# Proxy / Gateway to Event Service
# (Public only via Attendance port 18082)
# =========================================================
async def _proxy_to_event(
    method: str,
    path: str,
    authorization: Optional[str],
    json_body: Optional[dict] = None,
):
    # Ensure token exists and format is Bearer <token>
    _ = get_bearer_token(authorization)
    headers = {"Authorization": authorization}

    url = f"{EVENT_BASE_URL}{path}"

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            r = await client.request(method, url, headers=headers, json=json_body)
        except httpx.RequestError:
            raise HTTPException(status_code=502, detail="Event service unreachable")

    # Forward JSON if possible
    content_type = r.headers.get("content-type", "")
    if "application/json" in content_type:
        try:
            return JSONResponse(status_code=r.status_code, content=r.json())
        except Exception:
            return Response(status_code=r.status_code, content=r.text, media_type=content_type)

    return Response(status_code=r.status_code, content=r.text, media_type=content_type or "text/plain")


@app.get("/events")
async def proxy_list_events(authorization: Optional[str] = Header(default=None, alias="Authorization")):
    return await _proxy_to_event("GET", "/events", authorization)


@app.get("/events/{event_id}")
async def proxy_get_event(event_id: str, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    return await _proxy_to_event("GET", f"/events/{event_id}", authorization)


@app.post("/events")
async def proxy_create_event(payload: dict, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    return await _proxy_to_event("POST", "/events", authorization, json_body=payload)


@app.put("/events/{event_id}")
async def proxy_update_event(event_id: str, payload: dict, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    return await _proxy_to_event("PUT", f"/events/{event_id}", authorization, json_body=payload)


@app.delete("/events/{event_id}")
async def proxy_delete_event(event_id: str, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    return await _proxy_to_event("DELETE", f"/events/{event_id}", authorization)


@app.post("/events/{event_id}/checkins")
async def proxy_checkin_via_event(event_id: str, payload: dict, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    return await _proxy_to_event("POST", f"/events/{event_id}/checkins", authorization, json_body=payload)


@app.get("/events/{event_id}/attendance")
async def proxy_get_event_attendance(event_id: str, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    return await _proxy_to_event("GET", f"/events/{event_id}/attendance", authorization)


@app.get("/events/{event_id}/summary")
async def proxy_get_event_summary(event_id: str, authorization: Optional[str] = Header(default=None, alias="Authorization")):
    return await _proxy_to_event("GET", f"/events/{event_id}/summary", authorization)