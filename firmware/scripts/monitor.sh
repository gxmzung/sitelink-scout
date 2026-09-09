#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

PORT=$(./scripts/detect_port.sh)

echo "Opening serial monitor: $PORT"

python3 -m platformio device monitor \
  --port "$PORT" \
  --baud 115200
