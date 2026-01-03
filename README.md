# TixGo Microservices# TixGo Microservices# TixGo Microservices# TixGo Microservices# TixGo MicroservicesTixGo Microservices



Sistem microservices berbasis FastAPI untuk manajemen ticketing dan event attendance. Proyek ini mendemonstrasikan implementasi arsitektur microservices dengan autentikasi JWT, otorisasi berbasis role, dan komunikasi inter-service.



## Daftar IsiSistem microservices berbasis FastAPI untuk manajemen ticketing dan event attendance. Proyek ini mendemonstrasikan implementasi arsitektur microservices dengan autentikasi JWT, otorisasi berbasis role, dan komunikasi inter-service.



- [Overview](#overview)

- [Arsitektur Sistem](#arsitektur-sistem)

- [Persyaratan Deployment](#persyaratan-deployment)## Daftar IsiSistem microservices berbasis FastAPI untuk manajemen ticketing dan event attendance. Proyek ini mendemonstrasikan implementasi arsitektur microservices dengan autentikasi JWT, otorisasi berbasis role, dan komunikasi inter-service.

- [Panduan Deployment](#panduan-deployment)

- [Cara Mengakses Layanan](#cara-mengakses-layanan)

- [Dokumentasi API](#dokumentasi-api)

- [Autentikasi dan Otorisasi](#autentikasi-dan-otorisasi)- [Overview](#overview)

- [Testing](#testing)

- [Troubleshooting](#troubleshooting)- [Arsitektur Sistem](#arsitektur-sistem)



## Overview- [Persyaratan Deployment](#persyaratan-deployment)## Daftar IsiSistem microservices berbasis FastAPI untuk manajemen ticketing dan event attendance. Proyek ini mendemonstrasikan implementasi arsitektur microservices dengan autentikasi JWT, otorisasi berbasis role, dan komunikasi inter-service.===================



TixGo Microservices terdiri dari dua layanan independen:- [Panduan Deployment](#panduan-deployment)



**1. Identity Service (Port 18081)**- [Cara Mengakses Layanan](#cara-mengakses-layanan)

- Menangani autentikasi dan manajemen identitas user

- Registrasi user baru dengan password hashing (bcrypt)- [Dokumentasi API](#dokumentasi-api)

- Login dan token generation (JWT HS256)

- Verifikasi identitas user melalui endpoint `/me`- [Autentikasi dan Otorisasi](#autentikasi-dan-otorisasi)- [Overview](#overview)

- Manajemen role berbasis (committee, admin)

- [Testing](#testing)

**2. Attendance Service (Port 18082)**

- Menangani check-in peserta dan pencatatan kehadiran- [Troubleshooting](#troubleshooting)- [Arsitektur Sistem](#arsitektur-sistem)

- Check-in peserta ke event dengan validasi token

- Pencatatan kehadiran per event dengan timestamp

- Query data kehadiran dengan filter event

- Validasi token dari Identity Service## Overview- [Persyaratan Deployment](#persyaratan-deployment)## Daftar IsiSistem microservices berbasis FastAPI untuk manajemen ticketing dan event attendance. Proyek ini mendemonstrasikan implementasi arsitektur microservices dengan autentikasi JWT, otorisasi berbasis role, dan komunikasi inter-service.



**Tech Stack:** FastAPI 0.115.6, Python 3.11, Docker, JWT Authentication (HS256), bcrypt password hashing, in-memory data store.



## Arsitektur SistemTixGo Microservices terdiri dari dua layanan independen yang dirancang untuk menangani aspek berbeda dari sistem manajemen event:- [Panduan Deployment](#panduan-deployment)



Dua layanan berjalan di Docker containers yang terpisah dengan port mapping masing-masing:



- **Identity Service**: berjalan di port 18081### 1. Identity Service (Port 18081)- [Cara Mengakses Layanan](#cara-mengakses-layanan)

- **Attendance Service**: berjalan di port 18082



Kedua services dapat diakses melalui:

1. Lokal (localhost) - untuk testing di STBMenangani seluruh aspek autentikasi dan manajemen identitas:- [Dokumentasi API](#dokumentasi-api)

2. IP Address - dari network yang sama

3. Domain publik - via Cloudflare Tunnel atau reverse proxy



Services berkomunikasi melalui shared JWT_SECRET untuk validasi token. Setiap service memiliki data store independen (in-memory).- Registrasi user baru dengan password hashing (bcrypt)- [Autentikasi dan Otorisasi](#autentikasi-dan-otorisasi)- [Overview](#overview)This repository contains two FastAPI microservices used for the TixGo final project:



## Persyaratan Deployment- Login dan token generation (JWT HS256)



**Hardware & Software:**- Verifikasi identitas user melalui endpoint `/me`- [Testing](#testing)

- Docker & Docker Compose v2.0 atau lebih baru

- Git untuk clone repository- Manajemen role berbasis (committee, admin)

- Minimal 2GB RAM untuk menjalankan 2 containers

- Minimal 500MB disk space- [Troubleshooting](#troubleshooting)- [Arsitektur Sistem](#arsitektur-sistem)

- Network: port 18081 dan 18082 harus accessible

### 2. Attendance Service (Port 18082)

**Verifikasi Prerequisites:**



```bash

docker --versionMenangani check-in peserta dan pencatatan kehadiran:

docker-compose --version

git --version## Overview- [Persyaratan Deployment](#persyaratan-deployment)## 📋 Daftar Isi

```

- Check-in peserta ke event dengan validasi token

## Panduan Deployment

- Pencatatan kehadiran per event dengan timestamp

### Step 1: Clone Repository

- Query data kehadiran dengan filter event

```bash

cd /home/user- Validasi token dari Identity ServiceTixGo Microservices terdiri dari dua layanan independen:- [Panduan Deployment](#panduan-deployment)

git clone https://github.com/ratukhansaaaa/tixgo-microservices.git

cd tixgo-microservices

```

### Tech Stack

### Step 2: Setup Environment Variables



Buat file `.env` lokal dengan secrets yang aman (jangan commit ke git):

- FastAPI 0.115.6 (ASGI Web Framework)**1. Identity Service (Port 18081)**- [Cara Mengakses Layanan](#cara-mengakses-layanan)- **identity-service**: authentication & authorization (register, login, me, role-based access)

```bash

cp .env.example .env- Python 3.11 (Runtime)

nano .env

```- Docker dan Docker Compose (Containerization)- Registrasi user baru



Isi `.env`:- JWT Authentication (HS256 algorithm)



```env- bcrypt (Password hashing)- Login dan token generation (JWT)- [Dokumentasi API](#dokumentasi-api)

JWT_SECRET=<random-string-min-32-karakter>

JWT_ALG=HS256- In-memory data store (development/testing)

TOKEN_EXPIRE_MINUTES=120

```- Verifikasi identitas user



Generate JWT_SECRET yang aman:## Arsitektur Sistem



```bash- Manajemen role (committee, admin)- [Autentikasi dan Otorisasi](#autentikasi-dan-otorisasi)- [Overview](#overview)- **attendance-service**: check-in management (create checkin, fetch attendance per event)

# Menggunakan OpenSSL

openssl rand -hex 32```



# Atau menggunakan Python┌─────────────────────────────────────────────────────────────┐

python3 -c "import secrets; print(secrets.token_hex(32))"

```│                    Public Internet / STB                     │



### Step 3: Build dan Deploy Services│             (Diakses via domain atau IP publik)             │**2. Attendance Service (Port 18082)**- [Testing](#testing)



```bash└──────────────────────────┬──────────────────────────────────┘

# Build images

docker-compose build- Check-in peserta ke event



# Start services di background                           │

docker-compose -f docker-compose.prod.yml up -d

- Pencatatan kehadiran per event- [Troubleshooting](#troubleshooting)- [Arsitektur Sistem](#arsitektur-sistem)

# Atau gunakan deploy script

chmod +x deploy.sh            ┌──────────────┴──────────────┐

./deploy.sh

```- Query data kehadiran dengan filter event



### Step 4: Verifikasi Deployment            │                             │



Check container status:- Validasi token dari Identity Service



```bash       Port 18081                   Port 18082

docker ps

```



Expected output:            │                             │



```Stack teknologi: FastAPI 0.115.6, Python 3.11, Docker, JWT Authentication (HS256), In-memory data store.## Overview- [Persyaratan Deployment](#persyaratan-deployment)## Architecture Overview

CONTAINER ID   IMAGE                     STATUS           PORTS

xxxxx          tixgo-identity            Up 2 minutes     0.0.0.0:18081->8000/tcp    ┌───────▼─────────────┐     ┌────────▼─────────────┐

xxxxx          tixgo-attendance          Up 2 minutes     0.0.0.0:18082->8000/tcp

```



Health check endpoints:    │ Identity Service    │     │ Attendance Service   │



```bash## Arsitektur Sistem

curl http://localhost:18081/health

curl http://localhost:18082/health    │                     │     │                      │

```



Expected response:

    │ • Register User     │     │ • Create Check-in    │

```json

{"status": "ok", "service": "identity-service"}```TixGo Microservices terdiri dari dua layanan independen:- [Panduan Deployment di STB](#panduan-deployment-di-stb)

{"status": "ok", "service": "attendance"}

```    │ • Login (JWT)       │     │ • Get Attendance     │



## Cara Mengakses Layanan┌─────────────────────────────────────────────────────────────┐



### A. Akses Lokal (Di STB)    │ • Get User Info     │     │ • Verify JWT Token   │



Testing langsung di machine yang menjalankan Docker:│                    Public Internet / STB                     │



```bash    └─────────────────────┘     └──────────────────────┘

# Identity Service

curl http://localhost:18081/health│             (Diakses via domain atau IP publik)             │

curl http://localhost:18081/auth/register

curl http://localhost:18081/auth/login            │                              │



# Attendance Service└──────────────────────────┬──────────────────────────────────┘**1. Identity Service (Port 18081)**- [Cara Mengakses Layanan](#cara-mengakses-layanan)```

curl http://localhost:18082/health

curl http://localhost:18082/checkins            │  FastAPI App                │  FastAPI App

```

                           │

### B. Akses via IP Address (Network)

            │  (Container Port 8000)      │  (Container Port 8000)

Dari machine lain di network yang sama (replace `<STB_IP>` dengan IP address STB):

            ┌──────────────┴──────────────┐- Registrasi user baru

```bash

# Identity Service            │                              │

curl http://<STB_IP>:18081/health

            │                             │

# Attendance Service

curl http://<STB_IP>:18082/health            ↓                              ↓

```

       Port 18081                   Port 18082- Login dan token generation (JWT)- [Dokumentasi API](#dokumentasi-api)┌─────────────────────────────────────────────────────────────┐

### C. Akses via Domain Publik

    ┌──────▼─────────────┐     ┌────────▼──────────────┐

Setelah domain publik dikonfigurasi via reverse proxy atau Cloudflare Tunnel:

            │                             │

```bash

# Identity Service    │  Docker Container   │     │  Docker Container    │

curl https://<identity-domain>/health

curl https://<identity-domain>/auth/login    ┌───────▼─────────────┐     ┌────────▼─────────────┐- Verifikasi identitas user



# Attendance Service    │  (Python 3.11)      │     │  (Python 3.11)       │

curl https://<attendance-domain>/health

curl https://<attendance-domain>/checkins    │ Identity Service    │     │ Attendance Service   │

```

    └─────────────────────┘     └──────────────────────┘

Domain mapping:

- Identity Service: `<identity-domain>` → `<STB_IP>:18081`    │                     │     │                      │- Manajemen role (committee, admin)- [Autentikasi & Otorisasi](#autentikasi--otorisasi)│                    Public Internet / STB                     │

- Attendance Service: `<attendance-domain>` → `<STB_IP>:18082`

        Port 18081                     Port 18082

## Dokumentasi API

    │ • Register User     │     │ • Create Check-in    │

### Identity Service (Port 18081)

            ↓                              ↓

#### 1. Health Check

    │ • Login (JWT)       │     │ • Get Attendance     │

**Endpoint:** `GET /health`

    ┌──────────────────┐        ┌──────────────────┐

```bash

curl http://localhost:18081/health    │ • Get User Info     │     │ • Verify JWT Token   │

```

    │ Identity Service │        │Attendance Service│

Response:

```json    └─────────────────────┘     └──────────────────────┘**2. Attendance Service (Port 18082)**- [Testing](#testing)└─────────────────────────────────────────────────────────────┘

{"status": "ok", "service": "identity-service"}

```    │   (FastAPI)      │        │   (FastAPI)      │



#### 2. User Registration           │                              │



**Endpoint:** `POST /auth/register`    │ • Register       │        │ • Create Checkin │



```bash           │  FastAPI App                │  FastAPI App- Check-in peserta ke event

curl -X POST http://localhost:18081/auth/register \

  -H "Content-Type: application/json" \    │ • Login (JWT)    │        │ • Get Attendance │

  -d '{

    "username": "panitia1",           │  (Container Port 8000)      │  (Container Port 8000)

    "password": "secret",

    "role": "committee"    │ • /me endpoint   │        │ • Authorization  │

  }'

```           │                              │- Pencatatan kehadiran per event- [Troubleshooting](#troubleshooting)              ↓                              ↓



Parameters:    └──────────────────┘        └──────────────────┘

- `username` (string): min 3, max 50 karakter

- `password` (string): min 4, max 200 karakter```    ┌──────▼─────────────┐     ┌────────▼──────────────┐

- `role` (string): `committee` atau `admin`



Response (200 OK):

```json## Persyaratan Deployment    │  Docker Container   │     │  Docker Container    │- Query data kehadiran dengan filter event

{

  "username": "panitia1",

  "role": "committee"

}### Hardware & Software    │  (Python 3.11)      │     │  (Python 3.11)       │

```



Error (400 - User sudah ada):

```json- **Docker & Docker Compose**: v2.0 atau lebih baru    └─────────────────────┘     └──────────────────────┘- Validasi token dari Identity Service        Port 18081                     Port 18082

{"detail": "User panitia1 sudah terdaftar"}

```- **Git**: untuk clone repository



#### 3. User Login- **Memory**: minimal 2GB RAM untuk menjalankan 2 containers```



**Endpoint:** `POST /auth/login`- **Disk Space**: minimal 500MB untuk images dan containers



```bash- **Network**: port 18081 dan 18082 harus accessible

curl -X POST http://localhost:18081/auth/login \

  -H "Content-Type: application/json" \

  -d '{"username":"panitia1","password":"secret"}'

```### Verifikasi Prerequisites## Persyaratan Deployment



Parameters:

- `username` (string): min 3, max 50

- `password` (string): min 4, max 200Jalankan command berikut untuk memastikan semua tools tersedia:Stack teknologi: FastAPI 0.115.6, Python 3.11, Docker, JWT Authentication (HS256), In-memory data store.---              ↓                              ↓



Response (200 OK):

```json

{```bash### Hardware & Software

  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",

  "token_type": "bearer"docker --version

}

```docker-compose --version



Save token untuk request berikutnya:git --version



```bash```- Docker dan Docker Compose v2.0 atau lebih baru

TOKEN=$(curl -s -X POST http://localhost:18081/auth/login \

  -H "Content-Type: application/json" \

  -d '{"username":"panitia1","password":"secret"}' | jq -r .access_token)

```## Panduan Deployment- Git untuk clone repository## Arsitektur Sistem    ┌──────────────────┐        ┌──────────────────┐



#### 4. Get Current User Info



**Endpoint:** `GET /auth/me`### Step 1: Clone Repository- Minimal 2GB RAM untuk menjalankan 2 containers



```bash

curl -H "Authorization: Bearer $TOKEN" http://localhost:18081/auth/me

``````bash- Minimal 500MB disk space



Response (200 OK):cd /home/user

```json

{git clone https://github.com/ratukhansaaaa/tixgo-microservices.git- Network: port 18081 dan 18082 harus accessible

  "username": "panitia1",

  "role": "committee"cd tixgo-microservices

}

`````````## Overview    │ Identity Service │        │Attendance Service│



### Attendance Service (Port 18082)



#### 1. Health Check### Step 2: Setup Environment Variables### Verifikasi Prerequisites



**Endpoint:** `GET /health`



```bashJangan commit `.env` ke repository. Buat file `.env` lokal dengan secrets yang aman.┌─────────────────────────────────────────────────────────────┐

curl http://localhost:18082/health

```



Response:```bash```bash

```json

{"status": "ok", "service": "attendance"}cp .env.example .env

```

nano .envdocker --version│                    Public Internet / STB                     │    │   (FastAPI)      │        │   (FastAPI)      │

#### 2. Create Check-in

```

**Endpoint:** `POST /checkins`

docker-compose --version

Requires Bearer token.

Isi `.env` dengan nilai yang diperlukan:

```bash

curl -X POST http://localhost:18082/checkins \git --version│             (Diakses via domain atau IP publik)             │

  -H "Content-Type: application/json" \

  -H "Authorization: Bearer $TOKEN" \```env

  -d '{"event_id":"evt1","ticket_id":"TICKET123"}'

```JWT_SECRET=<random-string-min-32-karakter>```



Parameters:JWT_ALG=HS256

- `event_id` (string): identitas event

- `ticket_id` (string): identitas ticket pesertaTOKEN_EXPIRE_MINUTES=120└──────────────────────────┬──────────────────────────────────┘**TixGo Microservices** terdiri dari dua layanan independen yang dirancang untuk menangani aspek berbeda dari sistem manajemen event:    │                  │        │                  │



Response (201 Created):```

```json

{## Panduan Deployment

  "status": "checked_in",

  "record": {Generate JWT_SECRET yang aman:

    "event_id": "evt1",

    "ticket_id": "TICKET123",                           │

    "checked_in_by": "panitia1",

    "checked_in_at": "2026-01-03T13:25:53.415880+00:00"```bash

  }

}# Menggunakan OpenSSL### Step 1: Clone Repository

```

openssl rand -hex 32

Error (400 - Duplicate):

```json            ┌──────────────┴──────────────┐    │ • Register       │        │ • Create Checkin │

{"detail": "Ticket sudah pernah check-in"}

```# Atau menggunakan Python



#### 3. Get Attendance by Eventpython3 -c "import secrets; print(secrets.token_hex(32))"```bash



**Endpoint:** `GET /attendance/{event_id}````



Requires Bearer token.cd /home/user            │                             │



```bash### Step 3: Build dan Deploy Services

curl -H "Authorization: Bearer $TOKEN" http://localhost:18082/attendance/evt1

```git clone https://github.com/ratukhansaaaa/tixgo-microservices.git



Response (200 OK):```bash

```json

{# Build imagescd tixgo-microservices       Port 18081                   Port 18082### 1. **Identity Service** (Port 18081)    │ • Login (JWT)    │        │ • Get Attendance │

  "event_id": "evt1",

  "total_checkins": 2,docker-compose build

  "records": [

    {```

      "ticket_id": "TICKET123",

      "checked_in_by": "panitia1",# Start services di background

      "checked_in_at": "2026-01-03T13:25:53.415880+00:00"

    },docker-compose -f docker-compose.prod.yml up -d            │                             │

    {

      "ticket_id": "TICKET456",

      "checked_in_by": "panitia1",

      "checked_in_at": "2026-01-03T13:26:20.123456+00:00"# Atau gunakan deploy script### Step 2: Setup Environment Variables

    }

  ]chmod +x deploy.sh

}

```./deploy.sh    ┌───────▼─────────────┐     ┌────────▼─────────────┐Menangani:    │ • /me endpoint   │        │ • Authorization  │



## Autentikasi dan Otorisasi```



### JWT Token FormatJangan commit `.env` ke repository. Buat file `.env` lokal dengan secrets yang aman.



Semua endpoint (kecuali `/health`, `/auth/register`, `/auth/login`) memerlukan Bearer token:### Step 4: Verifikasi Deployment



```    │ Identity Service    │     │ Attendance Service   │

Authorization: Bearer <access_token>

```Check container status:



Token adalah JWT yang di-sign dengan HS256. Payload berisi:```bash

- `sub` (subject): username user

- `role`: committee atau admin```bash

- `iat` (issued at): waktu token dibuat

- `exp` (expiration): waktu token kadaluarsadocker pscp .env.example .env    │                     │     │                      │- Registrasi user baru    └──────────────────┘        └──────────────────┘



### Token Lifetime```



Token berlaku 120 menit (2 jam). Setelah expired, user harus login ulang.nano .env



### Role-Based AccessExpected output:



Saat ini semua endpoint yang memerlukan autentikasi dapat diakses oleh user dengan role apapun (committee atau admin).```    │ • Register User     │     │ • Create Check-in    │



### Password Requirements```



- Minimum 4 karakterCONTAINER ID   IMAGE                     STATUS           PORTS

- Maximum 200 karakter (bcrypt limit 72 bytes)

- Di-hash dengan bcrypt (salt 12 rounds)xxxxx          tixgo-identity            Up 2 minutes     0.0.0.0:18081->8000/tcp



## Testingxxxxx          tixgo-attendance          Up 2 minutes     0.0.0.0:18082->8000/tcpIsi `.env` dengan nilai yang diperlukan:    │ • Login (JWT)       │     │ • Get Attendance     │- Login dan token generation (JWT)         8000/tcp                      8000/tcp



### Automated Testing (smoke-test.sh)```



Script untuk end-to-end testing:



```bashHealth check endpoints:

chmod +x smoke-test.sh

./smoke-test.sh```env    │ • Get User Info     │     │ • Verify JWT Token   │

```

```bash

Script akan:

1. Test health endpoints (Identity + Attendance)curl http://localhost:18081/healthJWT_SECRET=<random-string-min-32-karakter>

2. Register user baru

3. Login dan extract tokencurl http://localhost:18082/health

4. Test GET /auth/me

5. Create check-in```JWT_ALG=HS256    └─────────────────────┘     └──────────────────────┘- Verifikasi identitas user              ↓                              ↓

6. Get attendance data

7. Verify error handling



Expected: Semua test passed (7/7)Expected response:TOKEN_EXPIRE_MINUTES=120



### Manual Testing



Complete workflow:```json```           │                              │



```bash{"status": "ok", "service": "identity-service"}

# 1. Register user

curl -X POST http://localhost:18081/auth/register \{"status": "ok", "service": "attendance"}

  -H "Content-Type: application/json" \

  -d '{"username":"testuser","password":"password123","role":"committee"}'```



# 2. LoginGenerate JWT_SECRET yang aman:           │  FastAPI App                │  FastAPI App- Manajemen role (committee, admin)    ┌──────────────────┐        ┌──────────────────┐

curl -X POST http://localhost:18081/auth/login \

  -H "Content-Type: application/json" \## Cara Mengakses Layanan

  -d '{"username":"testuser","password":"password123"}'



# 3. Save token

TOKEN="<token-dari-login>"### A. Akses Lokal (Di STB)



# 4. Get user info```bash           │  (Container Port 8000)      │  (Container Port 8000)

curl -H "Authorization: Bearer $TOKEN" http://localhost:18081/auth/me

Jika test langsung di machine yang menjalankan Docker:

# 5. Create check-in

curl -X POST http://localhost:18082/checkins \# Menggunakan OpenSSL

  -H "Content-Type: application/json" \

  -H "Authorization: Bearer $TOKEN" \```bash

  -d '{"event_id":"evt1","ticket_id":"TICKET001"}'

# Identity Serviceopenssl rand -hex 32           │                              │    │   Container      │        │   Container      │

# 6. Get attendance

curl -H "Authorization: Bearer $TOKEN" http://localhost:18082/attendance/evt1curl http://localhost:18081/health

```

curl http://localhost:18081/auth/register

## Troubleshooting

curl http://localhost:18081/auth/login

### Port sudah digunakan

# Atau menggunakan Python    ┌──────▼─────────────┐     ┌────────▼──────────────┐

Error: `Ports are not available`

# Attendance Service

Solusi:

curl http://localhost:18082/healthpython3 -c "import secrets; print(secrets.token_hex(32))"

```bash

# Cek port yang digunakancurl http://localhost:18082/checkins

lsof -i :18081

lsof -i :18082``````    │  Docker Container   │     │  Docker Container    │### 2. **Attendance Service** (Port 18082)    │ (Python 3.11)    │        │ (Python 3.11)    │



# Kill process

kill -9 <PID>

### B. Akses via IP Address (Network)

# Atau ubah port di docker-compose.yml

```



### JWT_SECRET tidak ditemukanJika diakses dari machine lain di network yang sama, replace `<STB_IP>` dengan IP address STB:### Step 3: Build dan Deploy Services    │  (Python 3.11)      │     │  (Python 3.11)       │



Error: `KeyError: 'JWT_SECRET'`



Solusi:```bash



```bash# Identity Service

# Buat .env dari template

cp .env.example .envcurl http://<STB_IP>:18081/health```bash    └─────────────────────┘     └──────────────────────┘Menangani:    └──────────────────┘        └──────────────────┘



# Generate secret baru

openssl rand -hex 32

# Attendance Service# Build images

# Edit .env

nano .envcurl http://<STB_IP>:18082/health

```

```docker-compose build```

### Login gagal



Error: `Incorrect username or password`

### C. Akses via Domain Publik

Solusi:

1. Verifikasi username dan password benar (case-sensitive)

2. Pastikan user sudah di-register

3. Check Docker logs:Ketika domain publik sudah dikonfigurasi via reverse proxy atau Cloudflare Tunnel:# Start services di background- Check-in peserta ke event```



```bash

docker logs tixgo-identity

docker logs tixgo-attendance```bashdocker-compose -f docker-compose.prod.yml up -d

```

# Identity Service

### Token validation error

curl https://<identity-domain>/health## Persyaratan Deployment

Error: `Could not validate credentials`

curl https://<identity-domain>/auth/login

Solusi:

1. Pastikan token belum expired (valid 120 menit)# Atau gunakan deploy script

2. Verifikasi format header: `Bearer <token>`

3. Pastikan kedua services menggunakan JWT_SECRET yang sama# Attendance Service



### Check-in duplicate errorcurl https://<attendance-domain>/healthchmod +x deploy.sh- Pencatatan kehadiran per event



Error: `Ticket sudah pernah check-in`curl https://<attendance-domain>/checkins



Solusi:```./deploy.sh

1. Ini adalah expected behavior (prevent duplicate)

2. Gunakan ticket_id yang berbeda

3. Atau gunakan event_id yang berbeda

Domain mapping (sesuaikan dengan setup Anda):```### Hardware & Software

### Container tidak start



Error: `Error starting service`

- Identity Service: `<identity-domain>` → `<STB_IP>:18081`

Solusi:

- Attendance Service: `<attendance-domain>` → `<STB_IP>:18082`

```bash

# Check logs### Step 4: Verifikasi Deployment- Query data kehadiran dengan filter event## Deployment Files

docker-compose logs -f

## Dokumentasi API

# Verifikasi .env ada

cat .env



# Rebuild### Identity Service (Port 18081)

docker-compose down

docker-compose build --no-cacheCheck container status:- Docker dan Docker Compose v2.0 atau lebih baru

docker-compose up -d

```#### 1. Health Check



### Network connectivity issue



Jika tidak bisa akses via domain publik:**Endpoint:** `GET /health`



1. Verifikasi DNS pointing ke STB IP```bash- Git untuk clone repository- Validasi token dari Identity Service

2. Check firewall (port 18081, 18082 harus open)

3. Verifikasi Cloudflare Tunnel configAuthentication: Tidak diperlukan

4. Test DNS:

docker ps

```bash

nslookup <identity-domain>```bash

nslookup <attendance-domain>

```curl http://localhost:18081/health```- Minimal 2GB RAM untuk menjalankan 2 containers



### Memory usage tinggi```



Solusi:



```bashResponse (200 OK):

# Limit resources di docker-compose.prod.yml

services:Expected output:- Minimal 500MB disk space- `docker-compose.yml` — development compose file

  identity-service:

    deploy:```json

      resources:

        limits:{```

          memory: 512M

          cpus: '0.5'  "status": "ok",

```

  "service": "identity-service"CONTAINER ID   IMAGE                     STATUS           PORTS- Network: port 18081 dan 18082 harus accessible

```bash

# Restart containers}

docker-compose restart

``````xxxxx          tixgo-identity            Up 2 minutes     0.0.0.0:18081->8000/tcp



### Data hilang setelah restart



Ini adalah expected behavior (in-memory store). Untuk production, implementasikan database persistent (PostgreSQL, SQLite, MongoDB).#### 2. User Registrationxxxxx          tixgo-attendance          Up 2 minutes     0.0.0.0:18082->8000/tcp**Tech Stack:**- `docker-compose.prod.yml` — production-ready compose file with host ports mapped (18081/18082)



## Repository Structure



- `identity-service/app/main.py` — Identity service application**Endpoint:** `POST /auth/register````

- `attendance-service/app/main.py` — Attendance service application

- `docker-compose.yml` — Development compose file

- `docker-compose.prod.yml` — Production-ready compose file

- `deploy.sh` — Automated deployment scriptAuthentication: Tidak diperlukan### Verifikasi Prerequisites

- `smoke-test.sh` — Quick verification script

- `.env.example` — Environment variables template

- `.env` — Actual secrets (NOT tracked in git)

```bashHealth check endpoints:

## Repository Links

curl -X POST http://localhost:18081/auth/register \

GitHub: https://github.com/ratukhansaaaa/tixgo-microservices

  -H "Content-Type: application/json" \- FastAPI 0.115.6- `deploy.sh` — automated deployment script for STB

Untuk informasi lebih lanjut atau kontribusi, silakan fork repository dan create pull request.

  -d '{

    "username": "panitia1",```bash

    "password": "secret",

    "role": "committee"curl http://localhost:18081/health```bash

  }'

```curl http://localhost:18082/health



Request body parameters:```docker --version- Python 3.11- `smoke-test.sh` — quick verification/testing script



- `username` (string): min 3, max 50 karakter

- `password` (string): min 4, max 200 karakter

- `role` (string): `committee` atau `admin`Expected response:docker-compose --version



Response (200 OK):```json



```json{"status": "ok", "service": "identity-service"}git --version- Docker & Docker Compose- `cloudflared/config.yml.example` — example Cloudflare Tunnel config 

{

  "username": "panitia1",{"status": "ok", "service": "attendance"}

  "role": "committee"

}``````

```



Error (400 - User sudah ada):

## Cara Mengakses Layanan- JWT Authentication (HS256)- `.env.example` — environment variables template

```json

{

  "detail": "User panitia1 sudah terdaftar"

}### A. Akses Lokal (Di STB)## Panduan Deployment

```



#### 3. User Login

Jika test langsung di machine yang menjalankan Docker:- In-memory data store

**Endpoint:** `POST /auth/login`



Authentication: Tidak diperlukan

```bash### Step 1: Clone Repository

```bash

curl -X POST http://localhost:18081/auth/login \# Identity Service

  -H "Content-Type: application/json" \

  -d '{curl http://localhost:18081/health## API Endpoints Reference

    "username": "panitia1",

    "password": "secret"curl http://localhost:18081/auth/register

  }'

```curl http://localhost:18081/auth/login```bash



Request body parameters:



- `username` (string): min 3, max 50# Attendance Servicecd /home/user---

- `password` (string): min 4, max 200

curl http://localhost:18082/health

Response (200 OK):

curl http://localhost:18082/checkinsgit clone https://github.com/ratukhansaaaa/tixgo-microservices.git

```json

{```

  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",

  "token_type": "bearer"cd tixgo-microservices### Identity Service (Port 18081)

}

```### B. Akses via IP Address (Network)



Save token ke variable:```



```bashJika diakses dari machine lain di network yang sama:

TOKEN=$(curl -s -X POST http://localhost:18081/auth/login \

  -H "Content-Type: application/json" \## Arsitektur Sistem

  -d '{"username":"panitia1","password":"secret"}' | jq -r .access_token)

```bash

echo $TOKEN

```# Replace <STB_IP> dengan IP address STB### Step 2: Setup Environment Variables



#### 4. Get Current User Infocurl http://192.168.1.100:18081/health



**Endpoint:** `GET /auth/me`curl http://192.168.1.100:18082/health#### 1. Health Check



Authentication: Bearer Token Required```



```bashJangan commit `.env` ke repository. Buat file `.env` lokal dengan secrets yang aman.

curl -H "Authorization: Bearer $TOKEN" \

  http://localhost:18081/auth/me### C. Akses via Domain Publik

```

``````http

Response (200 OK):

Ketika domain publik sudah dikonfigurasi via reverse proxy atau Cloudflare Tunnel:

```json

{```bash

  "username": "panitia1",

  "role": "committee"```bash

}

```# Identity Servicecp .env.example .env┌─────────────────────────────────────────────────────────────────┐GET /health



Error (401 - Unauthorized):curl https://<identity-domain>/health



```jsoncurl https://<identity-domain>/auth/loginnano .env

{

  "detail": "Could not validate credentials"

}

```# Attendance Service```│                    Public Internet / STB                         │```



### Attendance Service (Port 18082)curl https://<attendance-domain>/health



#### 1. Health Checkcurl https://<attendance-domain>/checkins



**Endpoint:** `GET /health````



Authentication: Tidak diperlukanIsi `.env` dengan nilai yang diperlukan:│             (Diakses via domain atau IP publik)                 │**Response:** `200 OK`



```bashDomain mapping (sesuaikan dengan setup Anda):

curl http://localhost:18082/health

```- Identity Service: `<identity-domain>` → `STB_IP:18081`



Response (200 OK):- Attendance Service: `<attendance-domain>` → `STB_IP:18082`



```json```env└──────────────────────────┬──────────────────────────────────────┘```json

{

  "status": "ok",## Dokumentasi API

  "service": "attendance"

}JWT_SECRET=<random-string-min-32-karakter>

```

### Identity Service (Port 18081)

#### 2. Create Check-in

JWT_ALG=HS256                           │{

**Endpoint:** `POST /checkins`

#### 1. Health Check

Authentication: Bearer Token Required

TOKEN_EXPIRE_MINUTES=120

```bash

curl -X POST http://localhost:18082/checkins \**Endpoint:** `GET /health`

  -H "Content-Type: application/json" \

  -H "Authorization: Bearer $TOKEN" \```            ┌──────────────┴──────────────┐  "status": "ok",

  -d '{

    "event_id": "evt1",Authentication: Tidak diperlukan

    "ticket_id": "TICKET123"

  }'

```

Response (200 OK):

Request body parameters:

```jsonGenerate JWT_SECRET yang aman:            │                             │  "service": "identity-service"

- `event_id` (string): identitas event

- `ticket_id` (string): identitas ticket peserta{



Response (201 Created):  "status": "ok",



```json  "service": "identity-service"

{

  "status": "checked_in",}```bash       Port 18081                   Port 18082}

  "record": {

    "event_id": "evt1",```

    "ticket_id": "TICKET123",

    "checked_in_by": "panitia1",# Menggunakan OpenSSL

    "checked_in_at": "2026-01-03T13:25:53.415880+00:00"

  }#### 2. User Registration

}

```openssl rand -hex 32            │                             │```



Error (400 - Duplicate check-in):**Endpoint:** `POST /auth/register`



```json

{

  "detail": "Ticket sudah pernah check-in"Authentication: Tidak diperlukan

}

```# Atau menggunakan Python    ┌───────▼─────────────┐     ┌────────▼─────────────┐



Error (401 - Unauthorized):Request body:



```json```jsonpython3 -c "import secrets; print(secrets.token_hex(32))"

{

  "detail": "Could not validate credentials"{

}

```  "username": "string (min 3, max 50 karakter)",```    │ Identity Service    │     │ Attendance Service   │#### 2. User Registration



#### 3. Get Attendance by Event  "password": "string (min 4, max 200 karakter)",



**Endpoint:** `GET /attendance/{event_id}`  "role": "string (committee|admin)"



Authentication: Bearer Token Required}



```bash```### Step 3: Build dan Deploy Services    │ (dina.*.my.id)      │     │ (ratu.*.my.id)       │```http

curl -H "Authorization: Bearer $TOKEN" \

  http://localhost:18082/attendance/evt1

```

Response (200 OK):

Response (200 OK):

```json

```json

{{```bash    │                     │     │                      │POST /auth/register

  "event_id": "evt1",

  "total_checkins": 2,  "username": "panitia1",

  "records": [

    {  "role": "committee"# Build images

      "ticket_id": "TICKET123",

      "checked_in_by": "panitia1",}

      "checked_in_at": "2026-01-03T13:25:53.415880+00:00"

    },```docker-compose build    │ • Register User     │     │ • Create Check-in    │Content-Type: application/json

    {

      "ticket_id": "TICKET456",

      "checked_in_by": "panitia1",

      "checked_in_at": "2026-01-03T13:26:20.123456+00:00"Error (400 - User sudah ada):

    }

  ]```json

}

```{# Start services di background    │ • Login (JWT)       │     │ • Get Attendance     │



Error (401 - Unauthorized):  "detail": "User panitia1 sudah terdaftar"



```json}docker-compose -f docker-compose.prod.yml up -d

{

  "detail": "Could not validate credentials"```

}

```    │ • Get User Info     │     │ • Verify JWT Token   │{



## Autentikasi dan Otorisasi#### 3. User Login



### JWT Token Format# Atau gunakan deploy script



Semua API endpoint (kecuali `/health`, `/auth/register`, `/auth/login`) memerlukan Bearer token di header:**Endpoint:** `POST /auth/login`



```chmod +x deploy.sh    │                     │     │                      │  "username": "string (min 3, max 50)",

Authorization: Bearer <access_token>

```Authentication: Tidak diperlukan



Token adalah JWT yang di-sign dengan HS256 algorithm. Payload token berisi informasi:./deploy.sh



- `sub` (subject): username userRequest body:

- `role`: committee atau admin

- `iat` (issued at): timestamp token dibuat```json```    └─────────────────────┘     └──────────────────────┘  "password": "string (min 4, max 200 bytes)",

- `exp` (expiration): timestamp token expired

{

### Token Expiration

  "username": "panitia1",

Token memiliki masa berlaku 120 menit (2 jam) dari waktu dibuat. Setelah expired, user harus login kembali untuk mendapatkan token baru.

  "password": "secret"

### Role-Based Access Control

}### Step 4: Verifikasi Deployment           │                              │  "role": "string (committee|admin)"

Saat ini, semua endpoint yang memerlukan autentikasi dapat diakses oleh user dengan role apapun (committee atau admin). Implementasi role-based authorization untuk endpoint tertentu dapat ditambahkan di fase development berikutnya.

```

### Password Requirements



Password harus memenuhi kriteria berikut:

Response (200 OK):

- Minimum 4 karakter

- Maximum 200 karakter (bcrypt limit 72 bytes)```jsonCheck container status:           │  FastAPI App                │  FastAPI App}

- Disimpan dengan hash bcrypt (salt 12 rounds)

{

## Testing

  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",

### Automated Testing (smoke-test.sh)

  "token_type": "bearer"

Script ini melakukan end-to-end testing untuk memastikan semua endpoint berfungsi dengan baik:

}```bash           │  (Container Port 8000)      │  (Container Port 8000)```

```bash

chmod +x smoke-test.sh```

./smoke-test.sh

```docker ps



Script akan melakukan:Curl example:



1. Test health endpoints (Identity + Attendance)```bash```           │                              │**Response:** `200 OK`

2. Register user baru

3. Login dan extract tokenTOKEN=$(curl -s -X POST http://localhost:18081/auth/login \

4. Test GET /auth/me

5. Create check-in  -H "Content-Type: application/json" \

6. Get attendance data

7. Verify error handling (unauthorized, duplicate check-in)  -d '{"username":"panitia1","password":"secret"}' | jq -r .access_token)



Expected output: Semua assertions passed (7/7)```Expected output:    ┌──────▼─────────────┐     ┌────────▼──────────────┐```json



### Manual Testing



Test dengan curl atau tools serupa:#### 4. Get Current User Info```



```bash

# 1. Register user

curl -X POST http://localhost:18081/auth/register \**Endpoint:** `GET /auth/me`CONTAINER ID   IMAGE                     STATUS           PORTS    │  Docker Container   │     │  Docker Container    │{

  -H "Content-Type: application/json" \

  -d '{"username":"testuser","password":"password123","role":"committee"}'



# 2. LoginAuthentication: Bearer Token Requiredxxxxx          tixgo-identity            Up 2 minutes     0.0.0.0:18081->8000/tcp

curl -X POST http://localhost:18081/auth/login \

  -H "Content-Type: application/json" \

  -d '{"username":"testuser","password":"password123"}'

Request header:xxxxx          tixgo-attendance          Up 2 minutes     0.0.0.0:18082->8000/tcp    │  (Python 3.11)      │     │  (Python 3.11)       │  "username": "panitia1",

# 3. Save token

TOKEN="<token-dari-response-login>"```



# 4. Get user infoAuthorization: Bearer <access_token>```

curl -H "Authorization: Bearer $TOKEN" \

  http://localhost:18081/auth/me```



# 5. Create check-in    │  tixgo-identity     │     │  tixgo-attendance    │  "role": "committee"

curl -X POST http://localhost:18082/checkins \

  -H "Content-Type: application/json" \Response (200 OK):

  -H "Authorization: Bearer $TOKEN" \

  -d '{"event_id":"evt1","ticket_id":"TICKET001"}'```jsonHealth check endpoints:



# 6. Get attendance{

curl -H "Authorization: Bearer $TOKEN" \

  http://localhost:18082/attendance/evt1  "username": "panitia1",    └─────────────────────┘     └──────────────────────┘}

```

  "role": "committee"

## Troubleshooting

}```bash

### Port sudah digunakan (Address already in use)

```

Error: `docker-compose: Error response from daemon: Ports are not available`

curl http://localhost:18081/health``````

Solusi:

Curl example:

```bash

# Cek port yang sedang digunakan```bashcurl http://localhost:18082/health

lsof -i :18081

lsof -i :18082curl -H "Authorization: Bearer $TOKEN" \



# Kill process yang menggunakan port  http://localhost:18081/auth/me```

kill -9 <PID>

```

# Atau ubah port di docker-compose.yml

# Ganti "18081:8000" menjadi "18083:8000" (gunakan port yang available)

```

### Attendance Service (Port 18082)

### JWT_SECRET tidak ditemukan

Expected response:---#### 3. User Login

Error: `KeyError: 'JWT_SECRET'`

#### 1. Health Check

Solusi:

```json

```bash

# Pastikan .env file ada dan berisi JWT_SECRET**Endpoint:** `GET /health`

cat .env

{"status": "ok", "service": "identity-service"}```http

# Jika belum ada, buat dari .env.example

cp .env.example .envAuthentication: Tidak diperlukan



# Generate JWT_SECRET baru{"status": "ok", "service": "attendance"}

openssl rand -hex 32

Response (200 OK):

# Update .env dengan JWT_SECRET

nano .env```json```## Persyaratan DeploymentPOST /auth/login

```

{

### Login gagal (Invalid credentials)

  "status": "ok",

Error: `detail: "Incorrect username or password"`

  "service": "attendance"

Solusi:

}## Cara Mengakses LayananContent-Type: application/json

1. Verifikasi username dan password sudah benar (case-sensitive)

2. Pastikan user sudah di-register terlebih dahulu```

3. Check Docker logs:



```bash

docker logs tixgo-identity#### 2. Create Check-in

docker logs tixgo-attendance

```### A. Akses Lokal (Di STB)### Hardware & Software



### Token validation error**Endpoint:** `POST /checkins`



Error: `detail: "Could not validate credentials"` pada endpoint Attendance Service



Solusi:Authentication: Bearer Token Required



1. Pastikan token masih berlaku (expired setelah 120 menit)Jika test langsung di machine yang menjalankan Docker:- **Docker & Docker Compose**: v2.0 atau lebih baru{

2. Verifikasi Authorization header format: `Bearer <token>`

3. Pastikan kedua services menggunakan JWT_SECRET yang sama di `.env`Request header:



### Check-in duplicate error```



Error: `detail: "Ticket sudah pernah check-in"`Authorization: Bearer <access_token>



Solusi:Content-Type: application/json```bash- **Git**: untuk clone repository  "username": "panitia1",



1. Ini adalah expected behavior (duplicate prevention)```

2. Gunakan ticket_id yang berbeda untuk check-in baru

3. Atau gunakan event_id yang berbeda# Identity Service



### Container tidak startRequest body:



Error: `docker-compose: Error starting service````jsoncurl http://localhost:18081/health- **Memory**: minimal 2GB RAM  "password": "secret"



Solusi:{



1. Check Docker logs:  "event_id": "evt1",curl http://localhost:18081/auth/register



```bash  "ticket_id": "TICKET123"

docker-compose logs -f

```}curl http://localhost:18081/auth/login- **Disk Space**: minimal 500MB (untuk image + containers)}



2. Verifikasi `.env` file sudah ada dan valid:```



```bash

cat .env

# Pastikan JWT_SECRET tidak kosongResponse (201 Created):

```

```json# Attendance Service- **Network**: port 18081 dan 18082 harus accessible```

3. Rebuild images:

{

```bash

docker-compose down  "status": "checked_in",curl http://localhost:18082/health

docker-compose build --no-cache

docker-compose up -d  "record": {

```

    "event_id": "evt1",curl http://localhost:18082/checkins**Response:** `200 OK`

### Network connectivity (STB ke domain publik)

    "ticket_id": "TICKET123",

Jika tidak bisa akses via domain publik meskipun services running:

    "checked_in_by": "panitia1",```

1. Verifikasi domain DNS pointing ke STB IP

2. Check firewall rules (port 18081, 18082 harus open)    "checked_in_at": "2026-01-03T13:25:53.415880+00:00"

3. Verifikasi Cloudflare Tunnel configuration (jika digunakan)

4. Test DNS resolution:  }### Pre-requisites```json



```bash}

nslookup <identity-domain>

nslookup <attendance-domain>```### B. Akses via IP Address (Network)

```



### Memory atau CPU usage tinggi

Curl example:```bash{

Solusi:

```bash

1. Limit resource di docker-compose.prod.yml:

curl -X POST http://localhost:18082/checkins \Jika diakses dari machine lain di network yang sama:

```yaml

services:  -H "Content-Type: application/json" \

  identity-service:

    deploy:  -H "Authorization: Bearer $TOKEN" \# Verify Docker installed  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",

      resources:

        limits:  -d '{"event_id":"evt1","ticket_id":"TICKET123"}'

          memory: 512M

          cpus: '0.5'``````bash

```



2. Restart containers:

Error (400 - Duplicate check-in):# Replace <STB_IP> dengan IP address STBdocker --version  "token_type": "bearer"

```bash

docker-compose restart```json

```

{curl http://192.168.1.100:18081/health

### Data tidak tersimpan setelah restart

  "detail": "Ticket sudah pernah check-in"

Ini adalah expected behavior (in-memory store). Data akan hilang setelah container di-restart.

}curl http://192.168.1.100:18082/healthdocker-compose --version}

Untuk production, implementasikan database persistent:

```

- PostgreSQL

- SQLite dengan mounted volume```

- MongoDB

#### 3. Get Attendance by Event

## Repository Structure

```

Setiap folder dalam repository memiliki fungsi spesifik:

**Endpoint:** `GET /attendance/{event_id}`

- `identity-service/app/main.py` — Identity service application

- `attendance-service/app/main.py` — Attendance service application### C. Akses via Domain Publik

- `docker-compose.yml` — Development compose file

- `docker-compose.prod.yml` — Production-ready compose fileAuthentication: Bearer Token Required

- `deploy.sh` — Automated deployment script for STB

- `smoke-test.sh` — Quick verification/testing script# Verify Git installed

- `.env.example` — Environment variables template

- `.env` — Actual secrets (NOT tracked in git)Request header:



## Repository Links```Backend Team (BT) melakukan routing via Cloudflare Tunnel atau reverse proxy:



GitHub: https://github.com/ratukhansaaaa/tixgo-microservicesAuthorization: Bearer <access_token>



Untuk informasi lebih lanjut atau kontribusi, silakan fork repository dan create pull request.```git --version#### 4. Get Current User Info




Response (200 OK):```bash

```json

{# Identity Service``````http

  "event_id": "evt1",

  "total_checked_in": 1,curl https://dina.theokaitou.my.id/health

  "records": [

    {curl https://dina.theokaitou.my.id/auth/loginGET /auth/me

      "event_id": "evt1",

      "ticket_id": "TICKET123",

      "checked_in_by": "panitia1",

      "checked_in_at": "2026-01-03T13:25:53.415880+00:00"# Attendance Service---Authorization: Bearer <TOKEN>

    }

  ]curl https://ratu.theokaitou.my.id/health

}

```curl https://ratu.theokaitou.my.id/checkins```



Curl example:```

```bash

curl -H "Authorization: Bearer $TOKEN" \## Panduan Deployment di STB**Response:** `200 OK`

  http://localhost:18082/attendance/evt1

```Domain mapping:



## Autentikasi dan Otorisasi- Identity Service: `dina.theokaitou.my.id` → `STB_IP:18081````json



### JWT Token Format- Attendance Service: `ratu.theokaitou.my.id` → `STB_IP:18082`



Tokens adalah JWT (JSON Web Token) yang di-sign dengan algoritma HS256.### Step 1: Clone Repository{



Struktur token:## Dokumentasi API

```

Header.Payload.Signature```bash  "username": "panitia1",

```

### Identity Service (Port 18081)

Payload (decoded):

```jsoncd /home/user  "role": "committee"

{

  "sub": "panitia1",#### 1. Health Check

  "role": "committee",

  "iat": 1767446742,git clone https://github.com/ratukhansaaaa/tixgo-microservices.git}

  "exp": 1767453942

}**Endpoint:** `GET /health`

```

cd tixgo-microservices```

Token lifetime: 120 menit (default)

Authentication: Tidak diperlukan

### Authorization Requirements

```

| Endpoint | Method | Auth Required | Deskripsi |

|----------|--------|---------------|-----------|Response (200 OK):

| `/health` (both) | GET | Tidak | Health check publik |

| `/auth/register` | POST | Tidak | Registrasi user baru |```json### Attendance Service (Port 18082)

| `/auth/login` | POST | Tidak | Login untuk dapat token |

| `/auth/me` | GET | Ya | Lihat info user sendiri |{

| `/checkins` | POST | Ya | Buat check-in baru |

| `/attendance/{id}` | GET | Ya | Lihat data kehadiran |  "status": "ok",### Step 2: Setup Environment Variables



### Security Notes  "service": "identity-service"



1. JWT_SECRET Management}#### 1. Health Check

   - Generate dengan `openssl rand -hex 32`

   - Simpan di `.env` - jangan commit ke git```

   - Gunakan secret yang berbeda untuk development dan production

   - Rotate secret secara berkala**PENTING:** Jangan commit `.env` ke repository. Buat file `.env` lokal dengan secrets yang aman.```http



2. Password Security#### 2. User Registration

   - Password di-hash menggunakan bcrypt

   - Panjang password: 4-200 karakterGET /health

   - Password > 72 bytes akan ditolak (bcrypt limit)

**Endpoint:** `POST /auth/register`

3. Token Security

   - Token hanya valid 120 menit```bash```

   - Token disimpan di client, bukan di server

   - Gunakan HTTPS untuk transmit tokenAuthentication: Tidak diperlukan

   - Jangan expose token di URL atau logs

# Copy template**Response:** `200 OK`

## Testing

Request body:

### Automated Testing

```jsoncp .env.example .env```json

Smoke test script:

{

```bash

chmod +x smoke-test.sh  "username": "string (min 3, max 50 karakter)",{

./smoke-test.sh http://localhost:18081 http://localhost:18082

```  "password": "string (min 4, max 200 karakter)",



Script ini melakukan:  "role": "string (committee|admin)"# Edit dengan editor pilihan  "status": "ok",

1. Check health endpoints

2. Register user baru}

3. Login dan dapatkan token

4. Buat check-in baru```nano .env  "service": "attendance"

5. Fetch attendance data

6. Report hasil test



Testing via public domain:Response (200 OK):```}



```bash```json

./smoke-test.sh https://<identity-domain> https://<attendance-domain>

```{```



### Manual Testing Flow  "username": "panitia1",



Complete workflow test:  "role": "committee"**Isi `.env` (REQUIRED):**



```bash}

# 1. Register user baru

curl -X POST http://localhost:18081/auth/register \``````env#### 2. Create Check-in

  -H "Content-Type: application/json" \

  -d '{

    "username": "testuser",

    "password": "testpass123",Error (400 - User sudah ada):JWT_SECRET=<random-string-32-karakter-atau-lebih>```http

    "role": "committee"

  }'```json



# 2. Login dan simpan token{JWT_ALG=HS256POST /checkins

TOKEN=$(curl -s -X POST http://localhost:18081/auth/login \

  -H "Content-Type: application/json" \  "detail": "User panitia1 sudah terdaftar"

  -d '{

    "username": "testuser",}TOKEN_EXPIRE_MINUTES=120Content-Type: application/json

    "password": "testpass123"

  }' | jq -r .access_token)```



# 3. Verify token dengan /me endpoint```Authorization: Bearer <TOKEN>

curl -H "Authorization: Bearer $TOKEN" \

  http://localhost:18081/auth/me#### 3. User Login



# 4. Create check-in

curl -X POST http://localhost:18082/checkins \

  -H "Content-Type: application/json" \**Endpoint:** `POST /auth/login`

  -H "Authorization: Bearer $TOKEN" \

  -d '{"event_id":"konsert_2026","ticket_id":"TKT-001"}'**Generate JWT_SECRET yang aman:**{



# 5. Get attendance for eventAuthentication: Tidak diperlukan

curl -H "Authorization: Bearer $TOKEN" \

  http://localhost:18082/attendance/konsert_2026```bash  "event_id": "evt1",

```

Request body:

## Troubleshooting

```json# Menggunakan OpenSSL  "ticket_id": "TICKET123"

### Containers tidak running

{

Diagnosis:

```bash  "username": "panitia1",openssl rand -hex 32}

docker-compose logs identity-service

docker-compose logs attendance-service  "password": "secret"

docker ps

```}```



Solution:```

```bash

docker-compose build# ATAU menggunakan Python**Response:** `201 Created`

docker-compose up

```Response (200 OK):



### Port sudah digunakan```jsonpython3 -c "import secrets; print(secrets.token_hex(32))"```json



Check process:{

```bash

lsof -i :18081  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",```{

lsof -i :18082

```  "token_type": "bearer"



Kill process:}  "status": "checked_in",

```bash

lsof -ti:18081 | xargs kill -9```

lsof -ti:18082 | xargs kill -9

```**Contoh `.env` yang valid:**  "record": {



### JWT_SECRET error atau token tidak validCurl example:



Check .env file:```bash```env    "event_id": "evt1",

```bash

cat .envTOKEN=$(curl -s -X POST http://localhost:18081/auth/login \

```

  -H "Content-Type: application/json" \JWT_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6    "ticket_id": "TICKET123",

Pastikan:

1. JWT_SECRET tidak kosong  -d '{"username":"panitia1","password":"secret"}' | jq -r .access_token)

2. JWT_SECRET sama di semua services

3. Min 32 karakter untuk security```JWT_ALG=HS256    "checked_in_by": "panitia1",



Restart services:

```bash

docker-compose restart#### 4. Get Current User InfoTOKEN_EXPIRE_MINUTES=120    "checked_in_at": "2026-01-03T13:25:53.415880+00:00"

```



### Token expired error

**Endpoint:** `GET /auth/me````  }

Token sudah kadaluarsa (> 120 menit). Login ulang:



```bash

TOKEN=$(curl -s -X POST http://localhost:18081/auth/login \Authentication: Bearer Token Required}

  -H "Content-Type: application/json" \

  -d '{"username":"panitia1","password":"secret"}' | jq -r .access_token)

```

Request header:### Step 3: Build & Deploy Services```

### Ticket sudah pernah check-in

```

Ticket ID harus unik per event. Gunakan ticket_id yang berbeda:

Authorization: Bearer <access_token>```bash**Error (duplicate):** `400 Bad Request`

```bash

curl -X POST http://localhost:18082/checkins \```

  -H "Content-Type: application/json" \

  -H "Authorization: Bearer $TOKEN" \# Build images (jika belum ada)```json

  -d '{"event_id":"evt1","ticket_id":"TKT-UNIQUE-002"}'

```Response (200 OK):



### 401 Unauthorized error```jsondocker-compose build{



Authorization header format harus: `"Bearer <token>"`{



Benar:  "username": "panitia1",  "detail": "Ticket sudah pernah check-in"

```bash

curl -H "Authorization: Bearer $TOKEN" http://localhost:18082/checkins  "role": "committee"

```

}# Start services di background}

### View Logs

```

```bash

docker-compose logs identity-service -fdocker-compose -f docker-compose.prod.yml up -d```

docker-compose logs attendance-service -f

docker-compose logs -fCurl example:

docker-compose logs --tail=50

``````bash



## Struktur Projectcurl -H "Authorization: Bearer $TOKEN" \



```  http://localhost:18081/auth/me# Atau gunakan deploy script#### 3. Get Attendance by Event

tixgo-microservices/

├── identity-service/```

│   ├── app/

│   │   └── main.py              # Identity service implementationchmod +x deploy.sh```http

│   ├── Dockerfile

│   └── requirements.txt### Attendance Service (Port 18082)

├── attendance-service/

│   ├── app/./deploy.shGET /attendance/{event_id}

│   │   └── main.py              # Attendance service implementation

│   ├── Dockerfile#### 1. Health Check

│   └── requirements.txt

├── cloudflared/```Authorization: Bearer <TOKEN>

│   └── config.yml.example

├── docker-compose.yml**Endpoint:** `GET /health`

├── docker-compose.prod.yml

├── deploy.sh```

├── smoke-test.sh

├── .env.exampleAuthentication: Tidak diperlukan

├── .gitignore

├── README.md### Step 4: Verifikasi Deployment**Response:** `200 OK`

└── README.pdf

```Response (200 OK):



## Notes```json```json



### Data Persistence{



Saat ini data disimpan in-memory. Data akan hilang saat container restart.  "status": "ok",**Check container status:**{



Untuk production: gunakan database seperti PostgreSQL atau SQLite.  "service": "attendance"



### Future Improvements}```bash  "event_id": "evt1",



1. Event Management Service```

2. Database Persistence (PostgreSQL/SQLite)

3. Rate limiting & throttlingdocker ps  "total_checked_in": 1,

4. API logging & monitoring

5. CI/CD pipeline (GitHub Actions)#### 2. Create Check-in



## References```  "records": [



- FastAPI Documentation: https://fastapi.tiangolo.com**Endpoint:** `POST /checkins`

- Docker Documentation: https://docs.docker.com

- JWT Specification: https://tools.ietf.org/html/rfc7519    {



---Authentication: Bearer Token Required



**Version:** 1.0.0Expected output:      "event_id": "evt1",

**Status:** Production Ready for Tugas 2

Request header:

``````      "ticket_id": "TICKET123",

Authorization: Bearer <access_token>

Content-Type: application/jsonCONTAINER ID   IMAGE                     STATUS           PORTS      "checked_in_by": "panitia1",

```

xxxxx          tixgo-identity            Up 2 minutes     0.0.0.0:18081->8000/tcp      "checked_in_at": "2026-01-03T13:25:53.415880+00:00"

Request body:

```jsonxxxxx          tixgo-attendance          Up 2 minutes     0.0.0.0:18082->8000/tcp    }

{

  "event_id": "evt1",```  ]

  "ticket_id": "TICKET123"

}}

```

**Health check endpoints:**```

Response (201 Created):

```json```bash

{

  "status": "checked_in",# Identity Service## Authentication & Authorization

  "record": {

    "event_id": "evt1",curl http://localhost:18081/health

    "ticket_id": "TICKET123",

    "checked_in_by": "panitia1",### JWT Token Format

    "checked_in_at": "2026-01-03T13:25:53.415880+00:00"

  }# Attendance ServiceTokens are signed with **HS256** and contain:

}

```curl http://localhost:18082/health```json



Curl example:```{

```bash

curl -X POST http://localhost:18082/checkins \  "sub": "username",

  -H "Content-Type: application/json" \

  -H "Authorization: Bearer $TOKEN" \Expected response:  "role": "committee|admin",

  -d '{"event_id":"evt1","ticket_id":"TICKET123"}'

``````json  "iat": 1234567890,



Error (400 - Duplicate check-in):{"status": "ok", "service": "identity-service"}  "exp": 1234671490

```json

{{"status": "ok", "service": "attendance"}}

  "detail": "Ticket sudah pernah check-in"

}``````

```



#### 3. Get Attendance by Event

---### Authorization Requirements

**Endpoint:** `GET /attendance/{event_id}`

| Endpoint | Method | Auth Required | Roles |

Authentication: Bearer Token Required

## Cara Mengakses Layanan|----------|--------|---------------|-------|

Request header:

```| `/health` (both) | GET | ❌ | - |

Authorization: Bearer <access_token>

```### A. Akses Lokal (Di STB)| `/auth/register` | POST | ❌ | - |



Response (200 OK):| `/auth/login` | POST | ❌ | - |

```json

{Jika kamu test langsung di machine yang menjalankan Docker:| `/auth/me` | GET | ✅ | any |

  "event_id": "evt1",

  "total_checked_in": 1,| `/checkins` | POST | ✅ | any |

  "records": [

    {```bash| `/attendance/{event_id}` | GET | ✅ | any |

      "event_id": "evt1",

      "ticket_id": "TICKET123",# Identity Service

      "checked_in_by": "panitia1",

      "checked_in_at": "2026-01-03T13:25:53.415880+00:00"curl http://localhost:18081/health### Error Responses

    }

  ]curl http://localhost:18081/auth/register- **401 Unauthorized**: Missing or invalid token

}

```curl http://localhost:18081/auth/login  ```json



Curl example:  {"detail": "Missing Authorization header"}

```bash

curl -H "Authorization: Bearer $TOKEN" \# Attendance Service  {"detail": "Token expired"}

  http://localhost:18082/attendance/evt1

```curl http://localhost:18082/health  {"detail": "Invalid token"}



## Autentikasi dan Otorisasicurl http://localhost:18082/checkins  ```



### JWT Token Format```- **400 Bad Request**: Invalid input or duplicate check-in



Tokens adalah JWT (JSON Web Token) yang di-sign dengan algoritma HS256.  ```json



Struktur token:### B. Akses via IP Address (Network)  {"detail": "Ticket sudah pernah check-in"}

```

Header.Payload.Signature  ```

```

Jika diakses dari machine lain di network yang sama:

Payload (decoded):

```json## Important Notes for Deployment

{

  "sub": "panitia1",```bash

  "role": "committee",

  "iat": 1767446742,# Replace <STB_IP> dengan IP address STB## Important Notes for Deployment

  "exp": 1767453942

}# Contoh: 192.168.1.100

```

### 1. Environment Configuration

Token lifetime: 120 menit (default)

curl http://192.168.1.100:18081/health**Do NOT commit your real `.env` into git.** Create a `.env` file on the STB with production secrets:

### Authorization Requirements

curl http://192.168.1.100:18082/health

| Endpoint | Method | Auth Required | Deskripsi |

|----------|--------|---------------|-----------|``````env

| `/health` (both) | GET | Tidak | Health check publik |

| `/auth/register` | POST | Tidak | Registrasi user baru |JWT_SECRET=<long-random-hex-string-min-32-chars>

| `/auth/login` | POST | Tidak | Login untuk dapat token |

| `/auth/me` | GET | Ya | Lihat info user sendiri |### C. Akses via Domain Publik (Recommended)JWT_ALG=HS256

| `/checkins` | POST | Ya | Buat check-in baru |

| `/attendance/{id}` | GET | Ya | Lihat data kehadiran |TOKEN_EXPIRE_MINUTES=120



### Security Notes**Backend Team (BT)** akan melakukan routing via Cloudflare Tunnel atau reverse proxy:```



1. JWT_SECRET Management

   - Generate dengan `openssl rand -hex 32`

   - Simpan di `.env` - jangan commit ke git```bashGenerate a secure JWT_SECRET:

   - Gunakan secret yang berbeda untuk development dan production

   - Rotate secret secara berkala# Identity Service```bash



2. Password Securitycurl https://dina.theokaitou.my.id/health# Using OpenSSL

   - Password di-hash menggunakan bcrypt

   - Panjang password: 4-200 karaktercurl https://dina.theokaitou.my.id/auth/loginopenssl rand -hex 32

   - Password > 72 bytes akan ditolak (bcrypt limit)



3. Token Security

   - Token hanya valid 120 menit# Attendance Service# Using Python

   - Token disimpan di client, bukan di server

   - Gunakan HTTPS untuk transmit tokencurl https://ratu.theokaitou.my.id/healthpython3 -c "import secrets; print(secrets.token_hex(32))"

   - Jangan expose token di URL atau logs

curl https://ratu.theokaitou.my.id/checkins```

## Testing

```

### Automated Testing

### 2. Port Mapping

Smoke test script:

**Domain Mapping:**Services are mapped to host ports for easy routing :

```bash

chmod +x smoke-test.sh- Identity Service: `dina.theokaitou.my.id` → `STB_IP:18081`- **Identity Service**: Container port 8000 → Host port 18081

./smoke-test.sh http://localhost:18081 http://localhost:18082

```- Attendance Service: `ratu.theokaitou.my.id` → `STB_IP:18082`- **Attendance Service**: Container port 8000 → Host port 18082



Script ini melakukan:

1. Check health endpoints

2. Register user baru---can then route:

3. Login dan dapatkan token

4. Buat check-in baru- `dina.theokaitou.my.id` → `STB_IP:18081` (identity)

5. Fetch attendance data

6. Report hasil test## Dokumentasi API- `ratu.theokaitou.my.id` → `STB_IP:18082` (attendance)



Testing via public domain:



```bash### Identity Service (Port 18081)### 3. Deployment Steps on STB

./smoke-test.sh https://dina.theokaitou.my.id https://ratu.theokaitou.my.id

```



### Manual Testing Flow#### 1. Health Check**Prerequisites:**



Complete workflow test:**Endpoint:** `GET /health`- Docker & Docker Compose installed



```bash- Git repository cloned

# 1. Register user baru

curl -X POST http://localhost:18081/auth/register \**Authentication:** ❌ Tidak diperlukan- `.env` file with production secrets ready

  -H "Content-Type: application/json" \

  -d '{

    "username": "testuser",

    "password": "testpass123",**Response (200 OK):****Deploy:**

    "role": "committee"

  }'```json```bash



# 2. Login dan simpan token{# Copy production .env to STB

TOKEN=$(curl -s -X POST http://localhost:18081/auth/login \

  -H "Content-Type: application/json" \  "status": "ok",scp .env user@stb:/home/user/tixgo-microservices/.env

  -d '{

    "username": "testuser",  "service": "identity-service"

    "password": "testpass123"

  }' | jq -r .access_token)}# SSH into STB and deploy



# 3. Verify token dengan /me endpoint```ssh user@stb

curl -H "Authorization: Bearer $TOKEN" \

  http://localhost:18081/auth/mecd /home/user/tixgo-microservices



# 4. Create check-in**Curl Example:**chmod +x deploy.sh

curl -X POST http://localhost:18082/checkins \

  -H "Content-Type: application/json" \```bash./deploy.sh

  -H "Authorization: Bearer $TOKEN" \

  -d '{"event_id":"konsert_2026","ticket_id":"TKT-001"}'curl http://localhost:18081/health```



# 5. Get attendance for event```

curl -H "Authorization: Bearer $TOKEN" \

  http://localhost:18082/attendance/konsert_2026**Expected Output:**

```

---```bash

## Troubleshooting

$ ./deploy.sh

### Containers tidak running

#### 2. User Registration✓ Building images...

Diagnosis:

```bash**Endpoint:** `POST /auth/register`✓ Starting containers...

docker-compose logs identity-service

docker-compose logs attendance-service✓ Services are running on ports 18081 and 18082

docker ps

```**Authentication:** ❌ Tidak diperlukan```



Solution:

```bash

docker-compose build**Request Body:**### 4. Testing the Deployment

docker-compose up

``````json



### Port sudah digunakan{**Local Testing (on STB):**



Check process:  "username": "string (min 3, max 50 karakter)",```bash

```bash

lsof -i :18081  "password": "string (min 4, max 200 karakter)",curl http://localhost:18081/health

lsof -i :18082

```  "role": "string (committee|admin) - default: committee"curl http://localhost:18082/health



Kill process:}```

```bash

lsof -ti:18081 | xargs kill -9```

lsof -ti:18082 | xargs kill -9

```**Remote Testing (via public domain):**



### JWT_SECRET error atau token tidak valid**Response (200 OK):**```bash



Check .env file:```jsoncurl https://dina.theokaitou.my.id/health

```bash

cat .env{curl https://ratu.theokaitou.my.id/health

```

  "username": "panitia1",```

Pastikan:

1. JWT_SECRET tidak kosong  "role": "committee"

2. JWT_SECRET sama di semua services

3. Min 32 karakter untuk security}**Full Workflow Example:**



Restart services:``````bash

```bash

docker-compose restart# Login

```

**Curl Example:**TOKEN=$(curl -s -X POST https://dina.theokaitou.my.id/auth/login \

### Token expired error

```bash  -H "Content-Type: application/json" \

Token sudah kadaluarsa (> 120 menit). Login ulang:

curl -X POST http://localhost:18081/auth/register \  -d '{"username":"panitia1","password":"secret"}' \

```bash

TOKEN=$(curl -s -X POST http://localhost:18081/auth/login \  -H "Content-Type: application/json" \  | jq -r .access_token)

  -H "Content-Type: application/json" \

  -d '{"username":"panitia1","password":"secret"}' | jq -r .access_token)  -d '{

```

    "username": "panitia1",# Create check-in

### Ticket sudah pernah check-in

    "password": "rahasia123",curl -X POST https://ratu.theokaitou.my.id/checkins \

Ticket ID harus unik per event. Gunakan ticket_id yang berbeda:

    "role": "committee"  -H "Content-Type: application/json" \

```bash

curl -X POST http://localhost:18082/checkins \  }'  -H "Authorization: Bearer $TOKEN" \

  -H "Content-Type: application/json" \

  -H "Authorization: Bearer $TOKEN" \```  -d '{"event_id":"evt1","ticket_id":"TICKET123"}'

  -d '{"event_id":"evt1","ticket_id":"TKT-UNIQUE-002"}'

```



### 401 Unauthorized error**Error Response (400):**# Fetch attendance



Authorization header format harus: `"Bearer <token>"````jsoncurl -H "Authorization: Bearer $TOKEN" \



Benar:{  https://ratu.theokaitou.my.id/attendance/evt1

```bash

curl -H "Authorization: Bearer $TOKEN" http://localhost:18082/checkins  "detail": "User panitia1 sudah terdaftar"```

```

}

### View Logs

```### 5. Automated Testing

```bash

docker-compose logs identity-service -fRun the smoke test to verify all services:

docker-compose logs attendance-service -f

docker-compose logs -f---```bash

docker-compose logs --tail=50

```# Local



## Struktur Project#### 3. User Login./smoke-test.sh http://localhost:18081 http://localhost:18082



```**Endpoint:** `POST /auth/login`

tixgo-microservices/

├── identity-service/# Remote

│   ├── app/

│   │   └── main.py              # Identity service implementation**Authentication:** ❌ Tidak diperlukan./smoke-test.sh https://dina.theokaitou.my.id https://ratu.theokaitou.my.id

│   ├── Dockerfile

│   └── requirements.txt```

├── attendance-service/

│   ├── app/**Request Body:**

│   │   └── main.py              # Attendance service implementation

│   ├── Dockerfile```jsonThe smoke test will:

│   └── requirements.txt

├── cloudflared/{Check health endpoints

│   └── config.yml.example

├── docker-compose.yml  "username": "string",Register & login a user

├── docker-compose.prod.yml

├── deploy.sh  "password": "string"Create a check-in

├── smoke-test.sh

├── .env.example}Fetch attendance data

├── .gitignore

├── README.md```

└── README.pdf

```## Project Structure



## Notes**Response (200 OK):**



### Data Persistence```json```



Saat ini data disimpan in-memory. Data akan hilang saat container restart.{tixgo-microservices/



Untuk production: gunakan database seperti PostgreSQL atau SQLite.  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJwYW5pdGlhMSIsInJvbGUiOiJjb21taXR0ZWUiLCJpYXQiOjE3Njc0NDY3NDIsImV4cCI6MTc2NzQ1Mzk0Mn0.MU1pIorjZmKyhe7hweDGHkLvFzPtsxCCFo6FMnYiXxE",├── identity-service/



### Future Improvements  "token_type": "bearer"│   ├── Dockerfile



1. Event Management Service}│   ├── requirements.txt

2. Database Persistence (PostgreSQL/SQLite)

3. Rate limiting & throttling```│   └── app/

4. API logging & monitoring

5. CI/CD pipeline (GitHub Actions)│       └── main.py           # FastAPI app with auth endpoints



## References**Curl Example:**├── attendance-service/



- FastAPI Documentation: https://fastapi.tiangolo.com```bash│   ├── Dockerfile

- Docker Documentation: https://docs.docker.com

- JWT Specification: https://tools.ietf.org/html/rfc7519# Login│   ├── requirements.txt



---TOKEN=$(curl -s -X POST http://localhost:18081/auth/login \│   └── app/



**Version:** 1.0.0  -H "Content-Type: application/json" \│       └── main.py           # FastAPI app with checkin endpoints

**Status:** Production Ready for Tugas 2

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
