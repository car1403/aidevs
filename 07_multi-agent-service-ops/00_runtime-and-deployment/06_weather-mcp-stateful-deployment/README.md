# 06 Stateful Weather MCP Deployment

05 Weather MCP Agent에 PostgreSQL 영구 이력과 Redis 진행 상태·날씨 Cache를 추가한
완성형 상태 기반 배포 프로젝트입니다. 인프라는 한 번 준비하고 Application만 반복 배포합니다.

## 학습 목표와 05와의 차이

| 구분 | 05 Stateless | 06 Stateful |
| --- | --- | --- |
| 실행 진행 상태 | 저장하지 않음 | Redis에 저장하고 Frontend가 Polling |
| 같은 날씨 재조회 | 매번 MCP 호출 | Redis Cache 사용(기본 600초) |
| 완료 이력 | 저장하지 않음 | PostgreSQL에 영구 저장 |
| Compose | 하나 | Infrastructure와 Application 분리 |
| 재배포 | 전체 실행 가능 | Application만 교체하고 데이터 유지 |

이 과정의 핵심은 Redis와 PostgreSQL의 역할을 구분하는 것입니다. Redis에는 자주 읽지만 오래
보관할 필요가 없는 진행 상태와 Cache를 저장하고, PostgreSQL에는 운영 이력으로 남겨야 하는
완료 결과를 저장합니다.

```text
Browser → Frontend → Backend Agent → Weather MCP → Open-Meteo
                         ├→ Redis: 진행 상태·날씨 Cache
                         ├→ PostgreSQL: 완료 실행 이력
                         └→ OpenAI 또는 Gemini
```

## 시나리오

사용자가 “서울 내일 날씨와 옷차림을 알려 줘”라고 입력합니다. Backend Agent는 MCP의
`get_weather` Tool로 실제 날씨 근거를 가져온 뒤 Cloud LLM이 답변을 만듭니다. Tool 결과 없이
온도·강수 정보를 만들어 내지 않습니다.

## 범위

| 포함 | 제외 |
| --- | --- |
| OpenAI 또는 Gemini, Open-Meteo, MCP | Ollama |
| PostgreSQL 실행 이력·Redis 상태와 Cache | Worker Queue, Multi-Agent |
| Health Check, CI, EC2 배포 | 실제 예약·결제 |

PostgreSQL·Redis·MCP는 외부에 공개하지 않습니다. CI는 실제 저장소 대신 Fake Store를
사용하며, CD는 인프라 Container를 재시작하지 않고 Application만 교체합니다.

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
database/init.sql           실행 이력 Schema와 Table
compose.infrastructure.yml PostgreSQL·Redis·Volume·공용 Network
compose.application.yml    Frontend·Backend·MCP와 외부 Network 연결
.env.example                OpenAI·Gemini 설정
```

## 실행 준비

### 사전 확인

Docker Desktop을 실행하고 다음 명령이 정상인지 확인합니다.

```powershell
docker version
docker compose version
Get-NetTCPConnection -LocalPort 8000,8501 -ErrorAction SilentlyContinue
```

출력이 있는 Port는 `docker ps`로 어떤 Container가 사용하는지 확인합니다. Database와 Redis는
Host Port를 공개하지 않으므로 기존 Host의 `5432`, `6379`와 충돌하지 않습니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\06_weather-mcp-stateful-deployment
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

다음 내부 주소의 `database`, `redis`, `weather-mcp`는 Compose 서비스 이름입니다. Container
안에서 `127.0.0.1`로 바꾸면 자기 자신을 가리키므로 연결되지 않습니다.

```ini
DATABASE_URL=postgresql://agent_user:agent_pwd@database:5432/agent_db
REDIS_URL=redis://redis:6379/0
WEATHER_MCP_URL=http://weather-mcp:8010/mcp
WEATHER_CACHE_TTL_SECONDS=600
```

`.env`가 Git에 포함되지 않는지도 `git check-ignore .env`로 확인합니다.

## 1. 인프라 최초 실행

```powershell
docker compose -f .\compose.infrastructure.yml config --quiet
docker compose -f .\compose.infrastructure.yml up -d
docker compose -f .\compose.infrastructure.yml ps
```

PostgreSQL과 Redis는 `weather-stateful` Network에 연결되고 각 Volume에 데이터를 유지합니다.

두 서비스가 `healthy`가 될 때까지 기다립니다. 최초 실행 시 새 PostgreSQL Volume에만
`database/init.sql`이 자동 적용되어 `weather_agent.runs` Table이 생성됩니다. 기존 Volume에는
Container를 재시작해도 초기화 SQL이 다시 실행되지 않습니다.

## 2. Application 실행

```powershell
docker compose -f .\compose.application.yml config --quiet
docker compose -f .\compose.application.yml up -d --build
docker compose -f .\compose.application.yml ps
```

Application Compose는 이미 생성된 외부 Network `weather-stateful`을 사용합니다. Network를
찾을 수 없다는 오류가 나면 Infrastructure를 먼저 실행하지 않은 것입니다.

접속 주소:

| 대상 | 주소 | 공개 여부 |
| --- | --- | --- |
| Frontend | `http://127.0.0.1:8501` | Browser에 공개 |
| Backend 문서 | `http://127.0.0.1:8000/docs` | 로컬 확인용 |
| Backend Readiness | `http://127.0.0.1:8000/health/ready` | 로컬 확인용 |
| Weather MCP | `http://weather-mcp:8010/mcp` | Docker 내부 전용 |
| PostgreSQL | `database:5432` | Docker 내부 전용 |
| Redis | `redis:6379` | Docker 내부 전용 |

