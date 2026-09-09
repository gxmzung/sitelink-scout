# SiteLink Scout — Project Specification

> Hardware-assisted Wi-Fi coverage validation system for dynamic construction sites.

## 1. Project Overview

**SiteLink Scout** is a field measurement and validation component of **SiteLink**, a construction-site wireless coverage planning system.

SiteLink plans candidate AP locations using construction-space information such as CAD/BIM and construction phase data. SiteLink Scout then measures the actual wireless environment in the field and compares real measurements with planned coverage.

The MVP focuses on an end-to-end validation loop:

```text
Construction Plan / CAD-BIM
        ↓
SiteLink Coverage Planning
        ↓
Recommended AP Placement
        ↓
Physical AP Deployment
        ↓
SiteLink Scout Measurement
        ↓
Measured vs Planned Coverage
        ↓
Dead Zone Detection
        ↓
AP Relocation Recommendation
```

## 2. MVP Goals

- Wi-Fi RSSI scanning using ESP32
- Target SSID / BSSID measurement
- Multi-Scout telemetry
- Zone-based measurement collection
- Signal quality classification
- Real-time Field Console
- Coverage heatmap
- RSSI history visualization
- Dead-zone detection
- Basic AP relocation recommendation

## 3. System Architecture

```text
┌──────────────────────┐
│   SiteLink Scout     │
│      ESP32           │
│                      │
│ Wi-Fi Scanner        │
│ RSSI Measurement     │
│ OLED Display         │
│ Status LED           │
└──────────┬───────────┘
           │
           │ HTTP / JSON
           ▼
┌──────────────────────┐
│   FastAPI Backend    │
│                      │
│ Measurement API      │
│ Device Management    │
│ Signal Analysis      │
│ Coverage Calculation │
│ SQLite               │
└──────────┬───────────┘
           │
           │ REST API
           ▼
┌──────────────────────┐
│ SiteLink Field       │
│ Console              │
│                      │
│ React + TypeScript   │
│ Scout Status         │
│ Coverage Heatmap     │
│ RSSI History         │
│ Recommendations      │
└──────────────────────┘
```

## 4. Tech Stack

### Firmware

- ESP32 DevKit V1
- C++
- Arduino Framework
- PlatformIO
- ESP32 Wi-Fi API
- SSD1306 OLED
- RGB / WS2812 Status LED

### Backend

- Python 3.12
- FastAPI
- Pydantic v2
- SQLAlchemy 2.x
- SQLite
- Pytest
- OpenAPI

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- TanStack Query
- Recharts

### Infrastructure

- Docker Compose
- GitHub Actions

## 5. Design Principle

The MVP intentionally prioritizes:

```text
Measurement Reliability
        >
End-to-End Integration
        >
Demonstrability
        >
Architectural Complexity
```

Technologies intentionally deferred from the first prototype:

- Kafka
- Kubernetes
- Redis
- Grafana
- InfluxDB
- WebSocket infrastructure
- ML-based optimization

The first prototype should prove the data path, not architectural complexity.

## 6. Device Layer

### Hardware

Initial Scout hardware:

- ESP32 DevKit V1
- SSD1306 0.96" OLED
- RGB LED or WS2812
- Push Button
- USB power supply / power bank
- Prototype board or breadboard
- Enclosure

### Responsibilities

Each Scout:

1. scans nearby Wi-Fi networks
2. locates the configured target SSID/BSSID
3. obtains RSSI
4. reads the Wi-Fi channel
5. classifies signal quality
6. displays the current result locally
7. sends the measurement to the backend

Example local display:

```text
SCOUT-01
ZONE-B03
AP: SiteLink_AP_01
RSSI: -64 dBm
STATUS: GOOD
```

## 7. Measurement Model

Example Scout telemetry:

```json
{
  "device_id": "SCOUT-01",
  "zone_id": "ZONE-B03",
  "ssid": "SiteLink_AP_01",
  "bssid": "AA:BB:CC:DD:EE:FF",
  "rssi": -64,
  "channel": 6
}
```

For the MVP, server reception time is the authoritative timestamp.

Core measurement fields:

```text
id
device_id
zone_id
ssid
bssid
rssi
channel
received_at
```

## 8. RSSI Classification

| RSSI | Status |
|---|---|
| >= -55 dBm | EXCELLENT |
| -56 to -65 dBm | GOOD |
| -66 to -75 dBm | FAIR |
| -76 to -85 dBm | POOR |
| <= -86 dBm | DEAD |

