# TixGo Microservices

Sistem microservices berbasis FastAPI untuk manajemen ticketing dan event attendance.

## Overview

Dua layanan microservices independen berjalan di Docker containers dengan port mapping masing-masing:

**1. Identity Service (Port 18081)**
- User registration dengan password hashing (bcrypt)
- Login dan JWT token generation (HS256)
- User info retrieval endpoint
- Role management (committee, admin)

**2. Attendance Service (Port 18082)**
- Check-in peserta ke event
- Attendance query per event
- JWT token validation

**Tech Stack:** FastAPI 0.115.6, Python 3.11, Docker & Docker Compose, JWT Authentication (HS256), bcrypt password hashing, in-memory data store.

## Cara Mengakses Layanan

Dokumentasi ini menjelaskan tiga cara untuk mengakses layanan:

### 1. Akses Lokal (di STB)

Testing langsung di machine yang menjalankan Docker:

```bash
curl http://localhost:18081/health
curl http://localhost:18082/health
```

**Identity Service endpoints:**
- Register: `POST http://localhost:18081/auth/register`
- Login: `POST http://localhost:18081/auth/login`
- Get user: `GET http://localhost:18081/auth/me` (requires token)
- Health: `GET http://localhost:18081/health`

**Attendance Service endpoints:**
- Create checkin: `POST http://localhost:18082/checkins` (requires token)
- Get attendance: `GET http://localhost:18082/attendance/{event_id}` (requires token)
- Health: `GET http://localhost:18082/health`

### 2. Akses via IP Address (Network)

Dari machine lain di network yang sama. Replace `<STB_IP>` dengan IP address STB:

```bash
curl http://<STB_IP>:18081/health
curl http://<STB_IP>:18082/health
```

**Contoh:** `curl http://192.168.1.100:18081/health`

**Mapping:**
- Identity Service: `http://<STB_IP>:18081`
- Attendance Service: `http://<STB_IP>:18082`

### 3. Akses via Domain Publik

Setelah domain publik dikonfigurasi via reverse proxy atau Cloudflare Tunnel:

```bash
curl https://<identity-domain>/health
curl https://<attendance-domain>/health
```

**Domain Mapping:**
- Identity Service: `<identity-domain>` → `<STB_IP>:18081`
- Attendance Service: `<attendance-domain>` → `<STB_IP>:18082`

## Quick Start - Setup & Deployment

### Prerequisites

```bash
docker --version
docker-compose --version
git --version
```

### Installation

```bash
# 1. Clone repository
git clone https://github.com/ratukhansaaaa/tixgo-microservices.git
cd tixgo-microservices

# 2. Create .env file (DO NOT commit this file to git)
cp .env.example .env
nano .env
```

Isi `.env` dengan:
```env
JWT_SECRET=<generated-secret-min-32-chars>
JWT_ALG=HS256
TOKEN_EXPIRE_MINUTES=120
```

Generate JWT_SECRET:
```bash
openssl rand -hex 32
```

```bash
# 3. Build dan deploy
docker-compose build
docker-compose -f docker-compose.prod.yml up -d

# Or use deploy script
chmod +x deploy.sh
./deploy.sh

# 4. Verify deployment
docker ps
curl http://localhost:18081/health
curl http://localhost:18082/health
```

## API Documentation

### Identity Service (Port 18081)

#### 1. Health Check
```http
GET /health
```

Response (200):
```json
{"status": "ok", "service": "identity-service"}
```

#### 2. Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "panitia1",
  "password": "secret",
  "role": "committee"
}
```

Response (200):
```json
{
  "username": "panitia1",
  "role": "committee"
}
```

Parameters:
- `username`: min 3, max 50 chars
- `password`: min 4, max 200 chars
- `role`: "committee" atau "admin"

Example:
```bash
curl -X POST http://localhost:18081/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"panitia1","password":"secret","role":"committee"}'
```

#### 3. User Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "panitia1",
  "password": "secret"
}
```