코드나 `.env`를 수정한 뒤에는 Container를 다시 만듭니다.

```powershell
docker compose -f .\compose.application.yml up -d --build --force-recreate weather-mcp backend frontend
```

이 명령은 Database·Redis Container와 Volume을 재생성하지 않습니다.

## 화면 실습 순서

1. `http://127.0.0.1:8501`을 열고 도시 `서울`, 날짜 `내일`을 선택합니다.
2. 실행 버튼을 누르고 Progress Bar와 현재 단계가 변하는지 확인합니다.
3. 최종 답변과 MCP Tool Result의 온도·강수 정보를 비교합니다.
4. 실행 이력 화면에서 PostgreSQL에 저장된 완료 기록을 확인합니다.
5. 같은 도시·날짜를 다시 실행하여 Redis Cache 사용 표시를 확인합니다.

Frontend가 Agent 단계를 실행하는 것은 아닙니다. Backend에 실행을 요청한 뒤 실행 ID를 받아
상태 API를 주기적으로 조회합니다. 첫 요청은 MCP와 Open-Meteo를 호출하고, 같은 Cache Key의
두 번째 요청은 TTL이 남아 있으면 Redis 결과를 사용합니다. LLM 답변과 실행 이력은 두 요청
모두 새로 생성됩니다.

## 상태를 직접 확인하기

Backend Process 생존과 의존 서비스 준비 상태를 구분합니다.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health/live
Invoke-RestMethod http://127.0.0.1:8000/health/ready
```

Liveness가 성공해도 Readiness는 MCP·PostgreSQL·Schema·Redis 중 하나가 실패하면 실패할 수
있습니다. API 전체 목록은 `http://127.0.0.1:8000/docs`에서 확인합니다.

PostgreSQL 실행 이력을 직접 조회합니다.

```powershell
docker compose -f .\compose.infrastructure.yml exec database psql -U agent_user -d agent_db -c "SELECT run_id, city, day, provider, model, created_at FROM weather_agent.runs ORDER BY created_at DESC LIMIT 10;"
```

Redis가 가진 날씨 관련 Key도 확인할 수 있습니다.

```powershell
docker compose -f .\compose.infrastructure.yml exec redis redis-cli --scan --pattern "weather:*"
```

`FLUSHALL`은 다른 실습 데이터까지 삭제할 수 있으므로 사용하지 않습니다.

## Schema가 없을 때

기존 Volume이 `init.sql` 추가 전에 만들어졌다면 다음 명령으로 SQL을 적용합니다.

```powershell
Get-Content .\database\init.sql | docker compose -f .\compose.infrastructure.yml exec -T database psql -U agent_user -d agent_db
docker compose -f .\compose.application.yml up -d --build --force-recreate backend frontend
```

