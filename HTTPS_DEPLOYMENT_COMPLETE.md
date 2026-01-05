# ✅ TixGo Microservices - HTTPS Deployment Complete

**Status Date:** January 5, 2026  
**Environment:** STB (ARM Linux)  
**Protocol:** HTTPS with Self-Signed Certificates  

---

## 🎯 Deployment Summary

### Services Online
- ✅ **Identity Service** → `https://dina.theokaitou.my.id`
- ✅ **Attendance Service** → `https://ratu.theokaitou.my.id`
- ✅ **Event Service** → Internal service (proxied via Attendance)

### Infrastructure
- ✅ **Docker Compose** - All services containerized
- ✅ **Nginx** - Reverse proxy with HTTPS/TLS
- ✅ **Self-Signed Certificates** - Valid for 365 days
- ✅ **DH Parameters** - 2048-bit for enhanced security

---

## 🔐 Certificate Details

| Domain | Issued | Expires | Validity |
|--------|--------|---------|----------|
| dina.theokaitou.my.id | Jan 5, 2026 | Jan 5, 2027 | 365 days |
| ratu.theokaitou.my.id | Jan 5, 2026 | Jan 5, 2027 | 365 days |

**Note:** Self-signed certificates will show browser warnings (expected). For production, upgrade to Let's Encrypt using the setup scripts provided.

---

## ✅ Verification Results

### Health Endpoints
```bash
curl -k https://dina.theokaitou.my.id/health
# Response: {"status":"ok","service":"identity-service"}

curl -k https://ratu.theokaitou.my.id/health
# Response: {"status":"ok","service":"attendance"}
```

### Authentication Flow
```bash
# 1. Login
curl -k https://dina.theokaitou.my.id/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"panitia1","password":"secret"}'
# Returns: JWT token

# 2. Create Checkin
curl -k https://ratu.theokaitou.my.id/checkins \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"event_id":"evt-test","ticket_id":"TICKET-001"}'
# Returns: {"status":"checked_in", ...}

# 3. Get Attendance
curl -k https://ratu.theokaitou.my.id/attendance/evt-test \
  -H "Authorization: Bearer <token>"
# Returns: Attendance records for event
```

### Event Service Proxy
```bash
curl -k https://ratu.theokaitou.my.id/events/health \
  -H "Authorization: Bearer <token>"
# Returns: Event service health (proxied internally)
```

---

## 🚀 How to Access

### From Browser
1. Visit: `https://dina.theokaitou.my.id` or `https://ratu.theokaitou.my.id`
2. **Warning:** Browser will show certificate warning (expected for self-signed)
3. Click **Advanced** → **Proceed anyway** to continue

### From CLI (curl)
```bash
# Ignore certificate warning with -k flag
curl -k https://dina.theokaitou.my.id/health

# Or import certificate to system trust store
sudo security add-trusted-cert -d -r trustRoot \
  -k /Library/Keychains/System.keychain \
  ./nginx/certs/dina.theokaitou.my.id/fullchain.pem
```

### From API/Mobile App
- Add certificate to trusted certificates in your app
- Or configure to ignore cert validation (dev only)
- Make requests to: `https://dina.theokaitou.my.id` or `https://ratu.theokaitou.my.id`

---

## 📋 Service Configuration

### Docker Compose Services
- **tixgo-identity** - Identity/Auth Service (port 18081→8000)
- **tixgo-attendance** - Attendance Service (port 18082→8000)
- **tixgo-event** - Event Service (port 8000, internal only)
- **tixgo-nginx** - Nginx Reverse Proxy (port 80→, 443→HTTPS)

### Nginx Configuration
- HTTP (port 80) → Redirects to HTTPS
- HTTPS (port 443) → SSL termination + proxying
- Domain routing:
  - `dina.theokaitou.my.id` → `http://identity:8000`
  - `ratu.theokaitou.my.id` → `http://attendance:8000`
  - `/events/*` paths → `http://event:8000` (Event Service proxy)

---

## 🔄 Certificate Management

### Current: Self-Signed Certificates
- ✅ Works immediately
- ⚠️ Browser warnings (expected)
- ✅ Valid for 365 days
- ✅ Good for testing/development

### Next: Let's Encrypt (When Ready)
Two setup scripts provided:

1. **DNS-Based Validation** (Recommended)
   ```bash
   bash setup-letsencrypt-dns.sh
   ```
   - Requires: Cloudflare API token
   - No port forwarding needed
   - Fully automated renewal

2. **HTTP-Based Validation** (Alternative)
   ```bash
   bash setup-letsencrypt.sh
   ```
   - Requires: Port 80/443 open to internet
   - Validates domain ownership via HTTP
   - Needs DNS pointing to server IP

