#!/usr/bin/env bash
set -u

BACKEND_PID_FILE="/tmp/sitelink-scout-backend.pid"
FRONTEND_PID_FILE="/tmp/sitelink-scout-frontend.pid"

echo "========================================"
echo " SiteLink Scout Demo Stop"
echo "========================================"

stop_pid() {
  local name="$1"
  local pid="$2"

  if ! kill -0 "$pid" 2>/dev/null; then
    echo "$name PID $pid already stopped."
    return
  fi

  echo "Stopping $name PID $pid..."
  kill "$pid" 2>/dev/null || true

  for _ in {1..15}; do
    if ! kill -0 "$pid" 2>/dev/null; then
      echo "$name PID $pid stopped."
      return
    fi
    sleep 0.2
  done

  echo "$name PID $pid did not stop gracefully. Sending SIGKILL."
  kill -9 "$pid" 2>/dev/null || true
}

stop_pid_file() {
  local name="$1"
  local pid_file="$2"

  if [ ! -f "$pid_file" ]; then
    echo "$name: no PID file."
    return
  fi

  local pid
  pid=$(cat "$pid_file")

  stop_pid "$name" "$pid"
  rm -f "$pid_file"
}

stop_pid_file "Backend" "$BACKEND_PID_FILE"
stop_pid_file "Frontend" "$FRONTEND_PID_FILE"

echo
echo "Cleaning leftover processes on demo ports..."

for port in 8000 5173; do
  PIDS=$(lsof -ti tcp:"$port" 2>/dev/null || true)

  if [ -z "$PIDS" ]; then
    echo "Port $port: free"
    continue
  fi

  echo "Port $port has leftover process(es):"
  echo "$PIDS"

  for pid in $PIDS; do
    stop_pid "Port $port process" "$pid"
  done
done

sleep 1

echo
echo "Final port check..."

FAILED=0

for port in 8000 5173; do
  if lsof -ti tcp:"$port" >/dev/null 2>&1; then
    echo "ERROR: port $port is still occupied:"
    lsof -i :"$port" || true
    FAILED=1
  else
    echo "Port $port: free"
  fi
done

echo
echo "========================================"

if [ "$FAILED" -eq 0 ]; then
  echo " SiteLink Scout Demo OFFLINE"
  echo "========================================"
  exit 0
else
  echo " SiteLink Scout Demo STOP FAILED"
  echo "========================================"
  exit 1
fi
