import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

import jwt
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel, Field
from passlib.hash import bcrypt

app = FastAPI(title="TixGo Identity Service", version="1.0.0")

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "120"))


# ----------------------------
# Helpers
# ----------------------------
def _password_bytes_len(pw: str) -> int:
    return len(pw.encode("utf-8"))


def _validate_password_length(pw: str) -> None:
    # bcrypt limit is 72 bytes
    if _password_bytes_len(pw) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password terlalu panjang (maks 72 bytes). Gunakan password lebih pendek."
        )


def create_access_token(username: str, role: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=TOKEN_EXPIRE_MINUTES)).timestamp()),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


def get_bearer_token(authorization: Optional[str]) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    parts = authorization.split(" ", 1)
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header format. Use: Bearer <token>")
    return parts[1].strip()


# ----------------------------
# In-memory user store
# ----------------------------
# Format: USERS[username] = {"password_hash": "...", "role": "..."}
USERS: Dict[str, Dict[str, str]] = {
    "panitia1": {"password_hash": bcrypt.hash("secret"), "role": "committee"},
    "admin1": {"password_hash": bcrypt.hash("secret"), "role": "admin"},
}


# ----------------------------
# Schemas
# ----------------------------
class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=4, max_length=200)  # bytes-length check handled manually
    role: str = Field("committee", description="committee/admin")


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class MeResponse(BaseModel):
    username: str
    role: str


# ----------------------------
# Routes
# ----------------------------
@app.get("/health")
def health():
    return {"status": "ok", "service": "identity-service"}


@app.get("/", response_class=HTMLResponse)
def root():
        # Modern HTML landing page with styling
        return """
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>TixGo Identity Service</title>
                <style>
                    * { margin: 0; padding: 0; box-sizing: border-box; }
                    body {
                        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        padding: 20px;
                    }
                    .container {
                        background: white;
                        border-radius: 12px;
                        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                        padding: 40px;
                        max-width: 500px;
                        width: 100%;
                    }
                    h1 {
                        color: #333;
                        margin-bottom: 10px;
                        font-size: 32px;
                    }
                    .subtitle {
                        color: #666;
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
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                    }
                    .btn-primary:hover {
                        transform: translateY(-2px);
                        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
                    }
                    .btn-secondary {
                        background: #f0f0f0;
                        color: #333;
                        border: 2px solid #e0e0e0;
                    }
                    .btn-secondary:hover {
                        background: #e8e8e8;
                        border-color: #667eea;
                        color: #667eea;
                    }
                    .info {
                        background: #f9f9f9;
                        border-left: 4px solid #667eea;
                        padding: 12px;
                        border-radius: 4px;
                        margin-top: 20px;
                        font-size: 13px;
                        color: #555;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>🔐 TixGo Identity Service</h1>
                    <p class="subtitle">Authentication & User Management for TixGo Events</p>
                    <div class="links">
                        <a href="/docs" class="btn-primary">📚 Swagger UI (Interactive)</a>
                        <a href="/redoc" class="btn-secondary">📖 ReDoc (Beautiful Docs)</a>
                        <a href="/health" class="btn-secondary">💚 Health Status</a>
                    </div>
                    <div class="info">
                        <strong>Demo Credentials:</strong><br/>
                        Username: <code>panitia1</code> | Password: <code>secret</code><br/>
                        Username: <code>admin1</code> | Password: <code>secret</code>
                    </div>
                </div>
            </body>
        </html>
        """


@app.get("/redoc")
def redoc_redirect():
        """Serve a resilient ReDoc page that loads ReDoc from the CDN but
        falls back to a visible link to /docs if the ReDoc script fails to load.
        This avoids showing a blank white page when the CDN is blocked.
        """
        return HTMLResponse(content="""
        <!doctype html>
        <html>
            <head>
                <meta charset="utf-8" />
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>TixGo Identity Service - ReDoc</title>
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


@app.post("/auth/register", response_model=MeResponse)
def register(req: RegisterRequest):
    if req.username in USERS:
        raise HTTPException(status_code=409, detail="Username already exists")

    _validate_password_length(req.password)

    role = req.role.strip().lower()
    if role not in {"committee", "admin"}:
        raise HTTPException(status_code=400, detail="Invalid role (use 'committee' or 'admin')")

    USERS[req.username] = {
        "password_hash": bcrypt.hash(req.password),
        "role": role,
    }
    return {"username": req.username, "role": role}


@app.post("/auth/login", response_model=TokenResponse)
def login(req: LoginRequest):
    user = USERS.get(req.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username/password")

    _validate_password_length(req.password)

    if not bcrypt.verify(req.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username/password")

    token = create_access_token(req.username, user["role"])
    return {"access_token": token, "token_type": "bearer"}


@app.get("/auth/me", response_model=MeResponse)
def me(authorization: Optional[str] = Header(None)):
    token = get_bearer_token(authorization)
    payload = decode_token(token)
    return {"username": payload.get("sub", ""), "role": payload.get("role", "")}