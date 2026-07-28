# 02 Simple GitHub Actions

01의 Simple Compose를 변경했을 때 Backend 테스트와 Docker Build가 자동으로
통과하는지 확인합니다. AWS 배포와 Secret은 아직 사용하지 않습니다.

실제 Workflow:

[07-simple-compose-ci.yml](../../../.github/workflows/07-simple-compose-ci.yml)

> 위 링크는 과정 폴더만 별도 복사한 경우에는 동작하지 않을 수 있습니다.
> GitHub는 저장소 루트의 `.github/workflows`에 있는 Workflow를 인식합니다.

## 1. 이번 단계의 목표

```text
Git Push 또는 Pull Request
→ 소스 내려받기
→ Python 3.12 준비
→ Backend 테스트
→ Compose 문법 검사
→ Frontend·Backend Image Build
```

다음은 하지 않습니다.

- AWS 자동 배포
- Container Registry Push
- SSH
- GitHub Secret
- LLM API 호출
- Redis·PostgreSQL 실행
- Production 배포

## 2. Workflow 위치

```text
C:\aidevs
├─ .github
│  └─ workflows
│     └─ 07-simple-compose-ci.yml
└─ 07_multi-agent-service-ops
   └─ 13_observability-docker-and-security
      └─ 01_simple-compose
```

Workflow를 `02_simple-github-actions` 안에만 두면 GitHub Actions가 실행하지
않습니다. 이 폴더에는 설명 문서를 두고 실제 실행 파일은 저장소 루트의
`.github/workflows`에 둡니다.

## 3. 실행 조건

다음 파일이 변경된 Push 또는 Pull Request에서 실행됩니다.

```text
01_simple-compose/**
.github/workflows/07-simple-compose-ci.yml
```

GitHub Actions 화면에서 직접 실행할 수 있도록 `workflow_dispatch`도
포함합니다.

## 4. 단계별 설명

### Checkout

Runner가 저장소 코드를 내려받습니다. Checkout 전에는 과정 파일에 접근할 수
없습니다.

### Python 준비

`actions/setup-python`으로 Python 3.12를 명시합니다. Runner의 기본 Python에
의존하지 않습니다.

### 테스트 의존성 설치

```text
FastAPI
Uvicorn
pytest
httpx
```

교육용 테스트는 외부 API·Redis·DB를 사용하지 않습니다.

### Backend 테스트

```powershell
python -m pytest backend/test_app.py -q
```

확인 항목:

- `/health` 상태
- `/api/message` 입력·응답
- 사용자 이름이 응답에 포함되는지

### Compose 검사

```powershell
docker compose config --quiet
```

Container를 실행하지 않고 Compose 파일의 기본 구조를 검사합니다.

### Image Build

```powershell
docker compose build
```

Backend와 Frontend Dockerfile이 실제로 Image를 만들 수 있는지 확인합니다.
Registry에 Push하지 않습니다.

## 5. 로컬 사전 확인

Push 전에 Simple Compose 폴더에서 실행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\13_observability-docker-and-security\01_simple-compose
python -m pip install -r .\backend\requirements.txt
python -m pip install pytest httpx
python -m pytest .\backend\test_app.py -q
docker compose config
docker compose build
```

## 6. GitHub에서 확인

1. 저장소 페이지를 엽니다.
2. `Actions` 탭을 선택합니다.
3. `07 Simple Compose CI`를 선택합니다.
4. 최신 실행을 선택합니다.
5. `test-and-build` Job을 엽니다.
6. 각 Step의 성공·실패 로그를 확인합니다.

## 7. 실패 실습

### 테스트 실패

Backend 응답의 `service`를 임시로 다른 값으로 바꿉니다.

```text
기대: backend
실제: wrong-backend
```

`Test backend` Step에서 실패해야 합니다. 확인 후 원래 값으로 복구합니다.

### Compose 실패

Compose의 `build: ./backend`를 존재하지 않는 폴더로 바꿉니다.

`Validate Compose` 또는 `Build images`에서 실패해야 합니다. 실습 후 반드시
복구합니다.

### Frontend Build 실패

Frontend requirements의 패키지 이름을 잘못 입력합니다. Build 로그에서 어느
Image와 명령이 실패했는지 찾고 원래 값으로 복구합니다.

## 8. 자주 하는 실수

| 증상 | 확인 |
| --- | --- |
| Workflow가 보이지 않음 | 파일이 저장소 루트 `.github/workflows`에 있는가? |
| 경로를 찾지 못함 | `working-directory`가 저장소 기준인가? |
| 테스트 Import 오류 | Backend requirements와 pytest·httpx 설치 여부 |
| Compose 명령 실패 | Runner가 Linux인지, Compose 파일 위치가 맞는지 |
| 변경해도 실행 안 됨 | `paths` 조건에 변경 파일이 포함되는가? |

## 9. 보안 원칙

- 이 Workflow에는 AWS Key를 넣지 않습니다.
- LLM API Key를 넣지 않습니다.
- `.env`를 Commit하지 않습니다.
- Pull Request의 코드가 Secret을 읽도록 구성하지 않습니다.
- Workflow 권한은 `contents: read`로 제한합니다.

## 10. 완료 체크

```text
[ ] Workflow 파일이 저장소 루트에 있다.
[ ] Push 또는 수동 실행으로 Workflow가 시작된다.
[ ] Backend 테스트가 통과한다.
[ ] Compose 검사가 통과한다.
[ ] 두 Docker Image Build가 통과한다.
[ ] 의도적인 테스트 실패 원인을 로그에서 찾는다.
[ ] AWS 배포와 CI가 아직 분리되어 있음을 설명한다.
```

## 공식 문서

- [GitHub Actions에서 Python 빌드와 테스트](https://docs.github.com/en/actions/tutorials/build-and-test-code/python)
- [Workflow 문법과 working-directory](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)

