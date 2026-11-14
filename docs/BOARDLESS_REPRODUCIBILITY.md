# SiteLink Scout: 장비 없는 API 재현성 검증

> 이 문서는 기존 `main` 브랜치의 FastAPI 계약에 대한 별도 검증입니다. 열려 있는 SPATIALINK 리브랜딩 PR #1의 파일은 변경하지 않습니다.

## 확인 가능한 것
- FastAPI 루트 응답과 `/api/v1/health`의 서비스 식별자
- 필수 필드 없는 측정 요청이 `422`로 거부되는지
- 기존 측정 생성/조회 테스트의 HTTP 동작

이 테스트들은 **ESP32 실측, RF 예측 정확도, 현장 AP 커버리지, CAD/BIM 연동을 검증하지 않습니다.**

## 환경
Python 3.11+ 및 별도 가상환경 권장. 저장소 루트에서 아래 명령을 실행합니다.

```sh
cd backend
python -m venv .venv
# PowerShell: .venv\Scripts\Activate.ps1
# bash: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

특정 계약만 재검증:
```sh
python -m pytest -q tests/test_api_contract_regression.py
```

## 기록 및 재현 조건
1. `git rev-parse HEAD`, `python --version`, `python -m pip freeze`를 기록합니다.
2. 테스트 성공/실패 수와 종료 코드, SQLite 데이터베이스 경로를 기록합니다.
3. 실험용 DB를 사용하고 팀의 실측 자료·비밀번호·개인정보를 커밋하지 않습니다.
4. 생성 테스트에서 DB 상태에 따라 결과가 달라진다면 테스트 격리/임시 DB를 후속 과제로 분리합니다.
5. 테스트 실패 시 CI도 함께 확인하고, 실패 원인을 해결하기 전에는 **검증 완료**로 표기하지 않습니다.

## 해석
`TestClient`는 서버 내부 호출 수준을 확인하며 실제 네트워크, 보드 펌웨어 및 무선 환경을 대체하지 않습니다. 제품 품질 향상을 위해 실측 자료의 수집 시점, SSID/BSSID 익명화, RSSI 단위, 예측값/관측값 구분을 추가로 검증해야 합니다.
