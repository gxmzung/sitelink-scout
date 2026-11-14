#!/usr/bin/env python3
"""Live-stack smoke test: FastAPI + isolated SQLite + Vite HTTP + synthetic telemetry.

This is software-only integration. It does not verify browser rendering, ESP32 or RF accuracy.
"""
import json
import os
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "http://127.0.0.1:8000"
WEB = "http://127.0.0.1:5173"


def request(url, payload=None):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"} if payload is not None else {},
        method="POST" if payload is not None else "GET",
    )
    with urllib.request.urlopen(req, timeout=3) as response:
        body = response.read().decode("utf-8")
        return response.status, body


def await_http(url, process, seconds=35):
    deadline = time.monotonic() + seconds
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"Process exited early ({process.returncode}): {url}")
        try:
            status, body = request(url)
            if status == 200:
                return body
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            pass
        time.sleep(0.25)
    raise TimeoutError(f"Service did not become ready: {url}")


def record(zone, rssi, device):
    status, response = request(
        API + "/api/v1/measurements",
        {
            "device_id": device,
            "zone_id": zone,
            "ssid": "SPATIALINK_SYNTHETIC",
            "bssid": "02:00:00:00:00:01",
            "rssi": rssi,
            "channel": 6,
        },
    )
    assert status == 201, (status, response)
    return json.loads(response)


def main():
    processes = []
    with tempfile.TemporaryDirectory(prefix="spatialink-e2e-") as temp:
        db = Path(temp) / "isolated-e2e.db"
        log_paths = [Path(temp) / "backend.log", Path(temp) / "frontend.log"]
        logs = []
        try:
            env = os.environ.copy()
            env["SITELINK_DATABASE_URL"] = f"sqlite:///{db}"
            env["PYTHONUNBUFFERED"] = "1"
            backend_log = log_paths[0].open("w+")
            logs.append(backend_log)
            backend = subprocess.Popen(
                [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
                cwd=ROOT / "backend", env=env, stdout=backend_log, stderr=subprocess.STDOUT,
            )
            processes.append(backend)
            health = json.loads(await_http(API + "/api/v1/health", backend))
            assert health["status"] == "ok", health

            frontend_log = log_paths[1].open("w+")
            logs.append(frontend_log)
            frontend = subprocess.Popen(
                ["npm", "run", "dev", "--", "--host", "127.0.0.1", "--port", "5173", "--strictPort"],
                cwd=ROOT / "frontend", env=os.environ.copy(),
                stdout=frontend_log, stderr=subprocess.STDOUT,
            )
            processes.append(frontend)
            html = await_http(WEB, frontend)
            assert 'id="root"' in html, "Vite did not serve the React entry HTML"

            # Two independent zones: one usable and one POOR.
            record("E2E-ZONE-A", -62, "E2E-01")
            record("E2E-ZONE-B", -82, "E2E-02")
            _, response = request(API + "/api/v1/coverage")
            coverage = json.loads(response)
            assert coverage["metric"] == "latest_zone_sample_coverage"
            assert coverage["total_zones"] == 2, coverage
            assert coverage["covered_zones"] == 1, coverage
            assert coverage["uncovered_zones"] == 1, coverage
            assert coverage["coverage_percent"] == 50.0, coverage
            assert {z["zone_id"] for z in coverage["zones"]} == {"E2E-ZONE-A", "E2E-ZONE-B"}

            # Simulate change at same zone and verify latest-zone aggregation.
            time.sleep(0.05)
            record("E2E-ZONE-B", -89, "E2E-02")
            _, response = request(API + "/api/v1/coverage")
            changed = json.loads(response)
            assert changed["dead_zones"] == 1, changed
            assert changed["uncovered_zones"] == 1, changed
            _, response = request(API + "/api/v1/devices")
            devices = json.loads(response)
            assert len(devices) == 2, devices
            assert next(d for d in devices if d["device_id"] == "E2E-02")["rssi"] == -89
            _, response = request(API + "/api/v1/measurements")
            assert len(json.loads(response)) == 3, response

            print("PASS: backend health, Vite HTTP, simulated POST -> SQLite -> coverage/devices/measurements")
            print("BOUNDARY: no browser UI assertion, no physical ESP32, no measured RF performance")
        except Exception:
            for log in logs:
                log.flush()
            for path in log_paths:
                if path.exists():
                    print(f"--- {path.name} ---", file=sys.stderr)
                    print(path.read_text(errors="replace")[-5000:], file=sys.stderr)
            raise
        finally:
            for proc in reversed(processes):
                if proc.poll() is None:
                    proc.terminate()
            for proc in reversed(processes):
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait(timeout=5)
            for log in logs:
                log.close()


if __name__ == "__main__":
    main()
