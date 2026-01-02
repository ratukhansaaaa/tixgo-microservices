import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

import jwt
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field

app = FastAPI(title="TixGo Attendance Service", version="1.0.0")

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALG = os.getenv("JWT_ALG", "HS256")


# Demo in-memory checkin storage:
# CHECKINS[event_id][ticket_id] = {"checked_in_at": "...", "checked_in_by": "..."}
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


class CheckinRequest(BaseModel):
    event_id: str = Field(min_length=1)
    ticket_id: str = Field(min_length=1)


@app.get("/health")
def health():
    return {"status": "ok", "service": "attendance"}


@app.post("/checkins")
def create_checkin(req: CheckinRequest, authorization: Optional[str] = Header(default=None)):
    checked_in_by = require_auth(authorization)

    event = CHECKINS.setdefault(req.event_id, {})
    if req.ticket_id in event:
        raise HTTPException(status_code=409, detail="Ticket sudah pernah check-in")

    record = {
        "event_id": req.event_id,
        "ticket_id": req.ticket_id,
        "checked_in_by": checked_in_by,
        "checked_in_at": datetime.now(timezone.utc).isoformat(),
    }
    event[req.ticket_id] = record
    return {"status": "checked_in", "record": record}


@app.get("/attendance/{event_id}")
def get_attendance(event_id: str, authorization: Optional[str] = Header(default=None)):
    _ = require_auth(authorization)  # cukup validasi token
    event = CHECKINS.get(event_id, {})
    records: List[dict] = list(event.values())
    return {
        "event_id": event_id,
        "total_checked_in": len(records),
        "records": records,
    }