운영에서는 초기화 SQL을 반복 실행하기보다 버전이 기록되는 Migration 도구를 사용합니다.

## 자주 발생하는 오류

| 증상 | 확인 | 해결 방향 |
| --- | --- | --- |
| `weather-stateful` Network 없음 | `docker network ls` | Infrastructure를 먼저 실행 |
| Backend가 healthy가 되지 않음 | Application의 Backend 로그 | MCP·DB·Redis Readiness 확인 |
| Database Schema가 false | PostgreSQL 직접 조회 | 위 초기화 SQL 적용 |
| 진행률이 멈춤 | Backend·Frontend 로그 | 실행 실패 또는 Polling API 확인 |
| 매번 Cache miss | Redis Key·TTL | 도시·날짜 변경 또는 TTL 만료 확인 |
| LLM 설정 오류 | Backend 로그 | 선택 Provider API Key 확인 |
| 코드 변경 미반영 | Image 생성 시간 | `--build --force-recreate` 실행 |

## 로그와 종료

```powershell
docker compose -f .\compose.application.yml logs --tail=100 weather-mcp backend frontend
docker compose -f .\compose.application.yml down
```

이 명령은 PostgreSQL·Redis를 중지하거나 Volume을 삭제하지 않습니다. 전체 실습을 끝낼 때만
`docker compose -f .\compose.infrastructure.yml down`을 실행합니다. `down -v`는 저장 데이터를
삭제하므로 초기화 목적이 아니면 사용하지 않습니다.

Application의 `down`은 상태 인프라를 중지하지 않습니다. Infrastructure의 일반 `down`도
Volume은 유지합니다. `down -v`는 PostgreSQL 이력과 Redis 데이터를 삭제하며 복구할 수
없으므로 완전 초기화가 명확히 필요할 때만 사용합니다.

## CI/CD와 AWS 자동 배포

저장소 루트의 `.github/workflows/07-weather-stateful-cicd.yml`이 전용 Workflow입니다.

| 이벤트 | CI | AWS 배포 |
| --- | --- | --- |
| 개인 브랜치 Push | 실행 | 실행하지 않음 |
| Pull Request | 실행 | 실행하지 않음 |
| `main` Push | 실행 | CI 성공 후 `production` 승인 시 실행 |
| 수동 실행 | CI 실행 | Branch·이벤트 조건에 따라 실행하지 않음 |

CI는 Fake MCP·LLM·저장소로 계약을 검사하고 두 Compose를 검증합니다. CD는
`compose.application.yml`만 실행하므로 PostgreSQL·Redis와 기존 데이터가 유지됩니다.

AWS 최초 구성은 다음 순서입니다.

1. EC2에 저장소와 `.env`를 준비합니다.
2. Infrastructure Compose를 한 번 실행하고 Schema·Health를 확인합니다.
3. Application Compose를 수동 실행해 실제 API 연동을 검증합니다.
4. GitHub `production` Environment와 승인자를 설정합니다.
5. 이후 `main` 배포에서는 Application만 Build·교체합니다.

CI의 Fake Test 성공은 코드 계약과 Image Build가 정상이라는 뜻입니다. 실제 Open-Meteo,
Cloud LLM, Redis, PostgreSQL 통합은 로컬 또는 EC2에서 별도로 확인해야 합니다.

EC2와 GitHub Environment 준비는 [AWS 자동 배포 준비](./deploy/README.md)를 순서대로
진행합니다.

## 완료 체크

```text
[ ] Frontend에서 실제 Open-Meteo Tool Result를 확인했다.
[ ] 같은 도시·날짜를 다시 조회해 Redis Cache 사용 표시를 확인했다.
[ ] Application을 다시 배포해도 PostgreSQL 실행 이력이 남는 것을 확인했다.
[ ] Backend Readiness에서 MCP·PostgreSQL·Schema·Redis 상태를 구분했다.
[ ] 개인 브랜치와 Pull Request에서는 배포되지 않음을 확인했다.
[ ] main 배포가 PostgreSQL·Redis Container를 재생성하지 않음을 확인했다.
```
