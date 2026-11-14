# SiteLink Scout / SPATIALINK 공개 사용 가이드

## 시작점
이 저장소의 **현재 main**은 SiteLink Scout이며, SPATIALINK 명칭·공동 기여·건축/RF 연구 방향으로 개편하는 작업은 [별도 Draft PR #1](https://github.com/gxmzung/sitelink-scout/pull/1)에 있습니다. 두 PR을 서로 다른 README로 덮어쓰지 않습니다.

## 외부 개발자가 직접 재현할 수 있는 최소 범위

```sh
cd backend
python -m venv .venv
# 가상환경 활성화 후
python -m pip install -r requirements.txt
python -m pytest -q
```

장비 없이 테스트하는 범위는 FastAPI 서비스/health 응답, 측정 생성·조회, 누락 또는 범위 밖의 RSSI·채널·필수 문자열 요청 거부입니다. 테스트는 FastAPI TestClient를 이용합니다. [계약 시험 소스](../backend/tests/test_api_contract_regression.py) 및 [검증 절차](BOARDLESS_REPRODUCIBILITY.md), [CI 이력](https://github.com/gxmzung/sitelink-scout/actions)를 확인하세요.

## 관측과 추정의 구분

| 항목 | 현재 이 PR에서 확인하는 것 | 이 PR만으로 주장할 수 없는 것 |
| --- | --- | --- |
| API | 요청/응답 계약 및 입력 유효성 | 실제 ESP32 무선 수신 |
| RSSI | 허용 범위 검증 | RSSI 정확도 및 교정 |
| 채널 | API 입력 유효성 | 주파수 혼잡 및 RF 커버리지 |
| AP 배치 | 없음 | 현장 설치 최적화 성능 |
| 건축 공간 분석 | 별도 PR의 설계 범위 | CAD/BIM 기반 실측 검증 |

기존 문서의 AP 후보 454개, 약 6.3m 이동, 우선구역 76.0→79.1% 수치는 **출품 당시 시뮬레이션**이며 현장 측정 결과가 아닙니다.

## 공개 준비 점검
- [x] 장비 없는 API 계약 검증 코드 준비
- [ ] 새 OS/가상환경에서 독립적으로 설치·실행한 로그 첨부
- [ ] SQLite 테스트용 DB를 임시 경로로 분리하고 결과 재현 확인
- [ ] 실측 데이터의 SSID/BSSID·장소 등 개인정보/보안정보 익명화
- [ ] SPATIALINK PR #1의 공동 기여 표기와 링크 최종 검토
- [ ] 실제 화면 캡처/영상 확보 후 README에 추가
- [ ] ESP32 펌웨어/보드와 RF 환경을 통제한 현장 검증 진행

**주의:** 장비 없는 검증 성공은 무선 실측 완료가 아닙니다. 실제 장비 또는 현장 결과가 없다면 결과 이미지도 모의/예시로 명시해야 합니다.
