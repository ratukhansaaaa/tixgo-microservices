import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

import jwt
from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from passlib.hash import bcrypt

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("identity-service")

app = FastAPI(
    title="TixGo Identity Service",
    version="1.0.0"
)

# CORS Configuration for GitHub Pages frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://irdinailmunaa.github.io",
        "http://localhost:8080",
        "http://localhost:3000",
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
JWT_ALG = os.getenv("JWT_ALG", "HS256")
TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRE_MINUTES", "120"))


def _password_bytes_len(pw: str) -> int:
    return len(pw.encode("utf-8"))


def _validate_password_length(pw: str) -> None:
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


USERS: Dict[str, Dict[str, str]] = {
    "panitia1": {"password_hash": bcrypt.hash("secret"), "role": "committee"},
    "admin1": {"password_hash": bcrypt.hash("secret"), "role": "admin"},
}


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


@app.get("/health")
def health():
    return {"status": "ok", "service": "identity-service"}


@app.get("/", response_class=HTMLResponse)
def root():
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
                        background: linear-gradient(135deg, #4a148c 0%, #6a1b9a 100%);
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
                        max-width: 500px;
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
                <div class="container">
                    <h1>TixGo Identity Service</h1>
                    <p class="subtitle">Authentication & User Management</p>
                    <div class="links">
                        <a href="/docs" class="btn-primary">Swagger UI (Interactive)</a>
                        <a href="/redoc" class="btn-secondary">ReDoc</a>
                        <a href="/health" class="btn-secondary">Health Status</a>
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



@app.post("/auth/register", response_model=MeResponse)
def register(req: RegisterRequest):
    if req.username in USERS:
        logger.warning(f"Registration attempt with existing username: {req.username}")
        raise HTTPException(status_code=409, detail="Username already exists")

    _validate_password_length(req.password)

    role = req.role.strip().lower()
    if role not in {"committee", "admin"}:
        logger.warning(f"Registration attempt with invalid role: {role}")
        raise HTTPException(status_code=400, detail="Invalid role (use 'committee' or 'admin')")

    USERS[req.username] = {
        "password_hash": bcrypt.hash(req.password),
        "role": role,
    }
    logger.info(f"User registered successfully: {req.username} with role: {role}")
    return {"username": req.username, "role": role}


@app.post("/auth/login", response_model=TokenResponse)
def login(req: LoginRequest):
    user = USERS.get(req.username)
    if not user:
        logger.warning(f"Login attempt with non-existent username: {req.username}")
        raise HTTPException(status_code=401, detail="Invalid username/password")

    _validate_password_length(req.password)

    if not bcrypt.verify(req.password, user["password_hash"]):
        logger.warning(f"Login attempt with wrong password for username: {req.username}")
        raise HTTPException(status_code=401, detail="Invalid username/password")

    token = create_access_token(req.username, user["role"])
    logger.info(f"User logged in successfully: {req.username}")
    return {"access_token": token, "token_type": "bearer"}


@app.get("/auth/me", response_model=MeResponse)
def me(authorization: Optional[str] = Header(None)):
    token = get_bearer_token(authorization)
    payload = decode_token(token)
    return {"username": payload.get("sub", ""), "role": payload.get("role", "")}