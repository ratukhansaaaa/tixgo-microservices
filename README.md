# TixGo MicroservicesTixGo Microservices

===================

Sistem microservices berbasis FastAPI untuk manajemen ticketing dan event attendance. Proyek ini mendemonstrasikan implementasi arsitektur microservices dengan autentikasi JWT, otorisasi berbasis role, dan komunikasi inter-service.

This repository contains two FastAPI microservices used for the TixGo final project:

## 📋 Daftar Isi

- **identity-service**: authentication & authorization (register, login, me, role-based access)

- [Overview](#overview)- **attendance-service**: check-in management (create checkin, fetch attendance per event)

- [Arsitektur Sistem](#arsitektur-sistem)

- [Persyaratan Deployment](#persyaratan-deployment)## Architecture Overview

- [Panduan Deployment di STB](#panduan-deployment-di-stb)

- [Cara Mengakses Layanan](#cara-mengakses-layanan)```

- [Dokumentasi API](#dokumentasi-api)┌─────────────────────────────────────────────────────────────┐

- [Autentikasi & Otorisasi](#autentikasi--otorisasi)│                    Public Internet / STB                     │

- [Testing](#testing)└─────────────────────────────────────────────────────────────┘

- [Troubleshooting](#troubleshooting)              ↓                              ↓

        Port 18081                     Port 18082

---              ↓                              ↓

    ┌──────────────────┐        ┌──────────────────┐

## Overview    │ Identity Service │        │Attendance Service│

    │   (FastAPI)      │        │   (FastAPI)      │

**TixGo Microservices** terdiri dari dua layanan independen yang dirancang untuk menangani aspek berbeda dari sistem manajemen event:    │                  │        │                  │

    │ • Register       │        │ • Create Checkin │

### 1. **Identity Service** (Port 18081)    │ • Login (JWT)    │        │ • Get Attendance │

Menangani:    │ • /me endpoint   │        │ • Authorization  │

- Registrasi user baru    └──────────────────┘        └──────────────────┘

- Login dan token generation (JWT)         8000/tcp                      8000/tcp

- Verifikasi identitas user              ↓                              ↓

- Manajemen role (committee, admin)    ┌──────────────────┐        ┌──────────────────┐

    │   Container      │        │   Container      │

### 2. **Attendance Service** (Port 18082)    │ (Python 3.11)    │        │ (Python 3.11)    │

Menangani:    └──────────────────┘        └──────────────────┘

- Check-in peserta ke event```

- Pencatatan kehadiran per event

- Query data kehadiran dengan filter event## Deployment Files

- Validasi token dari Identity Service

- `docker-compose.yml` — development compose file

**Tech Stack:**- `docker-compose.prod.yml` — production-ready compose file with host ports mapped (18081/18082)

- FastAPI 0.115.6- `deploy.sh` — automated deployment script for STB

- Python 3.11- `smoke-test.sh` — quick verification/testing script

- Docker & Docker Compose- `cloudflared/config.yml.example` — example Cloudflare Tunnel config 

- JWT Authentication (HS256)- `.env.example` — environment variables template

- In-memory data store

## API Endpoints Reference

---

### Identity Service (Port 18081)

## Arsitektur Sistem

#### 1. Health Check

``````http

┌─────────────────────────────────────────────────────────────────┐GET /health

│                    Public Internet / STB                         │```

│             (Diakses via domain atau IP publik)                 │**Response:** `200 OK`

└──────────────────────────┬──────────────────────────────────────┘```json

                           │{

            ┌──────────────┴──────────────┐  "status": "ok",

            │                             │  "service": "identity-service"

       Port 18081                   Port 18082}

            │                             │```

    ┌───────▼─────────────┐     ┌────────▼─────────────┐

    │ Identity Service    │     │ Attendance Service   │#### 2. User Registration

    │ (dina.*.my.id)      │     │ (ratu.*.my.id)       │```http

    │                     │     │                      │POST /auth/register

    │ • Register User     │     │ • Create Check-in    │Content-Type: application/json

    │ • Login (JWT)       │     │ • Get Attendance     │

    │ • Get User Info     │     │ • Verify JWT Token   │{

    │                     │     │                      │  "username": "string (min 3, max 50)",

    └─────────────────────┘     └──────────────────────┘  "password": "string (min 4, max 200 bytes)",

           │                              │  "role": "string (committee|admin)"

           │  FastAPI App                │  FastAPI App}

           │  (Container Port 8000)      │  (Container Port 8000)```

           │                              │**Response:** `200 OK`

    ┌──────▼─────────────┐     ┌────────▼──────────────┐```json

    │  Docker Container   │     │  Docker Container    │{

    │  (Python 3.11)      │     │  (Python 3.11)       │  "username": "panitia1",

    │  tixgo-identity     │     │  tixgo-attendance    │  "role": "committee"

    └─────────────────────┘     └──────────────────────┘}

``````



---#### 3. User Login

```http

## Persyaratan DeploymentPOST /auth/login

Content-Type: application/json

### Hardware & Software

- **Docker & Docker Compose**: v2.0 atau lebih baru{

- **Git**: untuk clone repository  "username": "panitia1",

- **Memory**: minimal 2GB RAM  "password": "secret"

- **Disk Space**: minimal 500MB (untuk image + containers)}

- **Network**: port 18081 dan 18082 harus accessible```

**Response:** `200 OK`

### Pre-requisites```json

```bash{

# Verify Docker installed  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",

docker --version  "token_type": "bearer"

docker-compose --version}

```

# Verify Git installed

git --version#### 4. Get Current User Info

``````http

GET /auth/me

---Authorization: Bearer <TOKEN>

```

## Panduan Deployment di STB**Response:** `200 OK`

```json

### Step 1: Clone Repository{

```bash  "username": "panitia1",

cd /home/user  "role": "committee"

git clone https://github.com/ratukhansaaaa/tixgo-microservices.git}

cd tixgo-microservices```

```

### Attendance Service (Port 18082)

### Step 2: Setup Environment Variables

#### 1. Health Check

**PENTING:** Jangan commit `.env` ke repository. Buat file `.env` lokal dengan secrets yang aman.```http

GET /health

```bash```

# Copy template**Response:** `200 OK`

cp .env.example .env```json

{

# Edit dengan editor pilihan  "status": "ok",

nano .env  "service": "attendance"

```}

```

**Isi `.env` (REQUIRED):**

```env#### 2. Create Check-in

JWT_SECRET=<random-string-32-karakter-atau-lebih>```http

JWT_ALG=HS256POST /checkins

TOKEN_EXPIRE_MINUTES=120Content-Type: application/json

```Authorization: Bearer <TOKEN>



**Generate JWT_SECRET yang aman:**{

```bash  "event_id": "evt1",

# Menggunakan OpenSSL  "ticket_id": "TICKET123"

openssl rand -hex 32}

```

# ATAU menggunakan Python**Response:** `201 Created`

python3 -c "import secrets; print(secrets.token_hex(32))"```json

```{

  "status": "checked_in",

**Contoh `.env` yang valid:**  "record": {

```env    "event_id": "evt1",

JWT_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6    "ticket_id": "TICKET123",

JWT_ALG=HS256    "checked_in_by": "panitia1",

TOKEN_EXPIRE_MINUTES=120    "checked_in_at": "2026-01-03T13:25:53.415880+00:00"

```  }

}

### Step 3: Build & Deploy Services```

```bash**Error (duplicate):** `400 Bad Request`

# Build images (jika belum ada)```json

docker-compose build{

  "detail": "Ticket sudah pernah check-in"

# Start services di background}

docker-compose -f docker-compose.prod.yml up -d```



# Atau gunakan deploy script#### 3. Get Attendance by Event

chmod +x deploy.sh```http

./deploy.shGET /attendance/{event_id}

```Authorization: Bearer <TOKEN>

```

### Step 4: Verifikasi Deployment**Response:** `200 OK`

```json

**Check container status:**{

```bash  "event_id": "evt1",

docker ps  "total_checked_in": 1,

```  "records": [

    {

Expected output:      "event_id": "evt1",

```      "ticket_id": "TICKET123",

CONTAINER ID   IMAGE                     STATUS           PORTS      "checked_in_by": "panitia1",

xxxxx          tixgo-identity            Up 2 minutes     0.0.0.0:18081->8000/tcp      "checked_in_at": "2026-01-03T13:25:53.415880+00:00"

xxxxx          tixgo-attendance          Up 2 minutes     0.0.0.0:18082->8000/tcp    }

```  ]

}

**Health check endpoints:**```

```bash

# Identity Service## Authentication & Authorization

curl http://localhost:18081/health

### JWT Token Format

# Attendance ServiceTokens are signed with **HS256** and contain:

curl http://localhost:18082/health```json

```{

  "sub": "username",

Expected response:  "role": "committee|admin",

```json  "iat": 1234567890,

{"status": "ok", "service": "identity-service"}  "exp": 1234671490

{"status": "ok", "service": "attendance"}}

``````



---### Authorization Requirements

| Endpoint | Method | Auth Required | Roles |

## Cara Mengakses Layanan|----------|--------|---------------|-------|

| `/health` (both) | GET | ❌ | - |

### A. Akses Lokal (Di STB)| `/auth/register` | POST | ❌ | - |

| `/auth/login` | POST | ❌ | - |

Jika kamu test langsung di machine yang menjalankan Docker:| `/auth/me` | GET | ✅ | any |

| `/checkins` | POST | ✅ | any |

```bash| `/attendance/{event_id}` | GET | ✅ | any |

# Identity Service

curl http://localhost:18081/health### Error Responses

curl http://localhost:18081/auth/register- **401 Unauthorized**: Missing or invalid token

curl http://localhost:18081/auth/login  ```json

  {"detail": "Missing Authorization header"}

# Attendance Service  {"detail": "Token expired"}

curl http://localhost:18082/health  {"detail": "Invalid token"}

curl http://localhost:18082/checkins  ```

```- **400 Bad Request**: Invalid input or duplicate check-in

  ```json

### B. Akses via IP Address (Network)  {"detail": "Ticket sudah pernah check-in"}

  ```

Jika diakses dari machine lain di network yang sama:

## Important Notes for Deployment

```bash

# Replace <STB_IP> dengan IP address STB## Important Notes for Deployment

# Contoh: 192.168.1.100

### 1. Environment Configuration

curl http://192.168.1.100:18081/health**Do NOT commit your real `.env` into git.** Create a `.env` file on the STB with production secrets:

curl http://192.168.1.100:18082/health

``````env

JWT_SECRET=<long-random-hex-string-min-32-chars>

### C. Akses via Domain Publik (Recommended)JWT_ALG=HS256

TOKEN_EXPIRE_MINUTES=120

**Backend Team (BT)** akan melakukan routing via Cloudflare Tunnel atau reverse proxy:```



```bashGenerate a secure JWT_SECRET:

# Identity Service```bash

curl https://dina.theokaitou.my.id/health# Using OpenSSL

curl https://dina.theokaitou.my.id/auth/loginopenssl rand -hex 32



# Attendance Service# Using Python

curl https://ratu.theokaitou.my.id/healthpython3 -c "import secrets; print(secrets.token_hex(32))"

curl https://ratu.theokaitou.my.id/checkins```

```

### 2. Port Mapping

**Domain Mapping:**Services are mapped to host ports for easy routing :

- Identity Service: `dina.theokaitou.my.id` → `STB_IP:18081`- **Identity Service**: Container port 8000 → Host port 18081

- Attendance Service: `ratu.theokaitou.my.id` → `STB_IP:18082`- **Attendance Service**: Container port 8000 → Host port 18082



---can then route:

- `dina.theokaitou.my.id` → `STB_IP:18081` (identity)

## Dokumentasi API- `ratu.theokaitou.my.id` → `STB_IP:18082` (attendance)



### Identity Service (Port 18081)### 3. Deployment Steps on STB



#### 1. Health Check**Prerequisites:**

**Endpoint:** `GET /health`- Docker & Docker Compose installed

- Git repository cloned

**Authentication:** ❌ Tidak diperlukan- `.env` file with production secrets ready



**Response (200 OK):****Deploy:**

```json```bash

{# Copy production .env to STB

  "status": "ok",scp .env user@stb:/home/user/tixgo-microservices/.env

  "service": "identity-service"

}# SSH into STB and deploy

```ssh user@stb

cd /home/user/tixgo-microservices

**Curl Example:**chmod +x deploy.sh

```bash./deploy.sh

curl http://localhost:18081/health```

```

**Expected Output:**

---```bash

$ ./deploy.sh

#### 2. User Registration✓ Building images...

**Endpoint:** `POST /auth/register`✓ Starting containers...

✓ Services are running on ports 18081 and 18082

**Authentication:** ❌ Tidak diperlukan```



**Request Body:**### 4. Testing the Deployment

```json

{**Local Testing (on STB):**

  "username": "string (min 3, max 50 karakter)",```bash

  "password": "string (min 4, max 200 karakter)",curl http://localhost:18081/health

  "role": "string (committee|admin) - default: committee"curl http://localhost:18082/health

}```

```

**Remote Testing (via public domain):**

**Response (200 OK):**```bash

```jsoncurl https://dina.theokaitou.my.id/health

{curl https://ratu.theokaitou.my.id/health

  "username": "panitia1",```

  "role": "committee"

}**Full Workflow Example:**

``````bash

# Login

**Curl Example:**TOKEN=$(curl -s -X POST https://dina.theokaitou.my.id/auth/login \

```bash  -H "Content-Type: application/json" \

curl -X POST http://localhost:18081/auth/register \  -d '{"username":"panitia1","password":"secret"}' \

  -H "Content-Type: application/json" \  | jq -r .access_token)

  -d '{

    "username": "panitia1",# Create check-in

    "password": "rahasia123",curl -X POST https://ratu.theokaitou.my.id/checkins \

    "role": "committee"  -H "Content-Type: application/json" \

  }'  -H "Authorization: Bearer $TOKEN" \

```  -d '{"event_id":"evt1","ticket_id":"TICKET123"}'



**Error Response (400):**# Fetch attendance

```jsoncurl -H "Authorization: Bearer $TOKEN" \

{  https://ratu.theokaitou.my.id/attendance/evt1

  "detail": "User panitia1 sudah terdaftar"```

}

```### 5. Automated Testing

Run the smoke test to verify all services:

---```bash

# Local

#### 3. User Login./smoke-test.sh http://localhost:18081 http://localhost:18082

**Endpoint:** `POST /auth/login`

# Remote

**Authentication:** ❌ Tidak diperlukan./smoke-test.sh https://dina.theokaitou.my.id https://ratu.theokaitou.my.id

```

**Request Body:**

```jsonThe smoke test will:

{Check health endpoints

  "username": "string",Register & login a user

  "password": "string"Create a check-in

}Fetch attendance data

```

## Project Structure

**Response (200 OK):**

```json```

{tixgo-microservices/

  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwYW5pdGlhMSIsInJvbGUiOiJjb21taXR0ZWUiLCJpYXQiOjE3Njc0NDY3NDIsImV4cCI6MTc2NzQ1Mzk0Mn0.MU1pIorjZmKyhe7hweDGHkLvFzPtsxCCFo6FMnYiXxE",├── identity-service/

  "token_type": "bearer"│   ├── Dockerfile

}│   ├── requirements.txt

```│   └── app/

│       └── main.py           # FastAPI app with auth endpoints

**Curl Example:**├── attendance-service/

```bash│   ├── Dockerfile

# Login│   ├── requirements.txt

TOKEN=$(curl -s -X POST http://localhost:18081/auth/login \│   └── app/

  -H "Content-Type: application/json" \│       └── main.py           # FastAPI app with checkin endpoints

  -d '{├── cloudflared/

    "username": "panitia1",│   └── config.yml.example    # Cloudflare Tunnel config 

    "password": "rahasia123"├── docker-compose.yml        # Development compose

  }' | jq -r .access_token)├── docker-compose.prod.yml   # Production compose

├── deploy.sh                 # Deployment script for STB

# Print token (untuk digunakan di request lain)├── smoke-test.sh             # Automated test script

echo $TOKEN├── .env                      # Production environment (DO NOT COMMIT)

```├── .env.example              # Environment template

└── README.md                 # This file

**Error Response (400):**```

```json

{## Technology Stack

  "detail": "Username atau password salah"

}- **Framework**: FastAPI 0.115.6+ (Python 3.11)

```- **Authentication**: PyJWT with HS256 signing

- **Password Hashing**: bcrypt (passlib)

---- **Server**: Uvicorn (ASGI)

- **Containerization**: Docker & Docker Compose

#### 4. Get Current User Info- **Data Storage**: In-memory (dictionary-based)

**Endpoint:** `GET /auth/me`

## Known Limitations & Future Improvements

**Authentication:** ✅ Bearer Token Required

### Current Limitations:

**Request Headers:**- **In-memory storage**: Data is lost on container restart

```- **No persistence**: Consider adding SQLite or PostgreSQL

Authorization: Bearer <access_token>- **No rate limiting**: May need API gateway for production

```- **No logging**: Add structured logging (ELK stack, etc.)



**Response (200 OK):**### Recommended Enhancements:

```json1. Add database persistence (SQLite for dev, PostgreSQL for prod)

{2. Implement rate limiting middleware

  "username": "panitia1",3. Add request/response logging

  "role": "committee"4. Set up API monitoring (Prometheus, Grafana)

}5. Add user management UI

```6. Implement refresh tokens for better security

7. Add multi-language support

**Curl Example:**

```bash## Troubleshooting

curl -H "Authorization: Bearer $TOKEN" \

  http://localhost:18081/auth/me### Containers won't start

``````bash

# Check logs

**Error Response (401):**docker-compose logs -f

```json

{# Rebuild images

  "detail": "Missing Authorization header"docker-compose down

}docker-compose up -d --build

``````



---### Port already in use

```bash

### Attendance Service (Port 18082)# Find process using port 18081

lsof -i :18081

#### 1. Health Checkkill -9 <PID>

**Endpoint:** `GET /health`

# Or modify docker-compose.yml port mapping

**Authentication:** ❌ Tidak diperlukan```



**Response (200 OK):**### Token expired or invalid

```json```bash

{# Generate new token

  "status": "ok",curl -X POST http://localhost:18081/auth/login \

  "service": "attendance"  -H "Content-Type: application/json" \

}  -d '{"username":"panitia1","password":"secret"}'

``````



**Curl Example:**### Check-in fails with "already checked in"

```bash```bash

curl http://localhost:18082/health# Use different ticket_id for new check-in

```curl -X POST http://localhost:18082/checkins \

  -H "Content-Type: application/json" \

---  -H "Authorization: Bearer $TOKEN" \

  -d '{"event_id":"evt1","ticket_id":"UNIQUE_TICKET_ID"}'

#### 2. Create Check-in```

**Endpoint:** `POST /checkins`

## Security Considerations

**Authentication:** ✅ Bearer Token Required

1. **JWT Secret**: Keep JWT_SECRET safe. Change before deployment.

**Request Body:**2. **HTTPS**: Always use HTTPS in production 

```json3. **Password Requirements**: Minimum 4 characters (bcrypt hashed, max 72 bytes)

{4. **Token Expiry**: Default 120 minutes, configurable via TOKEN_EXPIRE_MINUTES

  "event_id": "string (min 1 karakter)",5. **No CORS configured**: Add if needed for cross-origin requests

  "ticket_id": "string (min 1 karakter)"

}## Testing Results

```

 All endpoints tested and working:

**Request Headers:**- Health checks: PASSING

```- User registration: PASSING

Authorization: Bearer <access_token>- User login & JWT generation: PASSING

Content-Type: application/json- Token validation (/me): PASSING

```- Check-in creation: PASSING

- Attendance retrieval: PASSING

**Response (200 OK):**- Authorization enforcement: PASSING

```json

{See `smoke-test.sh` for automated test suite.

  "status": "checked_in",

  "record": {## Contact & Support
    "event_id": "evt1",
    "ticket_id": "TICKET123",
    "checked_in_by": "panitia1",
    "checked_in_at": "2026-01-03T13:25:53.415880+00:00"
  }
}
```

**Curl Example:**
```bash
# Pastikan TOKEN sudah dari login sebelumnya
curl -X POST http://localhost:18082/checkins \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "event_id": "evt_konsert_2026",
    "ticket_id": "TKT-001"
  }'
```

**Error Response (400 - Duplicate Check-in):**
```json
{
  "detail": "Ticket sudah pernah check-in"
}
```

**Error Response (401 - Invalid Token):**
```json
{
  "detail": "Token expired"
}
```

---

#### 3. Get Attendance by Event
**Endpoint:** `GET /attendance/{event_id}`

**Authentication:** ✅ Bearer Token Required

**Path Parameters:**
```
event_id: string
```

**Request Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "event_id": "evt1",
  "total_checked_in": 2,
  "records": [
    {
      "event_id": "evt1",
      "ticket_id": "TICKET123",
      "checked_in_by": "panitia1",
      "checked_in_at": "2026-01-03T13:25:53.415880+00:00"
    },
    {
      "event_id": "evt1",
      "ticket_id": "TICKET456",
      "checked_in_by": "panitia1",
      "checked_in_at": "2026-01-03T13:30:12.123456+00:00"
    }
  ]
}
```

**Curl Example:**
```bash
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:18082/attendance/evt_konsert_2026
```

**Error Response (401 - Missing Auth):**
```json
{
  "detail": "Missing Authorization header"
}
```

---

## Autentikasi & Otorisasi

### JWT Token Format

Token yang dihasilkan oleh `/auth/login` adalah JWT (JSON Web Token) yang di-sign dengan algoritma HS256.

**Struktur Token:**
```
Header.Payload.Signature
```

**Payload (decoded):**
```json
{
  "sub": "panitia1",           // username
  "role": "committee",          // user role (committee|admin)
  "iat": 1767446742,            // issued at (timestamp)
  "exp": 1767453942             // expiration (timestamp)
}
```

**Token Lifetime:**
- Default: 120 menit
- Setelah expired, user harus login ulang untuk mendapat token baru

### Authorization Rules

| Endpoint | Method | Auth Required | Role Required | Deskripsi |
|----------|--------|---------------|---------------|-----------|
| `/health` (both) | GET | ❌ | - | Health check publik |
| `/auth/register` | POST | ❌ | - | Registrasi user baru |
| `/auth/login` | POST | ❌ | - | Login untuk dapat token |
| `/auth/me` | GET | ✅ | any | Lihat info user sendiri |
| `/checkins` | POST | ✅ | any | Buat check-in baru |
| `/attendance/{id}` | GET | ✅ | any | Lihat data kehadiran |

### Security Notes

1. **JWT_SECRET Management:**
   - Generate dengan `openssl rand -hex 32`
   - Simpan di `.env` - JANGAN commit ke git
   - Gunakan secret yang berbeda untuk development dan production
   - Rotate secret secara berkala

2. **Password Security:**
   - Password di-hash menggunakan bcrypt
   - Panjang password: 4-200 karakter
   - Password > 72 bytes akan ditolak (bcrypt limit)

3. **Token Security:**
   - Token hanya valid 120 menit
   - Token disimpan di client, bukan di server
   - Gunakan HTTPS untuk transmit token
   - Jangan expose token di URL atau logs

4. **Cross-Service Communication:**
   - Attendance Service memverifikasi token menggunakan JWT_SECRET yang sama
   - Pastikan JWT_SECRET konsisten di semua services

---

## Testing

### Automated Testing

**Smoke Test Script:**
```bash
chmod +x smoke-test.sh
./smoke-test.sh http://localhost:18081 http://localhost:18082
```

Script ini akan:
1. Check health endpoints
2. Register user baru (jika belum ada)
3. Login dan dapatkan token
4. Buat check-in baru
5. Fetch attendance data
6. Report hasil test

**Expected Output:**
```
Checking health endpoints...
{ "status": "ok", "service": "identity-service" }
{ "status": "ok", "service": "attendance" }

Logging in as demo user (panitia1 / secret)
Token: eyJhbGc...

Creating checkin...
{ "status": "checked_in", "record": {...} }

Fetching attendance...
{ "event_id": "evt-smoke", "total_checked_in": 1, "records": [...] }

Smoke test finished. If the above responses look correct, services are working.
```

### Manual Testing Flow

**Complete workflow test:**

```bash
# 1. Register user baru
curl -X POST http://localhost:18081/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123",
    "role": "committee"
  }'

# Response:
# {"username": "testuser", "role": "committee"}

# 2. Login dan simpan token
TOKEN=$(curl -s -X POST http://localhost:18081/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }' | jq -r .access_token)

echo "Token obtained: ${TOKEN:0:50}..."

# 3. Verify token dengan /me endpoint
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:18081/auth/me

# Response:
# {"username": "testuser", "role": "committee"}

# 4. Create check-in
curl -X POST http://localhost:18082/checkins \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "event_id": "konsert_2026",
    "ticket_id": "TKT-TEST-001"
  }'

# Response:
# {"status": "checked_in", "record": {...}}

# 5. Get attendance for event
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:18082/attendance/konsert_2026

# Response:
# {"event_id": "konsert_2026", "total_checked_in": 1, "records": [...]}
```

### Testing via Public Domain

Setelah BT setup routing:

```bash
# Health check via domain
curl https://dina.theokaitou.my.id/health
curl https://ratu.theokaitou.my.id/health

# Login via domain
TOKEN=$(curl -s -X POST https://dina.theokaitou.my.id/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"panitia1","password":"secret"}' | jq -r .access_token)

# Create check-in via domain
curl -X POST https://ratu.theokaitou.my.id/checkins \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"event_id":"evt1","ticket_id":"TICKET123"}'
```

---

## Troubleshooting

### Problem: Containers tidak running

**Diagnosis:**
```bash
docker-compose logs identity-service
docker-compose logs attendance-service
docker ps
```

**Solution:**
```bash
# Rebuild images
docker-compose build

# Start dengan full output untuk debug
docker-compose up (tanpa -d flag)

# Check if ports are already in use
lsof -i :18081
lsof -i :18082
```

### Problem: Port 18081 atau 18082 sudah digunakan

**Solution:**
```bash
# Kill process yang menggunakan port
lsof -ti:18081 | xargs kill -9
lsof -ti:18082 | xargs kill -9

# ATAU ubah port di docker-compose.yml:
# ports:
#   - "18083:8000"  (ganti 18081 dengan 18083)
```

### Problem: JWT_SECRET error atau token tidak valid

**Diagnosis:**
```bash
# Check .env file
cat .env

# Login dan lihat error detail
curl -v -X POST http://localhost:18081/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"panitia1","password":"secret"}'
```

**Solution:**
```bash
# Pastikan JWT_SECRET di .env:
# 1. Tidak kosong
# 2. Sama persis di semua services
# 3. Min 32 karakter untuk security

# Generate baru jika perlu:
openssl rand -hex 32

# Update .env dan restart:
docker-compose restart
```

### Problem: "Token expired" error saat create check-in

**Cause:** Token sudah kadaluarsa (> 120 menit)

**Solution:**
```bash
# Login ulang untuk dapat token fresh
TOKEN=$(curl -s -X POST http://localhost:18081/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"panitia1","password":"secret"}' | jq -r .access_token)

# Cek token expiration (decode JWT)
echo $TOKEN | cut -d'.' -f2 | base64 -d | jq .exp
```

### Problem: "Ticket sudah pernah check-in"

**This is expected behavior!** Ticket ID harus unik per event untuk mencegah double check-in.

**Solution:**
```bash
# Gunakan ticket_id yang berbeda
curl -X POST http://localhost:18082/checkins \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "event_id": "evt1",
    "ticket_id": "TKT-UNIQUE-002"  # Ganti dengan ID baru
  }'
```

### Problem: 401 Unauthorized error

**Cause:** Authorization header missing atau format salah

**Check:**
```bash
# Format harus: "Bearer <token>"
curl -H "Authorization: Bearer $TOKEN" http://localhost:18082/checkins

# TIDAK boleh (akan error):
curl -H "Authorization: $TOKEN" ...           # Missing "Bearer"
curl -H "Authorization: Token $TOKEN" ...     # Salah prefix
curl http://localhost:18082/checkins          # Missing header
```

### View Logs

```bash
# Identity Service logs
docker-compose logs identity-service -f

# Attendance Service logs
docker-compose logs attendance-service -f

# All services
docker-compose logs -f

# Last 50 lines
docker-compose logs --tail=50
```

---

## File Structure

```
tixgo-microservices/
├── identity-service/
│   ├── app/
│   │   └── main.py              # Identity service implementation
│   ├── Dockerfile               # Container definition
│   └── requirements.txt          # Python dependencies
├── attendance-service/
│   ├── app/
│   │   └── main.py              # Attendance service implementation
│   ├── Dockerfile               # Container definition
│   └── requirements.txt          # Python dependencies
├── cloudflared/
│   └── config.yml.example       # Cloudflare Tunnel config (optional)
├── docker-compose.yml           # Development compose file
├── docker-compose.prod.yml      # Production compose file
├── deploy.sh                    # Automated deployment script
├── smoke-test.sh                # Automated testing script
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── README.md                    # This file
└── README.pdf                   # PDF version of documentation
```

---

## Development Notes

### Local Development (Without Docker)

Untuk development lokal tanpa Docker:

```bash
# 1. Setup virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r identity-service/requirements.txt
pip install -r attendance-service/requirements.txt

# 3. Run services (separate terminals)

# Terminal 1 - Identity Service
cd identity-service
JWT_SECRET=dev-secret uvicorn app.main:app --reload --port 8001

# Terminal 2 - Attendance Service
cd attendance-service
JWT_SECRET=dev-secret uvicorn app.main:app --reload --port 8002

# Access lokal:
# Identity: http://localhost:8001
# Attendance: http://localhost:8002
```

### Data Persistence

**Current Implementation:**
- Data disimpan in-memory (dictionary)
- Hilang saat container restart
- Cocok untuk development dan testing

**For Production:**
- Gunakan database seperti PostgreSQL atau SQLite
- Simpan data persistent
- Add database migrations
- Implement data backup strategy

### Future Improvements

1. **Event Management Service** (untuk Tugas 3)
   - Create, read, update, delete events
   - Link dengan Identity & Attendance services
   - Query attendance per event

2. **Database Persistence**
   - Replace in-memory storage dengan PostgreSQL
   - Add SQLAlchemy ORM
   - Implement migrations (Alembic)

3. **Advanced Features**
   - Rate limiting & throttling
   - API logging & monitoring
   - Metrics collection (Prometheus)
   - Distributed tracing (Jaeger)
   - Email notifications

4. **DevOps**
   - CI/CD pipeline (GitHub Actions)
   - Multi-architecture Docker images
   - Kubernetes deployment configs
   - Health checks & auto-restart policies

---

## References

- **FastAPI Documentation:** https://fastapi.tiangolo.com
- **Docker Documentation:** https://docs.docker.com
- **JWT Specification:** https://tools.ietf.org/html/rfc7519
- **FastAPI + Docker Best Practices:** https://fastapi.tiangolo.com/deployment/docker/

---

## License

Proyek ini dibuat untuk tujuan akademik/pembelajaran.

---

**Last Updated:** January 3, 2026
**Version:** 1.0.0
**Status:** Production Ready for Tugas 2
