# SiteLink Scout

> **제17회 LH 국토기술대전 출품 프로젝트**  
> **SiteLink — 공정 변화에 맞춘 건설현장 Wi-Fi 배치 기술**  
> Hardware-assisted Field Validation System

SiteLink Scout is a field measurement and validation subsystem developed for **SiteLink**, a construction-site Wi-Fi placement optimization concept submitted to the **제17회 LH 국토기술대전**.

The project addresses a simple but practical problem:

> **Construction sites change continuously, but Wi-Fi AP placement is often fixed.**

As walls, temporary structures, steel frames, equipment, materials, and work zones change during construction, the RF environment also changes.

SiteLink models those changes and recommends AP placement adjustments.

SiteLink Scout measures the actual field condition so those predictions can later be validated and calibrated.

---

## 1. Competition Overview

### Competition

**제17회 LH 국토기술대전**

### Project

**SiteLink — 공정 변화에 맞춘 건설현장 Wi-Fi 배치 기술**

### Project Goal

SiteLink aims to support Wi-Fi infrastructure decisions according to construction progress.

Instead of assuming that a fixed AP layout remains optimal throughout the entire construction period, SiteLink evaluates how the communication environment changes by phase and recommends minimal AP relocation or additional installation.

SiteLink Scout was developed as the validation layer of this concept.

The complete project flow is:

