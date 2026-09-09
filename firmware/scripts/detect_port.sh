#!/usr/bin/env bash
set -e

PORT=$(ls /dev/cu.* 2>/dev/null \
  | grep -v Bluetooth \
  | grep -E 'usb|USB|wch|CH34|SLAB|uart|serial' \
  | head -n 1 || true)

if [ -z "$PORT" ]; then
  echo "ESP32 USB serial port not detected."
  exit 1
fi

echo "$PORT"