Response (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

Example:
```bash
TOKEN=$(curl -s -X POST http://localhost:18081/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"panitia1","password":"secret"}' | jq -r .access_token)
```

#### 4. Get Current User Info
```http
GET /auth/me
Authorization: Bearer <access_token>
```

Response (200):
```json
{
  "username": "panitia1",
  "role": "committee"
}
```

Example:
```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:18081/auth/me
```

### Attendance Service (Port 18082)

#### 1. Health Check
```http
GET /health
```

Response (200):
```json
{"status": "ok", "service": "attendance"}
```

#### 2. Create Check-in
```http
POST /checkins
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "event_id": "evt1",
  "ticket_id": "TICKET123"
}
```

Response (201):
```json
{
  "status": "checked_in",
  "record": {
    "event_id": "evt1",
    "ticket_id": "TICKET123",
    "checked_in_by": "panitia1",
    "checked_in_at": "2026-01-03T13:25:53.415880+00:00"
  }
}
```

Example:
```bash
curl -X POST http://localhost:18082/checkins \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"event_id":"evt1","ticket_id":"TICKET123"}'
```

#### 3. Get Attendance by Event
```http
GET /attendance/{event_id}
Authorization: Bearer <access_token>
```

Response (200):
```json
{
  "event_id": "evt1",
  "total_checkins": 2,
  "records": [
    {
      "ticket_id": "TICKET123",
      "checked_in_by": "panitia1",
      "checked_in_at": "2026-01-03T13:25:53.415880+00:00"
    }
  ]
}
```

Example:
```bash
curl -H "Authorization: Bearer $TOKEN" http://localhost:18082/attendance/evt1
```

## Authentication & Authorization

### JWT Token Format

Token dari `/auth/login` adalah JWT yang di-sign dengan HS256 algorithm.

**Payload struktur:**
```json
{
  "sub": "username",
  "role": "committee|admin",
  "iat": 1767446742,
  "exp": 1767453942
}
```

Token lifetime: 120 menit.

### Authorization Rules

| Endpoint | Auth | Role |
|----------|------|------|
| `/health` | No | - |
| `/auth/register` | No | - |
| `/auth/login` | No | - |
| `/auth/me` | Yes | any |
| `/checkins` | Yes | any |
| `/attendance/{id}` | Yes | any |

### Security

1. **JWT_SECRET:** Generate dengan `openssl rand -hex 32`, simpan di `.env`, jangan commit
2. **Password:** Min 4 char, max 200 char, di-hash dengan bcrypt
3. **Token:** Valid 120 menit, gunakan HTTPS di production

## Testing

### Automated Test
```bash
chmod +x smoke-test.sh
./smoke-test.sh
```

### Manual Test Workflow

```bash
# 1. Register
curl -X POST http://localhost:18081/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"pass123","role":"committee"}'

# 2. Login
TOKEN=$(curl -s -X POST http://localhost:18081/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"pass123"}' | jq -r .access_token)

# 3. Get user info
curl -H "Authorization: Bearer $TOKEN" http://localhost:18081/auth/me

# 4. Create check-in
curl -X POST http://localhost:18082/checkins \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"event_id":"evt1","ticket_id":"TICKET001"}'

# 5. Get attendance
curl -H "Authorization: Bearer $TOKEN" http://localhost:18082/attendance/evt1
```

## Troubleshooting

### Port sudah digunakan
```bash
lsof -i :18081
lsof -i :18082
kill -9 <PID>
```

### JWT_SECRET error
```bash
cat .env
openssl rand -hex 32
nano .env
docker-compose restart
```

### Login gagal
```bash
docker logs tixgo-identity
docker logs tixgo-attendance
```

### Token validation error
1. Token expired → login ulang
2. Format header salah → gunakan `Authorization: Bearer <token>`
3. JWT_SECRET berbeda → verifikasi `.env`

### Container tidak start
```bash
docker-compose logs -f
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Project Structure

```
tixgo-microservices/
├── identity-service/
│   ├── app/main.py
│   ├── Dockerfile
│   └── requirements.txt
├── attendance-service/
│   ├── app/main.py
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── docker-compose.prod.yml
├── deploy.sh
├── smoke-test.sh
├── .env.example
├── README.md
└── README.pdf
```

## References

- FastAPI: https://fastapi.tiangolo.com
- Docker: https://docs.docker.com
- JWT: https://tools.ietf.org/html/rfc7519

---

**Version:** 1.0.0
**Status:** Production Ready for Tugas 2
**Repository:** https://github.com/ratukhansaaaa/tixgo-microservices
