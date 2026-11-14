# Project Origins — SiteLink Scout to SPATIALINK

## Original competition

**제17회 LH 국토기술대전**, **SiteLink — 공정 변화에 맞춘 건설현장 Wi-Fi 배치 기술**. SiteLink planned AP placement for changing construction phases; Scout was its field-measurement and prospective validation subsystem.

## Historical contributors (original README)

**이영준:** software/system integration, ESP32 firmware, FastAPI/SQLite, React field console, simulation and E2E workflow.  
**박하음:** construction-phase spatial analysis, wall/structure/temporary-facility conditions, CAD/BIM utilization direction, AP feasibility, priority zones, architectural interpretation and presentation spatial framing.

These are historical README attributions. New design deliverables are proposed separately.

## Proposal-stage simulation (not field measurement)

| Metric | Result |
|---|---|
| AP candidates | 454 |
| Additional APs | 0 |
| AP relocations | 1 |
| Relocation distance | ~6.3 m |
| Overall predicted coverage | 45.2% → 45.5% (+0.3%p) |
| Priority-zone predicted coverage | 76.0% → 79.1% (+3.1%p) |

The 3.1 percentage-point improvement is **simulation only**, not physically measured or independently validated.

## Preserved prototype scope

ESP32 DevKit V1 / ESP32-WROOM-32 (2.4 GHz only), RSSI/SSID/BSSID/channel telemetry, HTTP/JSON, FastAPI, SQLite, React, device and sampled-zone coverage APIs, boardless simulator, GitHub Actions and Pytest. Optional OLED, RGB LED, button, power bank and enclosure were hardware concepts.

RSSI classes: EXCELLENT ≥ -55, GOOD -56…-65, FAIR -66…-75, POOR -76…-85, DEAD ≤ -86 dBm. Usable sampled-zone threshold is ≥ -75 dBm. The coverage percentage reflects **latest sampled zones**, not continuous floor-plan coverage.

The original README recorded backend, frontend, simulator, firmware compilation and software E2E as completed prototype work, while physical USB detection, firmware upload, real scan, device-to-server E2E, obstacle experiment and RF model calibration remained pending. These historical claims are not fresh CI results.

## Original workflow

```bash
cd firmware
cp include/config.example.h include/config.h
python3 -m platformio run
cd ..
./scripts/detect_port.sh
./scripts/upload.sh
./scripts/monitor.sh
./scripts/start-demo.sh
./scripts/check-demo.sh
./scripts/simulate-demo.sh
./scripts/stop-demo.sh
```

ESP32 must use the backend host's LAN IP, not loopback. Keep `firmware/include/config.h` credentials out of Git.

## Evolution

- **SiteLink:** Where should APs be placed during construction?
- **Scout:** How can measurements validate placement predictions?
- **SPATIALINK:** How can architectural conditions and wireless measurements be studied and visualized together?

The rebrand changes documentation only; existing runtime names, code, API contracts and Git history remain unchanged.

## Future ideas retained

Latency, packet loss, jitter, throughput, channel utilization, predicted-versus-measured RSSI and calibration offset were future metrics, not current measured capabilities. The original architecture also discussed optional MQTT, WebSockets and a separate SiteLink Planner; none should be mistaken for implemented Scout services.

The verbatim original README remains accessible in Git history.
