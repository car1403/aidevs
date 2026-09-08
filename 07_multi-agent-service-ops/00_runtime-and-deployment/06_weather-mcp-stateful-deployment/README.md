# 05 Weather MCP Deployment Project

실제 날씨를 조회하는 MCP Tool 하나를 가진 가장 작은 Agent 배포 프로젝트입니다. Redis,
PostgreSQL, Ollama는 사용하지 않습니다. 목표는 Agent 기능을 늘리는 것이 아니라 Docker
Compose, CI, EC2 자동 배포의 전체 흐름을 확인하는 것입니다.

```text
Browser → Frontend :8501 → Backend Agent :8000
                              → Weather MCP :8010 (내부 전용)
                              → Open-Meteo 실제 날씨 API
                              → OpenAI 또는 Gemini
```

## 시나리오

사용자가 “서울 내일 날씨와 옷차림을 알려 줘”라고 입력합니다. Backend Agent는 MCP의
`get_weather` Tool로 실제 날씨 근거를 가져온 뒤 Cloud LLM이 답변을 만듭니다. Tool 결과 없이
온도·강수 정보를 만들어 내지 않습니다.

## 범위

| 포함 | 제외 |
| --- | --- |
| OpenAI 또는 Gemini, Open-Meteo, MCP | Ollama, Redis, PostgreSQL |
| Frontend·Backend·MCP Docker Compose | 대화 이력, Queue, Multi-Agent |
| Health Check, CI, EC2 배포 | 실제 예약·결제 |

MCP `8010`과 Backend `8000`은 Host·Security Group에 공개하지 않고, Browser는 Frontend
`8501`로만 접근합니다. CI는 실제 LLM·날씨 API를 호출하지 않고 Fake MCP·Fake LLM으로
계약을 검사합니다.

## 구현 순서

1. Backend·MCP·Frontend 구현
2. 로컬 Compose와 Health Check
3. CI: Test·Compose 검사·Image Build
4. EC2 수동 배포
5. production 승인형 GitHub Actions 배포

## 프로젝트 구조

```text
backend/app.py              Weather Agent API, MCP Client, Cloud LLM
backend/Dockerfile
frontend/app.py             왼쪽 메뉴가 있는 Streamlit 화면
frontend/Dockerfile
mcp_server/server.py        Open-Meteo get_weather MCP Tool
mcp_server/Dockerfile
compose.yml                 세 Container 연결과 Health Check
.env.example                OpenAI·Gemini 설정
```

## 실행 준비

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\05_weather-mcp-deployment-project
Copy-Item .env.example .env
```

`.env`에 사용할 Provider의 API Key를 입력합니다. OpenAI와 Gemini를 모두 사용할 경우 두
Key를 모두 설정합니다. `.env`를 Git에 Commit하지 않습니다.

```ini
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.5-flash
```

## Docker Compose 실행

```powershell
docker compose config --quiet
docker compose up -d --build
docker compose ps
```

접속 주소:

| 대상 | 주소 | 공개 여부 |
| --- | --- | --- |
| Frontend | `http://127.0.0.1:8501` | Browser에 공개 |
| Backend 문서 | `http://127.0.0.1:8000/docs` | 로컬 확인용 |
| Backend Readiness | `http://127.0.0.1:8000/health/ready` | 로컬 확인용 |
| Weather MCP | `http://weather-mcp:8010/mcp` | Docker 내부 전용 |

코드나 `.env`를 수정한 뒤에는 Container를 다시 만듭니다.

```powershell
docker compose up -d --build --force-recreate backend frontend weather-mcp
```

## 로그와 종료

```powershell
docker compose logs --tail=100 weather-mcp backend frontend
docker compose down
```

이 프로젝트에는 Volume이 없으므로 대화나 날씨 결과를 영구 저장하지 않습니다.

## CI/CD와 AWS 자동 배포

저장소 루트의 `.github/workflows/07-weather-mcp-cicd.yml`이 이 프로젝트 전용 Workflow입니다.

| 이벤트 | CI | AWS 배포 |
| --- | --- | --- |
| 개인 브랜치 Push | 실행 | 실행하지 않음 |
| Pull Request | 실행 | 실행하지 않음 |
| `main` Push | 실행 | CI 성공 후 `production` 승인 시 실행 |
| 수동 실행 | CI 실행 | Branch·이벤트 조건에 따라 실행하지 않음 |

CI에서는 실제 API Key나 외부 날씨 API를 사용하지 않습니다. `backend/test_app.py`가 Fake MCP와
Fake LLM을 사용해 API 계약을 검사한 뒤 Compose 설정과 세 Docker Image Build를 확인합니다.

EC2와 GitHub Environment 준비는 [AWS 자동 배포 준비](./deploy/README.md)를 순서대로
진행합니다.

## 완료 체크

```text
[ ] Frontend에서 실제 Open-Meteo Tool Result를 확인했다.
[ ] Weather MCP 8010이 Host에 공개되지 않음을 확인했다.
[ ] Backend Readiness가 MCP Tool 목록을 확인하는 이유를 설명할 수 있다.
[ ] 개인 브랜치와 Pull Request에서는 배포되지 않음을 확인했다.
[ ] main CI 성공 후 production 승인을 거쳐 EC2에 배포했다.
```
