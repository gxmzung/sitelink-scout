#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

cd "$ROOT_DIR"

echo "========================================"
echo " SiteLink Scout Boardless Demo"
echo "========================================"

if ! curl -fsS \
  http://127.0.0.1:8000/api/v1/health \
  >/dev/null 2>&1; then

  echo "Demo stack is offline."
  echo "Starting SiteLink Scout..."

  ./scripts/start-demo.sh
fi

echo
echo "Sending simulated Scout telemetry..."
echo

python3 scripts/simulate-scout.py \
  --mode dynamic \
  --cycles 10 \
  --interval 2

echo
echo "========================================"
echo " Simulation complete"
echo "========================================"
echo
echo "Open:"
echo "  http://localhost:5173"
echo
echo "Check:"
echo "  ./scripts/check-demo.sh"
