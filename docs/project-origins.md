# 프로젝트 기원 — SiteLink Scout에서 SPATIALINK까지

## 1. 최초 대회 및 연구 범위

**제17회 LH 국토기술대전**에 제안한 **SiteLink — 공정 변화에 맞춘 건설현장 Wi-Fi 배치 기술**이 출발점입니다. SiteLink는 건설 단계 변화에 맞춘 AP 배치를 기획했으며, Scout는 현장 측정과 향후 검증을 위한 하위 시스템입니다.

## 2. 기존 README에 기록된 기여

- **이영준:** 소프트웨어·시스템 통합, ESP32 펌웨어, FastAPI·SQLite, React 현장 콘솔, 시뮬레이션 및 E2E 흐름
- **박하음:** 공정 단계별 공간 분석, 벽체·구조물·가설시설 조건, CAD/BIM 활용 방향, AP 설치 가능성, 우선구역, 건축적 해석과 발표의 공간적 구성

위 내용은 **기존 README의 역사적 기여 기록**입니다. 신규 AI 작성 디자인 시안은 박하음의 직접 작업이나 승인으로 간주하지 않습니다.

## 3. 제안 단계 시뮬레이션 — 실측 아님

| 지표 | 결과 |
|---|---|
| AP 후보 | 454개 |
| 추가 AP | 0개 |
| AP 재배치 | 1회 |
| 이동 거리 | 약 6.3m |
| 전체 예측 커버리지 | 45.2% → 45.5%(+0.3%p) |
| 우선구역 예측 커버리지 | 76.0% → 79.1%(+3.1%p) |

**+3.1%p는 시뮬레이션 결과**이며 배재대학교 현장 실측이나 독립 검증 결과가 아닙니다.

## 4. 보존한 기존 시제품

ESP32 DevKit V1 / ESP32-WROOM-32(2.4 GHz), RSSI·SSID·BSSID·채널 측정, HTTP/JSON, FastAPI, SQLite, React, 장치·측정 구역 커버리지 API, 가상 시뮬레이터, GitHub Actions, Pytest.

RSSI 등급: EXCELLENT(-55 이상), GOOD(-65~-56), FAIR(-75~-66), POOR(-85~-76), DEAD(-86 이하). 사용 가능 구역 기준은 -75 dBm 이상입니다. 이 커버리지 비율은 **측정된 구역의 최신값**을 집계한 것이지 연속 평면도 면적 커버리지가 아닙니다.

기존 README는 백엔드·프론트엔드·시뮬레이터·펌웨어 컴파일·소프트웨어 E2E를 시제품 작업으로 기록했습니다. 반면 USB 포트 인식, 펌웨어 업로드, 실물 Wi-Fi 스캔, 장치→서버 통합, 장애물 실험, RF 모델 보정은 미완료로 기록했습니다. 이는 당시의 기록이며 최신 실물 검증을 의미하지 않습니다.

## 5. 기존 명령

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

ESP32는 서버 PC의 LAN IP를 사용하며 `firmware/include/config.h`의 인증정보는 Git에 올리지 않습니다.

## 6. 연구 방향 전환

- **SiteLink:** 건설 공정 변화에 맞춰 AP를 어디에 배치할 것인가?
- **Scout:** 실제 측정으로 AP 배치 예측을 어떻게 검증할 것인가?
- **SPATIALINK:** 건축 조건과 무선 측정값을 어떻게 공간적으로 분석·표현할 것인가?

SPATIALINK의 **배재대학교 캠퍼스 1차 실증 계획**은 새 연구 방향이며, 기존 LH 대회에서 배재대 현장을 실측했다는 뜻이 아닙니다. 기존 코드·API·Git 이력은 유지합니다.

지연시간, 패킷 손실, 지터, 처리량, 채널 점유율, 예측 대비 실측 RSSI 및 보정 오프셋은 향후 지표입니다. MQTT·WebSocket·별도 Planner는 현재 Scout 구현 기능으로 표시하지 않습니다. 원본 README 전체는 Git 이력에서 확인할 수 있습니다.
