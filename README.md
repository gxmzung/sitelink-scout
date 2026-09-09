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
ESP32 Scout
     ↓ HTTP / JSON
FastAPI Backend
     ↓ REST API
SiteLink Field Console
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
{
  "device_id": "SCOUT-01",
  "zone_id": "ZONE-B03",
  "ssid": "SiteLink_AP_01",
  "bssid": "AA:BB:CC:DD:EE:FF",
  "rssi": -64,
  "channel": 6
}
RSSI Classification
RSSI	Status
>= -55 dBm	EXCELLENT
-56 to -65 dBm	GOOD
-66 to -75 dBm	FAIR
-76 to -85 dBm	POOR
<= -86 dBm	DEAD

These thresholds are prototype-level indicators, not universal construction-site RF requirements.

Repository Structure
sitelink-scout/
├── firmware/
├── backend/
├── frontend/
├── hardware/
├── docs/
└── .github/workflows/
Prototype Target
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

Target demonstration: 17th LH Land Technology Competition

License

License selection pending.
