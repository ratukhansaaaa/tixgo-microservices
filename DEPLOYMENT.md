# Deployment Documentation - TixGo Microservices

**Tanggal:** January 3, 2026  
**Status:** Successfully Deployed to STB  
**Deployment Method:** Docker Compose via CloudFlare Tunnel SSH  

---

## 1. Deployment Information

### Infrastructure
- **Target Server:** STB (Set Top Box) - `ssh.theokaitou.my.id`
- **SSH Method:** CloudFlare Access Tunnel
- **Deployment Script:** `deploy.sh`
- **Configuration:** `docker-compose.prod.yml`

### Services Deployed
| Service | Container Name | Port | Status |
|---------|---|---|---|
| Identity Service | tixgo-identity | 18081 | Running |
| Attendance Service | tixgo-attendance | 18082 | Running |

---

## 2. Deployment Steps

### Step 1: Copy Project Files to STB
```bash
# Copy entire project via SCP
scp -o ProxyCommand="cloudflared access ssh --hostname %h" \
  -r /path/to/tixgo-microservices/* \
  root@ssh.theokaitou.my.id:~/tixgo-microservices/
```

### Step 2: Copy .env File
```bash
# Copy .env separately (not in git)
scp -o ProxyCommand="cloudflared access ssh --hostname %h" \
  /path/to/.env \
  root@ssh.theokaitou.my.id:~/tixgo-microservices/.env
```

### Step 3: Run Deployment Script
```bash
# SSH into STB and run deploy script
ssh -o ProxyCommand="cloudflared access ssh --hostname %h" \
  -o StrictHostKeyChecking=accept-new \
  root@ssh.theokaitou.my.id

# On STB:
cd ~/tixgo-microservices
chmod +x deploy.sh
./deploy.sh
```

### Step 4: Verify Deployment
```bash
# Check running containers
docker compose -f docker-compose.prod.yml ps

# Test health endpoints
curl http://localhost:18081/health
curl http://localhost:18082/health
```

---

## 3. Test Results

### Health Check
```
Identity Service (18081): {"status":"ok","service":"identity-service"}
Attendance Service (18082): {"status":"ok","service":"attendance"}
```

### Automated Smoke Test
Executed: `./smoke-test.sh`

**Test Sequence:**
1. Health endpoints check
2. User registration (panitia1)
3. User login (JWT token generated)
4. Check-in creation (evt-smoke / TICKET-SMOKE)
5. Attendance query for event

**Result:** All tests passed

**Full Test Output:** See `test-results.txt`

---

## 4. Access Information

### Local Access (on STB)
```bash
curl http://localhost:18081/health
curl http://localhost:18082/health
```

### Network Access (from other machines)
```bash
curl http://<STB_IP>:18081/health
curl http://<STB_IP>:18082/health
```

### Public Access (via Domain)
After Backend Team configures domain routing:
```bash
curl https://<identity-domain>/health
curl https://<attendance-domain>/health
```

---

## 5. API Endpoints Available

### Identity Service (Port 18081)
- `GET /health` - Health check
- `POST /auth/register` - User registration
- `POST /auth/login` - User login (returns JWT token)
- `GET /auth/me` - Get current user info (requires auth)

### Attendance Service (Port 18082)
- `GET /health` - Health check
- `POST /checkins` - Create check-in (requires auth)
- `GET /attendance/{event_id}` - Get attendance records (requires auth)

---

## 6. Test Credentials

```
Username: panitia1
Password: secret
Role: committee
```

---

## 7. Important Files

| File | Purpose |
|------|---------|
| `README.md` | System documentation with usage instructions |
| `README.pdf` | PDF version of documentation |
| `docker-compose.prod.yml` | Production deployment configuration |
| `deploy.sh` | Automated deployment script |
| `smoke-test.sh` | Automated end-to-end test script |
| `.env` | Environment variables (not tracked in git) |
| `test-results.txt` | Results from smoke test execution |

---

## 8. Verification Checklist

- Source code on GitHub: `https://github.com/ratukhansaaaa/tixgo-microservices`
- Documentation (README.md + README.pdf)
- Docker containers isolated and running
- Authentication & authorization (JWT, bcrypt)
- No secrets in git (.env in .gitignore)
- Deployment script working
- Smoke test passing
- Services accessible on configured ports

---

## 9. Troubleshooting

### Containers not starting?
```bash
docker compose -f docker-compose.prod.yml logs -f
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
```

### Port already in use?
```bash
lsof -i :18081
lsof -i :18082
kill -9 <PID>
```

### JWT_SECRET error?
```bash
# Verify .env file exists with valid JWT_SECRET
cat .env
# Regenerate if needed
openssl rand -hex 32
```

### Token validation failed?
- Token may be expired (120 minute lifetime)
- Login again to get fresh token
- Verify JWT_SECRET is same across services

---

## 10. Monitoring

### View Logs
```bash
docker compose -f docker-compose.prod.yml logs -f tixgo-identity
docker compose -f docker-compose.prod.yml logs -f tixgo-attendance
```

### Check Service Health
```bash
curl http://localhost:18081/health
curl http://localhost:18082/health
```

---

**Deployment Status:** Production Ready  
**Last Verified:** 2026-01-03 22:56 (STB Time)  
**Next Steps:** Await Backend Team for domain routing configuration  
