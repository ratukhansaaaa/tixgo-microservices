import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

import jwt
from fastapi import FastAPI, HTTPException, Header
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