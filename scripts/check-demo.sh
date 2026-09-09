#!/usr/bin/env bash
set -u

BACKEND_URL="http://127.0.0.1:8000"
FRONTEND_URL="http://127.0.0.1:5173"

echo "========================================"
echo " SiteLink Scout Demo Health Check"
echo "========================================"

FAILED=0

echo
echo "[Backend process]"
if lsof -i :8000 >/dev/null 2>&1; then
  lsof -i :8000
else
  echo "OFFLINE"
  FAILED=1
fi

echo
echo "[Backend health]"
if curl -fsS "$BACKEND_URL/api/v1/health" | python3 -m json.tool; then
  :
else
  echo "FAILED"
  FAILED=1
fi

echo
echo "[Coverage]"
if curl -fsS "$BACKEND_URL/api/v1/coverage" | python3 -m json.tool; then
  :
else
  echo "FAILED"
  FAILED=1
fi

echo
echo "[Devices]"
if curl -fsS "$BACKEND_URL/api/v1/devices" | python3 -m json.tool; then
  :
else
  echo "FAILED"
  FAILED=1
fi

echo
echo "[Frontend process]"
if lsof -i :5173 >/dev/null 2>&1; then
  lsof -i :5173
else
  echo "OFFLINE"
  FAILED=1
fi

echo
echo "[Frontend HTTP]"
if curl -fsS "$FRONTEND_URL" >/dev/null; then
  echo "ONLINE"
else
  echo "FAILED"
  FAILED=1
fi

echo
echo "========================================"

if [ "$FAILED" -eq 0 ]; then
  echo " SiteLink Scout Demo: READY"
  echo "========================================"
  exit 0
else
  echo " SiteLink Scout Demo: NOT READY"
  echo "========================================"
  exit 1
fi
