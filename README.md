# SiteLink Scout

> Hardware-assisted Wi-Fi coverage validation system for dynamic construction sites.

**SiteLink Scout** is a field measurement component of **SiteLink**, a construction-site wireless coverage planning and validation system.

SiteLink plans candidate AP locations based on construction-space information, while SiteLink Scout measures the actual wireless environment in the field and compares real measurements with planned coverage.

## Core Concept

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
MVP Goals

The first prototype focuses on a simple end-to-end validation pipeline.

Wi-Fi RSSI scanning using ESP32
Target SSID / BSSID measurement
Multi-Scout telemetry
Zone-based measurement collection
Signal quality classification
Real-time Field Console
Coverage heatmap
RSSI history visualization
Dead-zone detection
Basic AP relocation recommendation
System Architecture
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
Tech Stack
Firmware
ESP32 DevKit V1
C++
Arduino Framework
PlatformIO
ESP32 Wi-Fi API
SSD1306 OLED
RGB / WS2812 Status LED
Backend
Python 3.12
FastAPI
Pydantic v2
SQLAlchemy 2.x
SQLite
Pytest
OpenAPI
Frontend
React
TypeScript
Vite
Tailwind CSS
TanStack Query
Recharts
Infrastructure
Docker Compose
GitHub Actions
Measurement Model

Example Scout telemetry:

{
  "device_id": "SCOUT-01",
  "zone_id": "ZONE-B03",
  "ssid": "SiteLink_AP_01",
  "bssid": "AA:BB:CC:DD:EE:FF",
  "rssi": -64,
  "channel": 6
}

Server reception time is used as the authoritative timestamp for the MVP.

RSSI Classification
RSSI	Status
>= -55 dBm	EXCELLENT
-56 ~ -65 dBm	GOOD
-66 ~ -75 dBm	FAIR
-76 ~ -85 dBm	POOR
<= -86 dBm	DEAD

These thresholds are prototype-level indicators and are not intended to represent universal construction-site communication requirements.

Future versions may additionally measure:

Packet loss
Latency
Jitter
Throughput
Channel utilization
Repository Structure
sitelink-scout/
├── firmware/
├── backend/
├── frontend/
├── hardware/
├── docs/
└── .github/workflows/
Prototype Target

The first prototype aims to demonstrate:

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
Project Status

Prototype / MVP Development

Target demonstration:

17th LH Land Technology Competition

License

License selection pending.
