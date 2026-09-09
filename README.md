# SiteLink Scout

> Hardware-assisted Wi-Fi coverage validation system for dynamic construction sites.

SiteLink Scout is a field measurement and validation companion for **SiteLink**, a construction-site Wi-Fi placement optimization concept.

Construction sites continuously change as walls, temporary structures, equipment, and work zones are added or removed. SiteLink models those changes and recommends Wi-Fi AP placement adjustments, while SiteLink Scout collects field measurements so predicted radio conditions can later be compared with real observations.

---

## 1. Project Goal

SiteLink Scout provides a lightweight field validation layer for construction-site Wi-Fi planning.

The MVP focuses on:

- collecting Wi-Fi RSSI from designated measurement zones
- identifying the target SSID / BSSID / channel
- sending measurements to a backend API
- storing field samples
- classifying signal quality
- visualizing the latest sampled-zone condition
- supporting repeatable boardless demonstrations before hardware validation
- preparing predicted-vs-measured RF calibration workflows

The current coverage metric represents **latest sampled-zone usability**, not continuous RF spatial coverage.

---

## 2. Why SiteLink Scout?

A Wi-Fi placement simulation alone cannot prove that predicted radio conditions match the real construction environment.

Construction sites contain dynamic RF obstacles such as:

- temporary walls
- reinforced concrete
- steel structures
- equipment
- material stacks
- changing floor layouts

SiteLink Scout is designed to close the loop:

