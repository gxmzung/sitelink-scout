# SPATIALINK 시스템 구조

**시스템 개발:** 이영준 · **건축·UI 방향 검토:** 박하음

## 1. 현재 구현 구조

```text
ESP32 (2.4 GHz, C++/Arduino/PlatformIO) 또는 가상 시뮬레이터
      → HTTP/JSON → FastAPI/Pydantic/SQLAlchemy → SQLite
      → React/TypeScript/Vite 현장 콘솔
```

기존 SiteLink Planner의 AP 최적화 알고리즘은 별도 기획 계층이며 이 저장소에 구현된 기능이 아닙니다. 실행 중 서비스 식별자는 아직 SiteLink Scout를 사용합니다.

## 2. 현재 측정 데이터 계약

```json
{"device_id":"SCOUT-01","zone_id":"ZONE-B03","ssid":"SiteLink_AP_01","bssid":"AA:BB:CC:DD:EE:FF","rssi":-64,"channel":6}
```

`received_at`은 서버가 기록합니다.

| 메서드 | 구현된 경로 |
|---|---|
| GET | `/api/v1/health` |
| POST | `/api/v1/measurements` |
| GET | `/api/v1/measurements` |
| GET | `/api/v1/devices` |
| GET | `/api/v1/devices/{device_id}` |
| GET | `/api/v1/coverage` |

과거 문서에 언급된 `GET /api/v1/zones`, `GET /api/v1/devices/{device_id}/measurements`는 구현 여부 확인 전까지 사용 가능한 API로 표시하지 않습니다. 실제 구동 시 `/docs`를 확인합니다.

## 3. RSSI 분류

| RSSI(dBm) | 등급 |
|---|---|
| -55 이상 | EXCELLENT |
| -65 ~ -56 | GOOD |
| -75 ~ -66 | FAIR |
| -85 ~ -76 | POOR |
| -86 이하 | DEAD |

사용 가능 판정은 RSSI ≥ -75 dBm입니다. 구역 커버리지는 **측정된 각 구역의 최신 샘플**을 기준으로 계산합니다. DEAD는 미커버 구역의 부분집합입니다. 평면 전체 면적이나 연속 히트맵은 계산하지 않습니다.

## 4. 개발 환경 실행

Unix 계열 셸, curl, lsof, Python, Node/npm이 필요합니다. `backend/.venv`에 의존성을 설치하고 `frontend/`에서 npm 의존성을 설치해야 합니다.

```bash
./scripts/start-demo.sh
./scripts/simulate-demo.sh
./scripts/check-demo.sh
./scripts/stop-demo.sh
```

백엔드 8000, 프론트엔드 5173 포트를 사용합니다. 시뮬레이터는 10회 주기, 2초 간격으로 **가상** 데이터를 보냅니다.

독립된 SQLite DB를 사용하는 자동 통합 스모크:

```bash
python scripts/e2e-smoke.py
```

이 명령은 백엔드·프론트엔드 의존성 설치 후 사용하며, 서버·Vite 실제 기동과 API 흐름을 검증합니다. 브라우저 UI·ESP32 실물 측정까지 보장하지 않습니다.

## 5. ESP32 펌웨어

```bash
cd firmware
cp include/config.example.h include/config.h
python3 -m platformio run
cd ..
./scripts/detect_port.sh
./scripts/upload.sh
./scripts/monitor.sh
```

장치·구역 ID, SSID/BSSID, Wi-Fi 인증정보, API 주소를 로컬 설정에 입력합니다. ESP32에서 `127.0.0.1` 대신 서버 컴퓨터의 LAN IP를 사용합니다. 인증정보를 커밋하지 않습니다. OLED·RGB LED·케이스는 기존 하드웨어 구상이며 실물 업로드·측정 성공 증거는 별도 확보해야 합니다.

## 6. 배재대학교 공간 데이터 확장(미구현)

제안 엔터티: `FloorPlan`, `SpatialFeature`, `MeasurementPoint`, `Scenario`, `OccupancyObservation`, `AttenuationEstimate`.

제안 API: `POST /api/v1/floorplans`, `POST /api/v1/measurement-points`, `GET /api/v1/scenarios`. **현재 구현되지 않았습니다.**

측정점에 도면 버전·축척·좌표·시나리오·출처(`physical|synthetic|estimated`)·시각·BSSID를 연결하는 것이 우선입니다. 캠퍼스 실증 전 시설 이용 및 네트워크 관리 규정과 개인정보 보호 범위를 확인해야 합니다.

## 7. 초기 기술 선택

초기 MVP는 저빈도 HTTP/JSON 전송과 단순 폴링을 사용합니다. MQTT·WebSocket·Kafka·Kubernetes·Redis·Grafana·InfluxDB·ML 최적화는 현재 구현 범위가 아닙니다. [프로젝트 기원](project-origins.md) 참고.
