# SiteLink Scout Physical E2E Checklist

## Phase 1 — Hardware Inspection

- [ ] ESP32 DevKit V1 / ESP32-WROOM-32 확인
- [ ] USB data cable 준비
- [ ] 보드 전원 LED 확인
- [ ] Mac USB serial 장치 확인
- [ ] OLED / RGB LED는 기본 통신 검증 이후 연결

---

## Phase 2 — Serial Port Detection

Run:

```bash
cd firmware
./scripts/detect_port.sh
Expected example:

/dev/cu.usbserial-XXXX

Do not use:

/dev/cu.Bluetooth-Incoming-Port

If no USB serial port appears:

USB cable data capability 확인
다른 USB port / hub 확인
USB-UART chip 확인
CH340 / CP210x driver 필요 여부 확인
Phase 3 — Local Configuration

Create:

cp include/config.example.h include/config.h

Set:

#define SCOUT_DEVICE_ID "SCOUT-01"
#define SCOUT_ZONE_ID   "ZONE-B03"

#define TARGET_SSID "REAL_2_4GHZ_SSID"
#define TARGET_BSSID ""

#define WIFI_SSID "REAL_2_4GHZ_WIFI"
#define WIFI_PASSWORD "REAL_PASSWORD"

#define API_URL "http://MAC_LAN_IP:8000/api/v1/measurements"

Checks:

 TARGET SSID is 2.4 GHz
 transport Wi-Fi is accessible
 Mac and ESP32 are on reachable networks
 API URL does not contain 127.0.0.1
 config.h remains ignored by Git
Phase 4 — Backend Preparation

From repository root:

./scripts/start-demo.sh

Verify:

curl http://127.0.0.1:8000/api/v1/health

Expected:

{
  "status": "ok"
}

Find Mac LAN IP:

ipconfig getifaddr en0

If necessary:

ipconfig getifaddr en1

Verify backend listens externally:

lsof -nP -iTCP:8000 -sTCP:LISTEN

Expected:

*:8000
Phase 5 — Firmware Build
cd firmware
python3 -m platformio run

Required:

SUCCESS
Phase 6 — Firmware Upload
./scripts/upload.sh

Required:

SUCCESS

If connection fails:

verify correct serial port
press/hold BOOT if required
verify board type
retry upload
reduce upload speed only if necessary
Phase 7 — Serial Monitor
./scripts/monitor.sh

Expected:

SiteLink Scout
[WiFi] Connected
[WiFi] ESP32 IP: 192.168.x.x

Then:

Device: SCOUT-01
Zone: ZONE-B03
SSID: ...
BSSID: ...
RSSI: -XX dBm
Channel: X
Phase 8 — HTTP E2E

Required serial output:

[API] HTTP 201
[Scout] Upload: SUCCESS

Backend check:

curl -s \
  http://127.0.0.1:8000/api/v1/devices/SCOUT-01 \
  | python3 -m json.tool

Confirm:

 device_id is SCOUT-01
 zone_id is correct
 real BSSID appears
 RSSI is not simulator constant
 channel is real
 received_at updates after every scan
Phase 9 — Field Console E2E

Open:

http://localhost:5173

Confirm:

 SCOUT-01 appears
 RSSI changes over time
 signal status follows RSSI
 coverage summary updates
 latest zone timestamp updates
Phase 10 — Basic RF Experiment

Measurement A:

AP ↔ Scout
No additional obstacle

Record:

RSSI
status
channel
timestamp

Measurement B:

AP ↔ temporary wall ↔ Scout

Use foam board, wood panel, metal plate, or another controlled obstacle.

Record same metrics.

Calculate:

ΔRSSI = RSSI_after - RSSI_before

Example:

Before: -61 dBm
After:  -74 dBm

ΔRSSI = -13 dB

Repeat multiple times instead of relying on one sample.

Phase 11 — Physical MVP Pass Criteria

Physical SiteLink Scout MVP is considered validated when:

 ESP32 firmware uploads successfully
 target 2.4 GHz AP is detected
 real RSSI is measured
 real BSSID is collected
 real channel is collected
 ESP32 connects to transport Wi-Fi
 POST /measurements returns HTTP 201
 backend stores the measurement
 device endpoint updates
 coverage endpoint updates
 Field Console displays the measurement
 RSSI changes when RF conditions change
Phase 12 — SiteLink Calibration Preparation

For each controlled measurement point record:

zone_id
position
predicted_rssi
measured_rssi
difference
obstacle_condition
AP position
timestamp

Error:

error = measured_rssi - predicted_rssi

This dataset will later be used to evaluate and calibrate the SiteLink RF prediction model.

Physical Validation Boundary

Before physical validation, do not claim:

real construction-site coverage improvement
measured 3.1%p priority-zone improvement
real RF model accuracy
physical ESP32 E2E completion

The 3.1%p result belongs to the SiteLink simulation.

Scout physical measurements will be used to validate future prediction accuracy.
