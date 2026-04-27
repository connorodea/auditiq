#!/usr/bin/env bash
set -euo pipefail

APP_DIR="/var/www/auditiq"
DOMAIN="aiaudits.dev"

echo "=== AuditIQ Deploy ==="
echo "Target: ${APP_DIR}"
echo "Domain: ${DOMAIN}"

# ── Database (Docker) ──
echo ""
echo "--- Starting database services ---"
cd "${APP_DIR}"
docker compose -f deploy/docker-compose.prod.yml up -d
echo "Waiting for Postgres to be ready..."
until docker exec auditiq-postgres pg_isready -U auditiq > /dev/null 2>&1; do
    sleep 1
done
echo "Postgres ready."

# ── Backend ──
echo ""
echo "--- Deploying backend ---"
cd "${APP_DIR}/backend"

# Create venv if not exists
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet -e .
deactivate

# Run migrations
source .venv/bin/activate
alembic upgrade head 2>/dev/null || echo "No migrations to run (or alembic not initialized yet)"

# Seed questions
python -m auditiq.seeds
deactivate

# Install and restart systemd service
cp "${APP_DIR}/deploy/auditiq-backend.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable auditiq-backend
systemctl restart auditiq-backend
echo "Backend service restarted."

# ── Frontend ──
echo ""
echo "--- Deploying frontend ---"
cd "${APP_DIR}/frontend"

npm ci --omit=dev --silent
npm run build

# Copy standalone static files
cp -r .next/static .next/standalone/.next/static 2>/dev/null || true
cp -r public .next/standalone/public 2>/dev/null || true

# Install and restart systemd service
cp "${APP_DIR}/deploy/auditiq-frontend.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable auditiq-frontend
systemctl restart auditiq-frontend
echo "Frontend service restarted."

# ── Nginx ──
echo ""
echo "--- Configuring nginx ---"
cp "${APP_DIR}/deploy/nginx.conf" /etc/nginx/sites-available/aiaudits.dev
ln -sf /etc/nginx/sites-available/aiaudits.dev /etc/nginx/sites-enabled/aiaudits.dev

# Test nginx config
nginx -t
systemctl reload nginx
echo "Nginx reloaded."

# ── Health check ──
echo ""
echo "--- Health checks ---"
sleep 2
curl -sf http://127.0.0.1:8100/api/v1/health && echo " [backend OK]" || echo " [backend FAILED]"
curl -sf http://127.0.0.1:3100/ > /dev/null && echo " [frontend OK]" || echo " [frontend FAILED]"

echo ""
echo "=== Deploy complete ==="
echo "Site: https://${DOMAIN}"
echo "API:  https://api.${DOMAIN}/api/v1/health"
