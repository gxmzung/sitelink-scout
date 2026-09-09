
SiteLink Scout — 7 Day Development Plan
Objective

Build a working end-to-end prototype within seven days:

ESP32
→ RSSI Measurement
→ FastAPI
→ SQLite
→ React Field Console
→ Coverage Visualization

The target is a reliable demonstration, not maximum feature count.

Day 1 — Architecture & Repository
Tasks
 Create repository
 Initialize project structure
 Define technology stack
 Define hardware architecture
 Write project documentation
 Configure PlatformIO
 Initialize FastAPI
 Initialize React/Vite
Exit Criteria
Firmware builds
GET /api/v1/health → 200
Frontend development server starts
Day 2 — ESP32 Wi-Fi Scanner
Tasks
 Scan Wi-Fi networks
 Filter target SSID
 Read RSSI
 Read BSSID
 Read channel
 Output measurements via Serial
 Display signal on OLED
 Add status LED
Exit Criteria

Physical Scout displays:

SCOUT-01
SiteLink_AP_01
-61 dBm
GOOD
Day 3 — Telemetry Backend
Tasks
 Implement measurement schema
 Implement POST /api/v1/measurements
 Configure SQLite
 Store measurements
 Implement device endpoint
 Connect ESP32 to FastAPI
Exit Criteria
ESP32
→ HTTP
→ FastAPI
→ SQLite

Real measurements persist successfully.

Day 4 — Field Console
Tasks
 Initialize dashboard
 Implement ScoutCard
 Implement SignalBadge
 Implement API client
 Add 2-second polling
 Display latest RSSI
 Display active devices
Exit Criteria

Moving the Scout changes the RSSI visible on the browser.

Day 5 — Multi-Scout & Coverage
Tasks
 Configure SCOUT-01
 Configure SCOUT-02
 Configure SCOUT-03
 Add zone IDs
 Implement CoverageHeatmap
 Implement coverage percentage
 Implement dead-zone count
 Add RSSI history
Exit Criteria

Three Scouts simultaneously appear in the Field Console.

Day 6 — Physical Demonstration
Tasks
 Build miniature site environment
 Establish baseline measurement
 Introduce wall / obstacle
 Measure degradation
 Detect poor/dead zone
 Move AP
 Measure recovery
 Implement recommendation card
Target Demonstration
Before obstacle
SCOUT-02 = -58 dBm
GOOD

After obstacle
SCOUT-02 = -79 dBm
POOR

AP relocated
SCOUT-02 = -63 dBm
GOOD
Day 7 — Freeze & Presentation
Rule

No new features.

Only:

bug fixes
reliability improvement
documentation
presentation
backup preparation
Tasks
 Full integration test
 Demo rehearsal
 Record backup demo video
 Finalize README
 Finalize presentation material
 Tag prototype release

Suggested release:

v0.1.0-demo
Priority

If schedule slips, development priority is:

1. ESP32 RSSI measurement
2. ESP32 → FastAPI transmission
3. Live browser visualization
4. Multi-Scout
5. Coverage heatmap
6. Recommendation
7. Visual polish

The first three items constitute the minimum successful prototype.
