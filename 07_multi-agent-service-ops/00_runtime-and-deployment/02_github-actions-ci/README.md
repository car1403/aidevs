# 02 GitHub Actions CI

Multi-LLM Compose 변경을 Push하거나 Pull Request로 보낼 때 다음을 자동 검사합니다.

```text
Checkout
→ Python 3.12
→ Fake Client 기반 Backend 테스트
→ Compose 문법 검사
→ Frontend·Backend Image Build
```

실제 LLM·Redis·PostgreSQL과 AWS는 CI에서 호출하지 않습니다. 실제 실행 코드는 Provider를 사용하지만 자동 테스트는 비용 없는 Fake Client로 계약만 검사합니다.

실제 Workflow는 저장소 루트 `.github/workflows/07-runtime-ci.yml`에 둡니다.

## CI와 배포의 차이

CI는 변경한 코드가 합쳐질 수 있는 상태인지 자동 검사합니다. 배포는 검증된 코드를
실행 환경에 반영합니다. 이 단계에서는 AWS에 접속하거나 서비스를 변경하지 않습니다.

| 단계 | 확인할 질문 | 외부 환경 변경 |
| --- | --- | --- |
| Test | 계약과 API 동작이 유지되는가? | 없음 |
| Compose 검사 | 설정과 환경 변수 참조가 유효한가? | 없음 |
| Image Build | Dockerfile로 Image를 만들 수 있는가? | CI 내부 Image만 생성 |
| Deploy | 실행 서버에 새 버전을 반영하는가? | 있음, 이 단원에서는 제외 |

## Workflow를 읽는 순서

루트의 `.github/workflows/07-runtime-ci.yml`에서 다음 항목을 순서대로 찾습니다.

1. `name`: Actions 화면에 표시되는 이름
2. `on`: Push와 Pull Request 중 언제 실행하는지
3. `permissions`: Workflow의 최소 저장소 권한
4. `jobs`: 서로 독립적인 검사 묶음
5. `steps`: 로컬 명령을 실행하는 순서

각 Step은 로컬에서 실행한 `pytest`, `docker compose config`, `docker compose build`를
깨끗한 Runner에서 다시 실행하는 과정입니다.

## 로컬 확인

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose
python -m pip install -r backend\requirements.txt
python -m pip install pytest
python -m pytest backend\test_app.py -q
docker compose config --quiet
docker compose build
```

위 명령을 모두 통과시킨 뒤 Push합니다. 로컬에서 실패하는 Test를 CI가 고쳐주지는
않습니다.

## GitHub에서 결과 확인

1. 저장소의 `Actions` 탭에서 `07 Runtime CI`를 선택합니다.
2. 최근 실행의 Commit과 Branch가 본인 작업과 일치하는지 확인합니다.
3. 실패한 Job을 열고 빨간색으로 표시된 첫 Step을 찾습니다.
4. Log 마지막 줄만 보지 말고 최초 오류와 실행 명령을 확인합니다.

| 실패 Step | 먼저 확인할 내용 |
| --- | --- |
| Dependency 설치 | requirements 경로·Python 버전·패키지 이름 |
| Backend Test | 첫 Assertion·Import 경로·계약 변경 |
| Compose config | YAML 들여쓰기·누락 환경 변수·파일 경로 |
| Image Build | COPY 경로·requirements·Base Image |

수정 후 새 Commit을 Push하면 새 실행이 만들어집니다. 이전 실패를 성공처럼 취급하지
않습니다.

## 보안 원칙

- Pull Request 테스트에 LLM·AWS Secret을 제공하지 않습니다.
- `.env`를 Commit하지 않습니다.
- Workflow 기본 권한은 `contents: read`입니다.
- 자동 AWS 배포는 수동 EC2 배포를 이해한 뒤 04에서 별도로 구성합니다.

## 완료 체크

```text
[ ] CI와 배포의 차이를 설명할 수 있다.
[ ] Workflow Trigger와 기본 권한을 찾았다.
[ ] 로컬 Test·Compose 검사·Build를 통과했다.
[ ] Actions에서 첫 실패 Step과 오류 문장을 찾을 수 있다.
[ ] CI가 실제 Provider Secret 없이 동작하는 이유를 설명할 수 있다.
```
