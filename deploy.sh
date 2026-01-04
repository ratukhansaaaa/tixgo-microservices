
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

if [ ! -f .env ]; then
  echo "ERROR: .env file not found. Create .env on the STB with production secrets. See .env.example"
  exit 1
fi

echo "Bringing down any existing stack (safe)..."
docker compose -f docker-compose.prod.yml down || true

echo "Building and starting services (this may take a few minutes)..."
docker compose -f docker-compose.prod.yml up -d --build

echo "Current containers:"
docker compose -f docker-compose.prod.yml ps

echo "To follow logs: docker compose -f docker-compose.prod.yml logs -f"
