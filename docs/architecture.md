# SPATIALINK — System Architecture

**Engineering:** 이영준 · **Spatial/UX Direction:** 박하음

## Implemented system

```text
ESP32 (2.4 GHz, C++/Arduino/PlatformIO) or boardless simulator
   → HTTP/JSON → FastAPI/Pydantic/SQLAlchemy → SQLite
   → React/TypeScript/Vite field console
```

The original SiteLink Planner AP optimization algorithm is a separate conceptual planning layer, **not** an implemented component of this Scout repository. Runtime service names remain SiteLink Scout until code is separately rebranded.

## Existing measurement contract

```json
{"device_id":"SCOUT-01","zone_id":"ZONE-B03","ssid":"SiteLink_AP_01","bssid":"AA:BB:CC:DD:EE:FF","rssi":-64,"channel":6}
```

The server sets `received_at`.

| Method | Endpoint |
|---|---|
| GET | /api/v1/health |
| POST | /api/v1/measurements |
| GET | /api/v1/measurements |
| GET | /api/v1/devices |
| GET | /api/v1/devices/{device_id} |
| GET | /api/v1/coverage |

Historical design proposals also mentioned `GET /api/v1/devices/{device_id}/measurements` and `GET /api/v1/zones`; verify router implementations before treating them as available. The running `/docs` OpenAPI page is authoritative.

## RSSI and coverage

| RSSI dBm | Class |
|---|---|
| ≥ -55 | EXCELLENT |
| -65…-56 | GOOD |
| -75…-66 | FAIR |
| -85…-76 | POOR |
| ≤ -86 | DEAD |

`usable = RSSI >= -75 dBm`. Coverage counts latest usable samples among zones that have samples. `dead_zones` are a subset of uncovered zones. **No continuous spatial coverage or calibrated heatmap is implemented.**

## Local run

Prepare Python environment at `backend/.venv` with the repository backend dependencies and install npm dependencies in `frontend/`. Requires a Unix-like shell, curl, lsof, Python and Node/npm.

```bash
./scripts/start-demo.sh
./scripts/simulate-demo.sh
./scripts/check-demo.sh
./scripts/stop-demo.sh
```

The start script uses backend port 8000 and frontend port 5173. The simulator sends synthetic samples in dynamic mode (10 cycles, 2-second interval). This verifies software integration, not real RF performance.

## Firmware

```bash
cd firmware
cp include/config.example.h include/config.h
python3 -m platformio run
cd ..
./scripts/detect_port.sh
./scripts/upload.sh
./scripts/monitor.sh
```

Configure device/zone ID, target SSID/BSSID, Wi-Fi credentials and API_URL in the local config. Use the backend computer's LAN IP, not `127.0.0.1` from ESP32. Never commit credentials. OLED, RGB LED and enclosure are historical hardware concepts; physical upload and end-to-end testing remain to be evidenced.

## Planned spatial layer (not implemented)

Entities: FloorPlan, SpatialFeature, MeasurementPoint, Scenario, OccupancyObservation, AttenuationEstimate. Proposed endpoints: `POST /api/v1/floorplans`, `POST /api/v1/measurement-points`, `GET /api/v1/scenarios`. Each measurement should link floor coordinates, plan scale, scenario, source (`physical|synthetic|estimated`), timestamp and BSSID.

Privacy: avoid exposing private SSIDs/BSSIDs or identifiable occupancy records. Restrict measurement ingestion in deployments.

## Original design considerations

The initial design favored low-rate HTTP/JSON telemetry and simple polling over MQTT/WebSockets. Kafka, Kubernetes, Redis, Grafana, InfluxDB and ML-based optimization were intentionally excluded from the MVP. See [Project Origins](project-origins.md).
