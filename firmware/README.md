# SiteLink Scout Firmware

ESP32-based field measurement firmware for SiteLink Scout.

## Current Functions

- 2.4 GHz Wi-Fi scanning
- Target SSID / optional BSSID selection
- RSSI measurement
- Channel detection
- Signal-status classification
- HTTP JSON upload to FastAPI
- Scout / zone identification

## Hardware Target

- ESP32 DevKit V1
- ESP32-WROOM-32

Classic ESP32 targets 2.4 GHz Wi-Fi only.

## Configuration

Create the local configuration:

```bash
cp include/config.example.h include/config.h
Then configure:

SCOUT_DEVICE_ID
SCOUT_ZONE_ID
TARGET_SSID
TARGET_BSSID
WIFI_SSID
WIFI_PASSWORD
API_URL

config.h is intentionally excluded from Git.

Build
python3 -m platformio run
Detect Connected Board
./scripts/detect_port.sh
Upload
./scripts/upload.sh
Serial Monitor
./scripts/monitor.sh
Expected Physical E2E Output
[WiFi] Connected
[WiFi] ESP32 IP: 192.168.x.x

SiteLink Scout Measurement
Device: SCOUT-01
Zone: ZONE-B03
SSID: SiteLink_AP_01
BSSID: XX:XX:XX:XX:XX:XX
RSSI: -64 dBm
Channel: 6

[API] HTTP 201
[Scout] Upload: SUCCESS
Signal Classification
RSSI	Status
>= -55 dBm	EXCELLENT
-56 to -65 dBm	GOOD
-66 to -75 dBm	FAIR
-76 to -85 dBm	POOR
<= -86 dBm	DEAD

These thresholds are prototype indicators rather than universal RF requirements.

Validation Status

Firmware compilation has been verified.

Boardless software E2E can be validated with:

../scripts/simulate-demo.sh

Physical ESP32 upload and real RF measurement validation remain pending hardware connection.