```text
Construction Progress
        ↓
Environment Change
        ↓
RF Condition Prediction
        ↓
AP Placement Optimization
        ↓
Field Measurement
        ↓
Prediction Validation
        ↓
Model Calibration
2. Problem Definition

Construction sites are not static environments.

As construction progresses:

walls are added
floors are partitioned
reinforced concrete structures appear
steel structures are installed
equipment locations change
material stacks move
temporary offices and barriers are added
important work zones change

These changes affect Wi-Fi propagation.

A Wi-Fi AP location that works well during one phase may produce weak or unusable coverage during another phase.

The practical challenge is therefore not simply:

"Where should an AP be installed?"

It is:

"How should AP placement change as the construction environment changes?"

3. Proposed Solution — SiteLink

SiteLink is the planning and optimization layer.

It is designed to use construction-phase information such as CAD/BIM-derived geometry and active structures to estimate RF conditions.

Conceptual flow:

Construction Phase
        ↓
CAD / BIM Environment
        ↓
Active Objects by Phase
        ↓
RF Propagation Estimation
        ↓
Weak / Dead Zone Prediction
        ↓
Priority Zone Evaluation
        ↓
Candidate AP Position Search
        ↓
Placement Optimization
        ↓
Recommended AP Adjustment

The optimization principle is not to maximize an abstract overall percentage at any cost.

Instead, SiteLink focuses on:

communication-critical zones
minimum AP relocation
minimum new AP installation
practical movement distance
explainable decision support
4. Priority-Zone Concept

Not every construction-site area has the same communication importance.

For example:

equipment operating zones
safety monitoring zones
control areas
temporary offices
inspection zones
logistics areas

may require more reliable communication than low-priority areas.

SiteLink therefore distinguishes between:

overall predicted coverage
priority-zone predicted coverage

This allows the system to optimize where communication quality matters most operationally.

5. Proposal-Stage Simulation Result

A proposal-stage SiteLink simulation evaluated:

454 candidate AP positions
0 additional APs
1 AP relocation
approximately 6.3 m relocation distance
Simulated Result
Metric	Before	After	Improvement
Overall predicted coverage	45.2%	45.5%	+0.3%p
Priority-zone predicted coverage	76.0%	79.1%	+3.1%p

The key result is:

Priority-zone predicted coverage improved by 3.1 percentage points without installing an additional AP.

The significance is not the small increase in overall coverage.

The important result is that SiteLink improved an operationally important area while minimizing infrastructure changes.

Validation Boundary

These values are simulation results.

They are not field-measured results.

SiteLink Scout is being developed specifically to provide the field validation required to compare prediction and reality.

6. Why SiteLink Scout?

A simulation result alone cannot prove that predicted RF conditions match a real environment.

RF behavior can differ because of:

construction materials
temporary structures
reflection
attenuation
interference
equipment
people
unmodeled obstacles
actual AP hardware

SiteLink Scout closes this validation gap.

Its role is:

SiteLink Prediction
        ↓
Recommended AP Placement
        ↓
Real Environment
        ↓
Scout Measurement
        ↓
Measured RSSI
        ↓
Prediction Error
        ↓
Future RF Model Calibration

SiteLink Scout therefore does not replace SiteLink.

It complements SiteLink.

SiteLink determines where an AP should be placed.

SiteLink Scout verifies whether that decision works in the field.

7. SiteLink Scout MVP

The SiteLink Scout MVP is a lightweight Wi-Fi field measurement node.

Primary functions:

target Wi-Fi scanning
SSID detection
optional BSSID targeting
RSSI measurement
Wi-Fi channel detection
Scout device identification
zone identification
HTTP JSON upload
backend storage
sampled-zone signal classification
frontend visualization

The MVP intentionally starts with RSSI as the first measurable RF indicator.

8. Hardware Concept

Planned Scout hardware:

ESP32 DevKit V1
ESP32-WROOM-32
OLED display
RGB LED
button
USB power bank
simple enclosure

Classic ESP32 hardware supports 2.4 GHz Wi-Fi only.

The current firmware target is therefore limited to 2.4 GHz measurement.

9. System Architecture
┌──────────────────────────┐
│     ESP32 Scout Node     │
│                          │
│  Wi-Fi Scan              │
│  RSSI                    │
│  SSID / BSSID            │
│  Channel                 │
└────────────┬─────────────┘
             │
             │ HTTP / JSON
             ▼
┌──────────────────────────┐
│      FastAPI Backend     │
│                          │
│  Measurement API         │
│  Device API              │
│  Coverage API            │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│         SQLite           │
│                          │
│  Measurement Storage     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│    React Field Console   │
│                          │
│  Scout Status            │
│  Latest Zone Samples     │
│  Signal Classification   │
│  Coverage Summary        │
└──────────────────────────┘

Boardless development replaces only the ESP32 device layer with a simulator.

The rest of the software path remains unchanged.

10. Measurement Flow

A physical Scout sends measurements in the following form:

{
  "device_id": "SCOUT-01",
  "zone_id": "ZONE-B03",
  "ssid": "SiteLink_AP_01",
  "bssid": "AA:BB:CC:DD:EE:FF",
  "rssi": -64,
  "channel": 6
}

Flow:

Scout
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

The backend uses the server receipt time as the authoritative timestamp.

11. Signal Classification

Prototype RSSI classification:

RSSI	Status
>= -55 dBm	EXCELLENT
-56 to -65 dBm	GOOD
-66 to -75 dBm	FAIR
-76 to -85 dBm	POOR
<= -86 dBm	DEAD

For the MVP:

usable sample = RSSI >= -75 dBm

These thresholds are prototype indicators.

They are not universal RF requirements for all construction sites.

12. Coverage Semantics

The current coverage metric is:

latest_zone_sample_coverage

Definitions:

total_zones
zones with at least one measurement
covered_zones
latest RSSI >= -75 dBm
uncovered_zones
latest RSSI < -75 dBm
dead_zones
latest signal classified as DEAD
coverage_percent
covered sampled zones / total sampled zones

Important:

This metric represents latest sampled-zone usability, not continuous spatial RF coverage.

The system does not yet calculate a full RF spatial heatmap from coordinates.

13. API
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
14. Technology Stack
Firmware
ESP32 DevKit V1
ESP32-WROOM-32
C++
Arduino Framework
PlatformIO
WiFi
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
Git
GitHub
GitHub Actions
Shell scripts
Scout simulator
15. Boardless Development

The current software system can be validated without a physical ESP32.

A Scout simulator sends measurements using the same API contract as the physical device.

Scout Simulator
        ↓
POST /api/v1/measurements
        ↓
FastAPI
        ↓
SQLite
        ↓
Coverage Logic
        ↓
React Field Console

This enables validation of:

API ingestion
database storage
device state
coverage calculation
frontend display
dynamic RSSI change behavior

before physical hardware arrives.

16. Run Demo

From the repository root:

./scripts/start-demo.sh

Check status:

./scripts/check-demo.sh

Open:

http://localhost:5173

Stop:

./scripts/stop-demo.sh

Run the boardless Scout simulation:

./scripts/simulate-demo.sh
17. Demo Scenario

The competition demonstration is based on a simple construction-phase change.

Initial State
AP ───────── Scout

Scout records a usable RSSI value.

Construction Change

A temporary wall or obstruction is introduced.

AP ─── Wall ─── Scout

The RSSI decreases.

The system then reflects the latest sampled-zone state as:

GOOD
FAIR
POOR
DEAD

depending on signal strength.

The goal is to visually demonstrate:

Construction Change
        ↓
RF Condition Change
        ↓
Scout Detection
        ↓
Zone Status Change
        ↓
AP Placement Review
18. Competition Demo Message

The demo should not be interpreted as a standalone RSSI meter.

The intended message is:

Construction progress changes the communication environment.

Therefore:

Communication infrastructure should be re-evaluated according to construction progress.

SiteLink provides the planning and optimization layer.

SiteLink Scout provides the field validation layer.

Together:

Predict
   ↓
Optimize
   ↓
Measure
   ↓
Validate
   ↓
Calibrate
   ↺
19. Firmware

Build:

cd firmware
python3 -m platformio run

Detect a connected device:

./scripts/detect_port.sh

Upload:

./scripts/upload.sh

Serial monitor:

./scripts/monitor.sh
20. Firmware Configuration

Create the local configuration file:

cd firmware
cp include/config.example.h include/config.h

Example:

#define SCOUT_DEVICE_ID "SCOUT-01"
#define SCOUT_ZONE_ID   "ZONE-B03"

#define TARGET_SSID "SiteLink_AP_01"
#define TARGET_BSSID ""

#define WIFI_SSID "YOUR_2_4GHZ_WIFI"
#define WIFI_PASSWORD "YOUR_WIFI_PASSWORD"

#define API_URL "http://192.168.x.x:8000/api/v1/measurements"

Do not use:

127.0.0.1

as the API address from the ESP32.

The ESP32 must use the backend computer's LAN IP.

firmware/include/config.h is excluded from Git.

21. Current Validation Status
Completed
FastAPI backend
SQLite measurement storage
measurement ingestion API
device API
sampled-zone coverage API
RSSI classification
uncovered vs DEAD semantic separation
automated backend tests
isolated test database
React Field Console
configurable frontend API endpoint
production frontend build
Scout simulator
boardless software E2E
demo lifecycle scripts
ESP32 firmware implementation
ESP32 firmware compilation
firmware upload / monitor workflow
GitHub Actions configuration
Pending Physical Hardware
ESP32 USB serial detection
real firmware upload
real 2.4 GHz Wi-Fi scan
real RSSI measurement
real BSSID validation
real channel validation
ESP32 → FastAPI HTTP E2E
physical obstacle before/after RF experiment
predicted RSSI vs measured RSSI comparison
RF model calibration
22. Physical Validation Plan

After the ESP32 is available:

ESP32 Firmware Upload
        ↓
Target 2.4 GHz AP Scan
        ↓
Real RSSI / BSSID / Channel
        ↓
HTTP POST
        ↓
FastAPI
        ↓
SQLite
        ↓
Field Console

The minimum physical MVP pass criteria are:

firmware uploads successfully
target AP is detected
real RSSI is measured
real BSSID is collected
real channel is collected
HTTP POST returns success
backend stores the measurement
frontend reflects the latest measurement
RSSI changes when the RF environment changes
23. Obstacle Experiment

A simple controlled RF test will compare measurements before and after adding an obstacle.

Before
AP ───────── Scout
After
AP ─── Obstacle ─── Scout

Record:

RSSI
signal status
channel
timestamp

Then calculate:

ΔRSSI = RSSI_after - RSSI_before

Example:

Before: -61 dBm
After:  -74 dBm

ΔRSSI = -13 dB

Multiple samples should be collected instead of relying on one measurement.

24. Prediction vs Measurement Calibration

The final objective of SiteLink Scout is not just signal monitoring.

It is prediction validation.

For each measurement point:

zone_id
position
predicted_rssi
measured_rssi
difference
obstacle_condition
AP_position
timestamp

Prediction error:

error = measured_rssi - predicted_rssi

This dataset can later be used to evaluate and calibrate the SiteLink RF prediction model.

25. Future Metrics

RSSI is intentionally used as the first MVP metric.

Future Scout measurements may include:

latency
packet loss
jitter
throughput
channel utilization
predicted RSSI
measured RSSI
prediction error
calibration offset

These additional metrics would allow SiteLink Scout to move from a signal-strength validation node toward broader communication-quality validation.

26. Project Scope

SiteLink Scout is intentionally designed as a focused MVP.

The goal is not to build a complete enterprise WLAN management platform.

The goal is to demonstrate a technically coherent construction-site communication loop:

Construction Environment Change
        ↓
Wi-Fi Condition Change
        ↓
RF Prediction
        ↓
AP Placement Decision
        ↓
Field Measurement
        ↓
Quantified Difference
        ↓
Prediction Validation
27. Validation Boundary

The following claims are currently supported:

boardless software E2E works
backend/frontend integration works
coverage semantics are implemented
Scout simulation works
ESP32 firmware compiles successfully

The following claims are not yet supported until physical testing is completed:

real construction-site RF accuracy
real measured +3.1%p improvement
physical Scout E2E completion
prediction-model accuracy
calibrated RF model performance

The +3.1%p priority-zone improvement belongs to the SiteLink proposal-stage simulation.

It must not be presented as a physical field measurement result.

28. Final Project Message

SiteLink Scout should not be understood as:

"an ESP32 that measures RSSI"

The intended concept is:

a field-validation node for a construction-phase-aware Wi-Fi placement optimization system

The relationship is simple:

SiteLink
  = Where should the AP be placed?

SiteLink Scout
  = Did that decision actually work?

Together, the project aims to create a practical construction-site communication decision-support system:

Construction Progress
        ↓
RF Environment Change
        ↓
Prediction
        ↓
AP Optimization
        ↓
Field Measurement
        ↓
Validation
        ↓
Calibration

