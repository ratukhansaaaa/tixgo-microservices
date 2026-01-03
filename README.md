TixGo Microservices
===================

This repository contains two small FastAPI microservices used for the TixGo final project:

- identity-service: authentication endpoints (register, login, me)
- attendance-service: check-in endpoints (create checkin, fetch attendance)

What I added for deployment

- `docker-compose.prod.yml` — production-ready compose file. It keeps host ports mapped (18081/18082) so BT can route their subdomains to STB:PORT.
- `deploy.sh` — simple script to run on the STB to bring up the stack.
- `smoke-test.sh` — quick verification script that logs in, creates a checkin, and fetches attendance.
- `cloudflared/config.yml.example` — example config for Cloudflare Tunnel (BT usually handles the tunnel).
- `.env.example` — example env file with variables used by both services.

Important notes (STB deployment)

1) Do NOT commit your real `.env` into git. Create a `.env` file on the STB with production secrets.
	 Example `.env` contents:

	 JWT_SECRET=<long-random-hex>
	 JWT_ALG=HS256
	 TOKEN_EXPIRE_MINUTES=120

2) Keep host ports mapped (we recommend this for your arrangement with BT):
	 - identity container maps 8000 -> host 18081
	 - attendance container maps 8000 -> host 18082
	 BT can route `dina.theokaitou.my.id` -> `STB_IP:18081` and `ratu.theokaitou.my.id` -> `STB_IP:18082`.

3) How to deploy on the STB (example)

```bash
# copy .env to the repo directory on STB
scp .env user@stb:/home/user/tixgo-microservices/.env
# on the STB
cd /home/user/tixgo-microservices
./deploy.sh
```

4) How to test (local on STB or remote via subdomain)

Local (on the host that runs Docker):
```bash
curl http://localhost:18081/health
curl http://localhost:18082/health
```

Remote (via BT routing / public subdomain):
```bash
curl https://dina.theokaitou.my.id/health
curl https://ratu.theokaitou.my.id/health
```

Login and create a checkin (example)

```bash
# login
curl -X POST https://dina.theokaitou.my.id/auth/login -H "Content-Type: application/json" \
	-d '{"username":"panitia1","password":"secret"}'

# use token from above to create a checkin
curl -X POST https://ratu.theokaitou.my.id/checkins \
	-H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" \
	-d '{"event_id":"evt1","ticket_id":"TICKET123"}'
```

5) Smoke test (automated)

On any machine with network access to the service (or run on STB):
```bash
./smoke-test.sh https://dina.theokaitou.my.id https://ratu.theokaitou.my.id
```

Files to complete after BT hands tunnel/route credentials

- If BT requires you to run cloudflared on the STB, create the credentials using `cloudflared tunnel create` and place the credentials file on the STB, then update `cloudflared/config.yml` and optionally enable the `cloudflared` service in `docker-compose.prod.yml`.

- If BT handles routing externally, no further tunnel work is required — just ensure containers are up and ports are accessible.

Notes & recommendations

- Data is currently in-memory; for production you should add persistence (SQLite or Postgres) so checkins and registered users survive restarts.
- Rotate `JWT_SECRET` before handing to graders and keep it secret.
- Consider adding basic rate-limiting or an API gateway if this will be exposed publicly for long periods.

Contact

If you want, I can also add a small GitHub Actions workflow to build multi-arch images and push them to Docker Hub (requires credentials). Let me know and provide the Docker Hub repo name.