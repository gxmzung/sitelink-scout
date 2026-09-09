#!/usr/bin/env bash
set -e

cd "$(dirname "$0")/.."

PORT=$(./scripts/detect_port.sh)

echo "Detected port: $PORT"
echo "Building and uploading SiteLink Scout..."

python3 -m platformio run \
  --target upload \
  --upload-port "$PORT"
