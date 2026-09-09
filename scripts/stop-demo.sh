#!/usr/bin/env bash
set -u

BACKEND_PID_FILE="/tmp/sitelink-scout-backend.pid"
FRONTEND_PID_FILE="/tmp/sitelink-scout-frontend.pid"

echo "========================================"
echo " SiteLink Scout Demo Stop"
echo "========================================"

stop_pid_file() {
  local name="$1"
  local pid_file="$2"

  if [ ! -f "$pid_file" ]; then
    echo "$name: no PID file."
    return
  fi

  local pid
  pid=$(cat "$pid_file")

  if kill -0 "$pid" 2>/dev/null; then
    echo "Stopping $name PID $pid..."
    kill "$pid" 2>/dev/null || true

    for _ in {1..10}; do
      if ! kill -0 "$pid" 2>/dev/null; then
        break
      fi
      sleep 0.3
    done

    if kill -0 "$pid" 2>/dev/null; then
      echo "$name did not stop gracefully. Sending SIGKILL."
      kill -9 "$pid" 2>/dev/null || true
    fi
  else
    echo "$name PID $pid is already stopped."
  fi

  rm -f "$pid_file"
}

stop_pid_file "Backend" "$BACKEND_PID_FILE"
stop_pid_file "Frontend" "$FRONTEND_PID_FILE"

echo
echo "Checking demo ports..."

for port in 8000 5173; do
  PIDS=$(lsof -ti tcp:"$port" 2>/dev/null || true)

  if [ -n "$PIDS" ]; then
    echo "Port $port still has process(es): $PIDS"
    echo "Stopping leftover demo process(es)..."

    for pid in $PIDS; do
      kill "$pid" 2>/dev/null || true
    done
  else
    echo "Port $port: free"
  fi
done

sleep 1

echo
echo "========================================"
echo " SiteLink Scout Demo OFFLINE"
echo "========================================"
