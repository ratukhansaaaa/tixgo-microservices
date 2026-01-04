set -euo pipefail


IDENTITY_HOST=${1:-http://localhost:18081}
ATTENDANCE_HOST=${2:-http://localhost:18082}

echo "Checking health endpoints..."
curl -sS "$IDENTITY_HOST/health" | jq || true
curl -sS "$ATTENDANCE_HOST/health" | jq || true

echo "\nLogging in as demo user (panitia1 / secret)"
TOKEN=$(curl -sS -X POST "$IDENTITY_HOST/auth/login" -H "Content-Type: application/json" -d '{"username":"panitia1","password":"secret"}' | jq -r .access_token)

echo "Token: ${TOKEN:0:60}..."

echo "\nCreating checkin evt-smoke / TICKET-SMOKE"
CREATE_RESP=$(curl -sS -X POST "$ATTENDANCE_HOST/checkins" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"event_id":"evt-smoke","ticket_id":"TICKET-SMOKE"}')

echo "$CREATE_RESP" | jq || echo "$CREATE_RESP"

echo "\nFetching attendance for evt-smoke"
curl -sS -H "Authorization: Bearer $TOKEN" "$ATTENDANCE_HOST/attendance/evt-smoke" | jq || true

echo "\nSmoke test finished. If the above responses look correct, services are working."
