
SiteLink Scout BOM
Prototype Configuration

Recommended demonstration configuration:

3 × SiteLink Scout Node
1 × Wi-Fi Access Point
1 × Backend / Field Console PC

Three Scout nodes are recommended because multiple spatial measurements are necessary to demonstrate coverage distribution and a meaningful heatmap.

Scout Node BOM
Item	Qty / Node	Qty / 3 Nodes	Purpose
ESP32 DevKit V1	1	3	Main controller / Wi-Fi scanner
SSD1306 0.96" OLED	1	3	Local status display
WS2812 RGB LED or RGB LED	1	3	Signal status indicator
Push Button	1	3	Local control / manual measurement
Breadboard or prototype PCB	1	3	Assembly
Jumper wires	Set	Set	Wiring
USB cable	1	3	Power / programming
USB power bank	1	3	Portable operation
Enclosure	1	3	Physical prototype housing
Optional Parts
Item	Purpose
Buzzer	Warning feedback
Battery level module	Portable power monitoring
ESP32-S3	Future hardware revision
microSD module	Offline measurement buffering
Environmental sensor	Additional site telemetry
Access Point

For the first demonstration, a dedicated enterprise AP is not required.

Possible options:

existing Wi-Fi router
smartphone hotspot
portable router
spare wireless AP

A dedicated SSID such as:

SiteLink_AP_01

is recommended.

Demonstration Environment

Recommended physical demonstration:

Foam board / model wall
        +
3 Scout nodes
        +
1 movable AP

Scenario:

Establish initial AP position
Measure RSSI
Insert wall / obstacle
Observe RSSI degradation
Detect poor coverage
Relocate AP
Measure improvement
Prototype Limitations

ESP32 RSSI is suitable for demonstrating relative wireless signal changes but is not a calibrated RF measurement instrument.

The MVP must therefore be described as:

RSSI-based field coverage validation prototype

rather than:

precision RF surveying equipment