```text
SiteLink RF Prediction
        ↓
Recommended AP Placement
        ↓
Field Measurement
        ↓
SiteLink Scout
        ↓
Predicted vs Measured RSSI
        ↓
Model Calibration
3. System Architecture
┌──────────────────────┐
│  ESP32 Scout Node    │
│                      │
│  Wi-Fi Scan          │
│  RSSI / Channel      │
│  SSID / BSSID        │
└──────────┬───────────┘
           │
           │ HTTP / JSON
           ▼
┌──────────────────────┐
│  FastAPI Backend     │
│                      │
│  Measurement API     │
│  Device API          │
│  Coverage API        │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│      SQLite          │
│  Measurement Store   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│ React Field Console  │
│                      │
│ Latest Zone Samples  │
│ Signal Status        │
│ Coverage Summary     │
└──────────────────────┘

Boardless development can replace the physical ESP32 layer with the included Scout simulator.

4. Technology Stack
Firmware
ESP32 DevKit V1 / ESP32-WROOM-32
C++
Arduino Framework
PlatformIO
Wi-Fi scanning
HTTPClient
Backend
Python
FastAPI
Pydantic
SQLAlchemy
SQLite
Pytest
OpenAPI / Swagger
Frontend
React
TypeScript
Vite
Development
GitHub
GitHub Actions
Shell-based demo lifecycle scripts
5. Measurement Model

Example payload:

{
  "device_id": "SCOUT-01",
  "zone_id": "ZONE-B03",
  "ssid": "SiteLink_AP_01",
  "bssid": "AA:BB:CC:DD:EE:01",
  "rssi": -64,
  "channel": 6
}

The backend uses the server receipt time as the authoritative measurement timestamp.

6. Signal Classification

Prototype RSSI classification:

RSSI	Status
>= -55 dBm	EXCELLENT
-56 to -65 dBm	GOOD
-66 to -75 dBm	FAIR
-76 to -85 dBm	POOR
<= -86 dBm	DEAD

For the MVP, a sampled zone is treated as usable when:

RSSI >= -75 dBm

These thresholds are prototype indicators and should not be interpreted as universal construction-site RF requirements.

7. Coverage Metric

The current API exposes:

metric = latest_zone_sample_coverage

Definitions:

total_zones — zones with measurements
covered_zones — latest RSSI >= -75 dBm
uncovered_zones — latest RSSI < -75 dBm
dead_zones — latest signal classified as DEAD
coverage_percent — covered sampled zones / total sampled zones

This is intentionally described as sampled-zone coverage.

It is not yet a continuous RF heatmap or spatial coverage calculation.

8. API
Health
GET /api/v1/health
Measurements
POST /api/v1/measurements
GET  /api/v1/measurements
Devices
GET /api/v1/devices
GET /api/v1/devices/{device_id}
Coverage
GET /api/v1/coverage

Swagger:

http://127.0.0.1:8000/docs
9. Run the Software Demo

Start the complete demo stack:

./scripts/start-demo.sh

Check system health:

./scripts/check-demo.sh

Open the Field Console:

http://localhost:5173

Stop the demo:

./scripts/stop-demo.sh
10. Boardless Scout Simulation

A physical ESP32 is not required for software E2E testing.

Run:

./scripts/simulate-demo.sh

The simulator generates Scout measurements and sends them through the same backend API used by the physical device.

Flow:

Scout Simulator
      ↓
POST /api/v1/measurements
      ↓
FastAPI
      ↓
SQLite
      ↓
Coverage / Device API
      ↓
React Field Console

This allows backend, frontend, coverage semantics, and telemetry flow to be validated before hardware arrival.

11. Firmware

Build:

cd firmware
python3 -m platformio run

Detect a connected ESP32:

./scripts/detect_port.sh

Upload:

./scripts/upload.sh

Serial monitor:

./scripts/monitor.sh

Classic ESP32 hardware supports 2.4 GHz Wi-Fi only.

12. Firmware Configuration

Create:

cd firmware
cp include/config.example.h include/config.h

Configure:

#define SCOUT_DEVICE_ID "SCOUT-01"
#define SCOUT_ZONE_ID   "ZONE-B03"

#define TARGET_SSID "SiteLink_AP_01"
#define TARGET_BSSID ""

#define WIFI_SSID "YOUR_2_4GHZ_WIFI"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

#define API_URL "http://192.168.x.x:8000/api/v1/measurements"

Do not use 127.0.0.1 as the API address from the ESP32.

The device must use the Mac/backend LAN IP.

firmware/include/config.h is excluded from Git.

13. Current Validation Status
Completed
FastAPI backend
SQLite measurement storage
measurement ingestion
device status API
sampled-zone coverage API
RSSI classification
uncovered vs dead semantic separation
backend automated tests
isolated test database
React Field Console
production frontend build
configurable frontend API endpoint
Scout software simulator
boardless software E2E
demo start / check / stop workflow
ESP32 firmware compilation
firmware upload / monitor workflow
GitHub Actions configuration
Pending Physical Hardware
ESP32 USB serial detection
real firmware upload
real 2.4 GHz scan
real RSSI measurement
real BSSID / channel validation
ESP32 → FastAPI HTTP E2E
physical obstacle before/after RF experiment
prediction vs measurement calibration
14. SiteLink Relationship

SiteLink Scout does not replace the original SiteLink optimization concept.

SiteLink:

Construction Phase / BIM / CAD
        ↓
RF Environment Model
        ↓
Candidate AP Positions
        ↓
Placement Optimization
        ↓
Recommended AP Adjustment

SiteLink Scout:

Recommended / Existing AP
        ↓
Real Construction Environment
        ↓
RSSI Measurement
        ↓
Validation
        ↓
Prediction Calibration

Together:

Predict → Optimize → Measure → Validate → Calibrate
15. Example SiteLink Simulation Result

A proposal-stage simulated scenario evaluated 454 candidate positions.

Example result:

new AP: 0
AP relocation: 1
relocation distance: approximately 6.3 m
overall predicted coverage: 45.2% → 45.5%
priority-zone predicted coverage: 76.0% → 79.1%

The primary result is the +3.1 percentage-point improvement in the priority zone without adding a new AP.

These figures are simulation results and are not presented as field validation results.

16. Future Metrics

RSSI is intentionally used as the first MVP metric.

Future measurement expansion may include:

latency
packet loss
jitter
throughput
channel utilization
predicted RSSI
measured RSSI
prediction error
calibration offset
17. MVP Principle

SiteLink Scout is currently designed as a focused validation MVP.

The goal is not to build a complete enterprise WLAN platform.

The goal is to demonstrate a technically coherent loop:

Construction Environment Change
        ↓
Wi-Fi Condition Change
        ↓
Field Measurement
        ↓
Quantified Signal Difference
        ↓
AP Placement Decision Support

