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

## Configuration

Copy:

```bash
cp include/config.example.h include/config.h
Then edit:

SCOUT_DEVICE_ID
SCOUT_ZONE_ID
TARGET_SSID
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
Expected Serial Output
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
Validation Status

Firmware compilation has been verified.

Physical ESP32 upload and real RF measurement validation are pending hardware connection.