---

## 📝 Logs & Monitoring

### View Service Logs
```bash
# All services
docker compose -f docker-compose.prod.yml logs -f

# Specific service
docker logs tixgo-nginx
docker logs tixgo-identity
docker logs tixgo-attendance
docker logs tixgo-event
```

### Check Service Status
```bash
docker compose -f docker-compose.prod.yml ps
```

### Nginx Access/Error Logs
```bash
docker exec tixgo-nginx tail -f /var/log/nginx/access.log
docker exec tixgo-nginx tail -f /var/log/nginx/error.log
```

---

## 🛠️ Troubleshooting

### Issue: Certificate Warning in Browser
**Expected behavior** - Self-signed certificates trigger warnings  
**Solution:** Click "Advanced" → "Proceed anyway" or upgrade to Let's Encrypt

### Issue: Connection Refused
```bash
# Check if nginx is running
docker compose -f docker-compose.prod.yml ps

# Restart nginx
docker compose -f docker-compose.prod.yml restart nginx

# Check nginx logs
docker logs tixgo-nginx
```

### Issue: 502 Bad Gateway
```bash
# Backend services may not be ready
# Check if identity/attendance/event containers are running
docker compose -f docker-compose.prod.yml ps

# View nginx logs for more details
docker exec tixgo-nginx grep "502" /var/log/nginx/error.log
```

### Issue: Missing JWT Token
```bash
# Ensure you login first and get token
curl -k https://dina.theokaitou.my.id/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"panitia1","password":"secret"}'

# Then use token in Authorization header
curl -k https://ratu.theokaitou.my.id/checkins \
  -H "Authorization: Bearer <your_token_here>"
```

---

## 📦 Files Modified

```
✅ docker-compose.prod.yml
   - Added nginx service with port 80, 443 mapping
   - Volume mounts for certificates

✅ nginx/nginx.conf
   - Dual domain SSL configuration
   - HTTP→HTTPS redirects
   - Reverse proxy rules
   - DH parameters for security

✅ setup-selfsigned.sh (NEW)
   - Auto-generates self-signed certificates
   - Creates DH parameters
   - Starts services with HTTPS

✅ setup-letsencrypt.sh (NEW)
   - Let's Encrypt HTTP-based validation
   - Automated certificate generation

✅ setup-letsencrypt-dns.sh (NEW)
   - Let's Encrypt DNS-based validation
   - Cloudflare API integration
   - No port forwarding needed
```

---

## ✨ Key Features Enabled

- ✅ HTTPS encryption on both domains
- ✅ JWT authentication working
- ✅ Checkin tracking functional
- ✅ Event service accessible via proxy
- ✅ Attendance reporting working
- ✅ Self-signed certificates (365 days validity)
- ✅ Automatic HTTPS redirect from HTTP
- ✅ Strong TLS configuration (1.2+)
- ✅ DH parameters for enhanced security

---

## 🎯 Next Steps

### Option 1: Keep Self-Signed Certificates
- No action needed
- Services will work for 365 days
- Users need to accept certificate warnings

### Option 2: Upgrade to Let's Encrypt (Recommended for Production)

**If you have Cloudflare domain:**
```bash
bash setup-letsencrypt-dns.sh
```

**If you can open port 80/443 to internet:**
```bash
bash setup-letsencrypt.sh
```

### Option 3: Update Certificate Renewal Reminder
```bash
# Check certificate expiration
openssl x509 -in ./nginx/certs/dina.theokaitou.my.id/fullchain.pem \
  -text -noout | grep -A1 "Not After"

# Set calendar reminder for Jan 4, 2027 to renew
```

---

## 📞 Support Commands

```bash
# Test HTTPS endpoint
curl -k https://dina.theokaitou.my.id/health

# View certificate details
openssl x509 -in ./nginx/certs/dina.theokaitou.my.id/fullchain.pem \
  -text -noout

# Check certificate expiration
openssl x509 -in ./nginx/certs/dina.theokaitou.my.id/fullchain.pem \
  -noout -dates

# View nginx config
cat nginx/nginx.conf

# Check docker network
docker network ls
docker network inspect tixgo-microservices_tixgo-net
```

---

## ✅ Deployment Checklist

- [x] Docker services configured
- [x] Nginx reverse proxy setup
- [x] Self-signed certificates generated
- [x] HTTPS endpoints verified working
- [x] JWT authentication tested
- [x] Checkin functionality tested
- [x] Event service proxy working
- [x] Health checks passing
- [x] End-to-end flow working
- [x] Documentation complete

---

**🎉 Deployment Complete!**  
Your TixGo Microservices are now running securely over HTTPS.

For questions or issues, refer to the Troubleshooting section above.