For the MVP coverage calculation:

```text
usable = RSSI >= -75 dBm
```

Example:

```text
16 usable cells
20 total cells

Coverage = 16 / 20 × 100
         = 80%
```

These thresholds are prototype-level indicators, not universal RF acceptance criteria.

Future versions may additionally measure:

- packet loss
- latency
- jitter
- throughput
- channel utilization

## 9. Communication

### MVP Protocol

```text
HTTP REST + JSON
```

Reasons:

- simple to implement
- simple to debug
- easy to demonstrate
- native FastAPI compatibility
- sufficient for low-rate telemetry

MQTT can be evaluated after the MVP.

## 10. Backend API

Primary API endpoints:

```text
GET  /api/v1/health
POST /api/v1/measurements
GET  /api/v1/devices
GET  /api/v1/devices/{device_id}
GET  /api/v1/devices/{device_id}/measurements
GET  /api/v1/zones
GET  /api/v1/coverage
```

## 11. Field Console

The SiteLink Field Console should show:

- total coverage
- average RSSI
- active Scout count
- dead-zone count
- Scout status cards
- zone heatmap
- RSSI history
- AP relocation recommendation

MVP refresh strategy:

```text
HTTP polling every 2 seconds
```

## 12. Repository Structure

```text
sitelink-scout/
├── README.md
├── .gitignore
├── .env.example
├── docker-compose.yml
│
├── firmware/
│   ├── platformio.ini
│   ├── include/
│   │   ├── config.example.h
│   │   ├── measurement.h
│   │   └── status.h
│   └── src/
│       ├── main.cpp
│       ├── wifi_scanner.cpp
│       ├── display.cpp
│       └── api_client.cpp
│
├── backend/
│   ├── pyproject.toml
│   ├── README.md
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   └── services/
│   └── tests/
│
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── api/
│       ├── components/
│       ├── pages/
│       └── types/
│
├── hardware/
│   ├── BOM.md
│   ├── wiring.md
│   └── enclosure/
│
├── docs/
│   ├── project-spec.md
│   ├── architecture.md
│   ├── api.md
│   ├── demo-scenario.md
│   ├── development-plan.md
│   ├── presentation.md
│   └── roadmap.md
│
└── .github/
    └── workflows/
        ├── backend.yml
        └── frontend.yml
```

## 13. BOM

### Prototype Configuration

Recommended demonstration configuration:

```text
3 × SiteLink Scout Node
1 × Wi-Fi Access Point
1 × Backend / Field Console PC
```

Three Scout nodes are recommended because spatial distribution becomes visible only when multiple points are measured simultaneously.

### Scout Node BOM

| Item | Qty / Node | Qty / 3 Nodes | Purpose |
|---|---:|---:|---|
| ESP32 DevKit V1 | 1 | 3 | Main controller / Wi-Fi scanner |
| SSD1306 0.96" OLED | 1 | 3 | Local status display |
| WS2812 RGB LED or RGB LED | 1 | 3 | Signal status indicator |
| Push Button | 1 | 3 | Local control |
| Breadboard or prototype PCB | 1 | 3 | Assembly |
| Jumper wires | Set | Set | Wiring |
| USB cable | 1 | 3 | Power / programming |
| USB power bank | 1 | 3 | Portable operation |
| Enclosure | 1 | 3 | Prototype housing |

### Optional Parts

| Item | Purpose |
|---|---|
| Buzzer | Warning feedback |
| Battery level module | Portable power monitoring |
| ESP32-S3 | Future hardware revision |
| microSD module | Offline measurement buffering |
| Environmental sensor | Additional site telemetry |

## 14. Demonstration Environment

Recommended physical demonstration:

```text
Foam board / model wall
        +
3 Scout nodes
        +
1 movable AP
```

Scenario:

1. establish initial AP position
2. measure baseline RSSI
3. insert a wall or obstacle
4. observe RSSI degradation
5. detect poor/dead zone
6. relocate AP
7. measure improvement

Example target behavior:

```text
Before obstacle
SCOUT-02 = -58 dBm
GOOD

After obstacle
SCOUT-02 = -79 dBm
POOR

AP relocated
SCOUT-02 = -63 dBm
GOOD
```

## 15. Prototype Limitations

ESP32 RSSI is suitable for demonstrating relative wireless signal changes but is not a calibrated RF measurement instrument.

The MVP should be described as:

