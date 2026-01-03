import os
from datetime import datetime, timezone
from typing import Dict, List, Optional

import jwt
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
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
                        background: linear-gradient(135deg, #87ceeb 0%, #4da6ff 100%);
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        padding: 20px;
                        overflow: hidden;
                        position: relative;
                    }
                    
                    .background-animation {
                        position: absolute;
                        top: 0;
                        left: 0;
                        width: 100%;
                        height: 100%;
                        overflow: hidden;
                        pointer-events: none;
                        z-index: 1;
                    }
                    
                    .ticket {
                        position: absolute;
                        font-size: 60px;
                        opacity: 0.1;
                        animation: float 15s infinite ease-in-out;
                    }
                    
                    .ticket:nth-child(1) { left: 5%; top: 10%; animation-delay: 0s; }
                    .ticket:nth-child(2) { left: 15%; top: 70%; animation-delay: 2s; }
                    .ticket:nth-child(3) { left: 80%; top: 20%; animation-delay: 4s; }
                    .ticket:nth-child(4) { left: 85%; top: 60%; animation-delay: 6s; }
                    .ticket:nth-child(5) { left: 40%; top: 5%; animation-delay: 8s; }
                    .ticket:nth-child(6) { left: 60%; top: 80%; animation-delay: 10s; }
                    
                    @keyframes float {
                        0%, 100% { transform: translateY(0px) rotate(0deg); }
                        50% { transform: translateY(-30px) rotate(5deg); }
                    }
                    
                    .container {
                        background: rgba(255, 255, 255, 0.15);
                        backdrop-filter: blur(10px);
                        border: 1px solid rgba(255, 255, 255, 0.3);
                        border-radius: 16px;
                        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.2);
                        padding: 40px;
                        max-width: 500px;
                        width: 100%;
                        position: relative;
                        z-index: 2;
                    }
                    
                    h1 {
                        color: #fff;
                        margin-bottom: 10px;
                        font-size: 32px;
                        font-weight: 600;
                    }
                    
                    .subtitle {
                        color: rgba(255, 255, 255, 0.85);
                        margin-bottom: 30px;
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
                        margin-top: 20px;
                        font-size: 13px;
                        color: rgba(255, 255, 255, 0.85);
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
                <div class="background-animation">
                    <div class="ticket">🎫</div>
                    <div class="ticket">🎫</div>
                    <div class="ticket">🎫</div>
                    <div class="ticket">🎫</div>
                    <div class="ticket">🎫</div>
                    <div class="ticket">🎫</div>
                </div>
                
                <div class="container">
                    <h1>TixGo Attendance Service</h1>
                    <p class="subtitle">Check-in & Attendance Management</p>
                    <div class="links">
                        <a href="/docs" class="btn-primary">Swagger UI (Interactive)</a>
                        <a href="/redoc" class="btn-secondary">ReDoc (Beautiful Docs)</a>
                        <a href="/health" class="btn-secondary">Health Status</a>
                    </div>
                    <div class="info">
                        <strong>Note:</strong> All endpoints require authentication. Get a JWT token from the identity service first.
                    </div>
                </div>
            </body>
        </html>
        """


@app.get("/redoc")
def redoc_page():
        return HTMLResponse(content="""
        <!doctype html>
        <html>
            <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>TixGo Attendance Service - ReDoc</title>
                <style>body{margin:0;padding:0;font-family:system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', Arial;}</style>
            </head>
            <body>
                <noscript>
                    <strong>ReDoc requires JavaScript to function. Please enable it to browse the documentation.</strong>
                </noscript>
                <redoc spec-url="/openapi.json"></redoc>
                <script>
                    (function(){
                        var script = document.createElement('script');
                        script.src = 'https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js';
                        script.onload = function(){ /* loaded */ };
                        script.onerror = function(){
                            document.body.innerHTML = '<div style="padding:24px;font-family:inherit"><h1>Documentation (ReDoc)</h1><p>Failed to load ReDoc from CDN. You can use the interactive Swagger UI instead:</p><p><a href="/docs">Open Swagger UI</a></p><pre style="background:#f5f5f5;padding:12px;border-radius:6px">OpenAPI spec available at /openapi.json</pre></div>';
                        };
                        document.body.appendChild(script);
                    })();
                </script>
            </body>
        </html>
        """, media_type="text/html")


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