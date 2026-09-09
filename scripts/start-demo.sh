#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"

BACKEND_PID_FILE="/tmp/sitelink-scout-backend.pid"
FRONTEND_PID_FILE="/tmp/sitelink-scout-frontend.pid"

BACKEND_LOG="/tmp/sitelink-scout-backend.log"
FRONTEND_LOG="/tmp/sitelink-scout-frontend.log"

BACKEND_URL="http://127.0.0.1:8000"
FRONTEND_URL="http://127.0.0.1:5173"

echo "========================================"
echo " SiteLink Scout Demo Start"
echo "========================================"

echo
echo "[1/5] Checking ports..."

if lsof -tiTCP:8000 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "ERROR: port 8000 is already in use."
  echo "Run: ./scripts/stop-demo.sh"
  exit 1
fi

if lsof -tiTCP:5173 -sTCP:LISTEN >/dev/null 2>&1; then
  echo "ERROR: port 5173 is already in use."
  echo "Run: ./scripts/stop-demo.sh"
  exit 1
fi

echo "Ports 8000 and 5173 are free."

echo
echo "[2/5] Starting backend..."

cd "$BACKEND_DIR"

nohup .venv/bin/python -m uvicorn app.main:app \
  --host 0.0.0.0 \
  --port 8000 \
  </dev/null \
  >"$BACKEND_LOG" \
  2>&1 &

BACKEND_PID=$!
echo "$BACKEND_PID" > "$BACKEND_PID_FILE"

echo "Backend PID: $BACKEND_PID"

echo
echo "[3/5] Waiting for backend..."

BACKEND_OK=0

for _ in {1..20}; do
  if curl -fsS "$BACKEND_URL/api/v1/health" >/dev/null 2>&1; then
    BACKEND_OK=1
    break
  fi
  sleep 0.5
done

if [ "$BACKEND_OK" -ne 1 ]; then
  echo "ERROR: backend failed to start."
  echo
  echo "--- backend log ---"
  cat "$BACKEND_LOG" || true
  exit 1
fi

echo "Backend ONLINE."

echo
echo "[4/5] Starting frontend..."

cd "$FRONTEND_DIR"

nohup npm run dev -- \
  --host 0.0.0.0 \
  --port 5173 \
  --strictPort \
  </dev/null \
  >"$FRONTEND_LOG" \
  2>&1 &

FRONTEND_PID=$!
echo "$FRONTEND_PID" > "$FRONTEND_PID_FILE"

echo "Frontend PID: $FRONTEND_PID"

echo
echo "[5/5] Waiting for frontend..."

FRONTEND_OK=0

for _ in {1..30}; do
  if curl -fsS "$FRONTEND_URL" >/dev/null 2>&1; then
    FRONTEND_OK=1
    break
  fi
  sleep 0.5
done

if [ "$FRONTEND_OK" -ne 1 ]; then
  echo "ERROR: frontend failed to start."
  echo
  echo "--- frontend log ---"
  cat "$FRONTEND_LOG" || true

  if kill -0 "$BACKEND_PID" 2>/dev/null; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi

  rm -f "$BACKEND_PID_FILE"
  exit 1
fi

echo
echo "========================================"
echo " SiteLink Scout Demo ONLINE"
echo "========================================"
echo
echo "Field Console:"
echo "  http://localhost:5173"
echo
echo "Backend:"
echo "  http://127.0.0.1:8000"
echo
echo "Swagger:"
echo "  http://127.0.0.1:8000/docs"
echo
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo
echo "Run health check:"
echo "  ./scripts/check-demo.sh"
echo
echo "Stop demo:"
echo "  ./scripts/stop-demo.sh"
echo "========================================"