> RSSI-based field coverage validation prototype

rather than:

> precision RF surveying equipment

## 16. 7-Day Development Plan

### Day 1 — Architecture & Repository

Tasks:

- [x] Create repository
- [x] Initialize project structure
- [x] Define technology stack
- [x] Define hardware architecture
- [x] Write project documentation
- [ ] Configure PlatformIO
- [ ] Initialize FastAPI
- [ ] Initialize React/Vite

Exit criteria:

```text
Firmware builds
GET /api/v1/health → 200
Frontend development server starts
```

### Day 2 — ESP32 Wi-Fi Scanner

Tasks:

- [ ] Scan Wi-Fi networks
- [ ] Filter target SSID
- [ ] Read RSSI
- [ ] Read BSSID
- [ ] Read channel
- [ ] Serial output
- [ ] OLED status
- [ ] Status LED

Exit criteria:

```text
SCOUT-01
SiteLink_AP_01
-61 dBm
GOOD
```

### Day 3 — Telemetry Backend

Tasks:

- [ ] Implement measurement schema
- [ ] Implement POST `/api/v1/measurements`
- [ ] Configure SQLite
- [ ] Store measurements
- [ ] Implement device endpoint
- [ ] Connect ESP32 to FastAPI

Exit criteria:

```text
ESP32
→ HTTP
→ FastAPI
→ SQLite
```

### Day 4 — Field Console

Tasks:

- [ ] Initialize dashboard
- [ ] Implement ScoutCard
- [ ] Implement SignalBadge
- [ ] Implement API client
- [ ] Add 2-second polling
- [ ] Display latest RSSI
- [ ] Display active devices

Exit criteria:

> Moving the Scout changes RSSI visible in the browser.

### Day 5 — Multi-Scout & Coverage

Tasks:

- [ ] Configure SCOUT-01
- [ ] Configure SCOUT-02
- [ ] Configure SCOUT-03
- [ ] Add zone IDs
- [ ] Implement CoverageHeatmap
- [ ] Implement coverage percentage
- [ ] Implement dead-zone count
- [ ] Add RSSI history

Exit criteria:

> Three Scouts simultaneously appear in the Field Console.

### Day 6 — Physical Demonstration

Tasks:

- [ ] Build miniature site environment
- [ ] Establish baseline measurement
- [ ] Introduce wall / obstacle
- [ ] Measure degradation
- [ ] Detect poor/dead zone
- [ ] Move AP
- [ ] Measure recovery
- [ ] Implement recommendation card

### Day 7 — Freeze & Presentation

Rule:

**No new features.**

Only:

- bug fixes
- reliability improvement
- documentation
- presentation
- backup preparation

Tasks:

- [ ] Full integration test
- [ ] Demo rehearsal
- [ ] Record backup demo video
- [ ] Finalize README
- [ ] Finalize presentation material
- [ ] Tag prototype release

Suggested release:

```text
v0.1.0-demo
```

## 17. Development Priority

If the schedule slips:

```text
1. ESP32 RSSI measurement
2. ESP32 → FastAPI transmission
3. Live browser visualization
4. Multi-Scout
5. Coverage heatmap
6. Recommendation
7. Visual polish
```

The first three items constitute the minimum successful prototype.

## 18. GitHub Issue Plan

Suggested issues:

```text
#1 Initialize monorepo
#2 Implement ESP32 Wi-Fi scanner
#3 Add SSD1306 status display
#4 Implement Scout measurement API
#5 Store measurements in SQLite
#6 Implement RSSI classification
#7 Build Field Console dashboard
#8 Implement coverage heatmap
#9 Add multi-Scout support
#10 Build physical demo environment
#11 Prepare presentation demo
```

## 19. Branch Strategy

Keep the repository simple for the one-week MVP:

```text
main
├── feat/firmware-scanner
├── feat/backend-measurements
├── feat/field-console
└── docs/demo
```

Suggested commits:

```text
feat: implement ESP32 Wi-Fi RSSI scanner
feat: add Scout measurement ingestion API
feat: add real-time Scout status dashboard
feat: visualize zone coverage heatmap
```

## 20. Prototype Target

```text
ESP32
  ↓
Real RSSI Measurement
  ↓
FastAPI
  ↓
SQLite
  ↓
React Field Console
  ↓
Coverage / Dead Zone Visualization
```

## 21. Project Status

**Prototype / MVP Development**

Target demonstration: **17th LH Land Technology Competition**
