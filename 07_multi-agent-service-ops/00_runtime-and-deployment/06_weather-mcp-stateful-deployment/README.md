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

## 1단계: 실행 준비

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

## 2단계: Infrastructure 최초 실행

```powershell
docker compose -f .\compose.infrastructure.yml config --quiet
docker compose -f .\compose.infrastructure.yml up -d
docker compose -f .\compose.infrastructure.yml ps
```

PostgreSQL과 Redis는 `weather-stateful` Network에 연결되고 각 Volume에 데이터를 유지합니다.

두 서비스가 `healthy`가 될 때까지 기다립니다. 최초 실행 시 새 PostgreSQL Volume에만
`database/init.sql`이 자동 적용되어 `weather_agent.runs` Table이 생성됩니다. 기존 Volume에는
Container를 재시작해도 초기화 SQL이 다시 실행되지 않습니다.

## 3단계: Application 실행

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

## 4단계: 상태 기반 기능 실습

### 화면 실습 순서

1. `http://127.0.0.1:8501`을 열고 도시 `서울`, 날짜 `내일`을 선택합니다.
2. 실행 버튼을 누르고 Progress Bar와 현재 단계가 변하는지 확인합니다.
3. 최종 답변과 MCP Tool Result의 온도·강수 정보를 비교합니다.
4. 실행 이력 화면에서 PostgreSQL에 저장된 완료 기록을 확인합니다.
5. 같은 도시·날짜를 다시 실행하여 Redis Cache 사용 표시를 확인합니다.

Frontend가 Agent 단계를 실행하는 것은 아닙니다. Backend에 실행을 요청한 뒤 실행 ID를 받아
상태 API를 주기적으로 조회합니다. 첫 요청은 MCP와 Open-Meteo를 호출하고, 같은 Cache Key의
두 번째 요청은 TTL이 남아 있으면 Redis 결과를 사용합니다. LLM 답변과 실행 이력은 두 요청
모두 새로 생성됩니다.

### 상태를 직접 확인하기

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

### Schema가 없을 때

기존 Volume이 `init.sql` 추가 전에 만들어졌다면 다음 명령으로 SQL을 적용합니다.

```powershell
Get-Content .\database\init.sql | docker compose -f .\compose.infrastructure.yml exec -T database psql -U agent_user -d agent_db
docker compose -f .\compose.application.yml up -d --build --force-recreate backend frontend
```

운영에서는 초기화 SQL을 반복 실행하기보다 버전이 기록되는 Migration 도구를 사용합니다.

### 로컬 실행에서 자주 발생하는 오류

| 증상 | 확인 | 해결 방향 |
| --- | --- | --- |
| `weather-stateful` Network 없음 | `docker network ls` | Infrastructure를 먼저 실행 |
| Backend가 healthy가 되지 않음 | Application의 Backend 로그 | MCP·DB·Redis Readiness 확인 |
| Database Schema가 false | PostgreSQL 직접 조회 | 위 초기화 SQL 적용 |
| 진행률이 멈춤 | Backend·Frontend 로그 | 실행 실패 또는 Polling API 확인 |
| 매번 Cache miss | Redis Key·TTL | 도시·날짜 변경 또는 TTL 만료 확인 |
| LLM 설정 오류 | Backend 로그 | 선택 Provider API Key 확인 |
| 코드 변경 미반영 | Image 생성 시간 | `--build --force-recreate` 실행 |

### 로그와 안전한 종료

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

## 5단계: 로컬에서 CI 명령 실행

CI는 **Continuous Integration(지속적 통합)**입니다. 코드가 Push되거나 Pull Request가
변경될 때 Test, Compose 검사, Docker Image Build를 자동 실행합니다. CD는 CI를 통과한
Application을 EC2에 반영하는 단계입니다.

GitHub에 Push하기 전에 로컬 PowerShell에서 CI와 같은 검사를 실행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\06_weather-mcp-stateful-deployment
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\backend\requirements.txt
python -m pip install pytest
python -m pytest .\backend\test_app.py -q
docker compose -f .\compose.infrastructure.yml config --quiet
docker compose -f .\compose.application.yml config --quiet
docker compose -f .\compose.application.yml build
```

Python 가상환경은 Test 패키지를 프로젝트별로 분리합니다. Docker Compose는 Python
가상환경의 기능이 아니라 Docker Engine을 사용하는 명령이므로 같은 PowerShell에서 그대로
실행하면 됩니다.

### CI가 확인하는 범위

```text
Source Checkout
→ Python 3.12 준비
→ Backend 패키지와 pytest 설치
→ Fake MCP·Fake LLM·Fake Store Test
→ Infrastructure Compose 문법 검사
→ Application Compose 문법 검사
→ Weather MCP·Backend·Frontend Image Build
```

| 검사 | 확인하는 것 | 확인하지 않는 것 |
| --- | --- | --- |
| Backend Test | API 계약·진행 상태·이력 처리 | 실제 Cloud LLM 요청 |
| Fake MCP | Tool 결과 처리 계약 | 실제 Open-Meteo 요청 |
| Fake Store | Redis·PostgreSQL 인터페이스 | 실제 DB 연결·Volume |
| Compose config | 두 YAML의 문법·변수 참조 | 장시간 Container 운영 |
| Application Build | 세 Application Image 생성 | PostgreSQL·Redis Image 재Build |

GitHub Runner에는 수강생 PC의 `.env`, Database, Redis, Docker Volume이 없습니다. 따라서 CI는
실제 외부 저장소 대신 Fake Store로 코드 계약을 검사합니다. CI 성공은 실제 통합 환경까지
성공했다는 의미가 아니므로 로컬과 EC2에서 별도 확인해야 합니다.

## 6단계: GitHub Actions Workflow 준비

Workflow는 Git 저장소 루트의 다음 위치에 있어야 GitHub가 인식합니다.

```text
.github/workflows/07-weather-stateful-cicd.yml
```

다음 Trigger는 06 프로젝트 또는 Workflow 파일이 변경될 때만 실행되도록 제한합니다.

```yaml
on:
  push:
    paths:
      - "07_multi-agent-service-ops/00_runtime-and-deployment/06_weather-mcp-stateful-deployment/**"
      - ".github/workflows/07-weather-stateful-cicd.yml"
  pull_request:
    paths:
      - "07_multi-agent-service-ops/00_runtime-and-deployment/06_weather-mcp-stateful-deployment/**"
      - ".github/workflows/07-weather-stateful-cicd.yml"
  workflow_dispatch:
```

| 이벤트 | Test·Build CI | AWS Application 배포 |
| --- | --- | --- |
| 개인 Branch Push | 실행 | 실행하지 않음 |
| Pull Request 생성·갱신 | 실행 | 실행하지 않음 |
| `main` Push·병합 | 실행 | CI 성공 후 실행 가능 |
| Actions의 `Run workflow` | 실행 | 현재 조건에서는 실행하지 않음 |
| 로컬 `git pull` | 실행하지 않음 | 실행하지 않음 |

Deploy Job의 핵심 조건은 다음과 같습니다.

```yaml
deploy-application:
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  needs: test-and-build
  environment: production
```

- `if`: `main` Branch의 Push에서만 배포합니다.
- `needs`: Test·Build가 실패하면 배포하지 않습니다.
- `environment`: `production` 승인 규칙과 Secret을 사용합니다.
- Job 이름처럼 Infrastructure가 아니라 Application만 배포합니다.

### 개인 Branch에서 CI 실행

저장소 루트에서 실행합니다.

```powershell
git switch -c weather-stateful-lab
git add 07_multi-agent-service-ops/00_runtime-and-deployment/06_weather-mcp-stateful-deployment
git add .github/workflows/07-weather-stateful-cicd.yml
git commit -m "Add stateful weather deployment lab"
git push -u origin weather-stateful-lab
```

GitHub 저장소의 `Actions` 탭에서 **07 Stateful Weather CI CD**를 선택합니다. Branch와 Commit을
확인하고 `test-and-build` Job을 엽니다. 실패한 경우 처음 빨간색이 된 Step의 첫 오류부터
확인합니다.

| 실패 Step | 먼저 확인할 내용 |
| --- | --- |
| Install and test | Python 버전, requirements, 최초 실패 Test |
| Validate Compose | YAML 들여쓰기, 환경 변수, 외부 Network 선언 |
| Build application images | Dockerfile의 Base Image·COPY 경로 |

## 7단계: AWS EC2 최초 준비

### 7-1. EC2와 Security Group

1. AWS Console에서 수업용 Region을 선택합니다.
2. Amazon Linux 2023 x86_64 EC2를 생성합니다.
3. 이름을 `weather-stateful`로 지정합니다.
4. 수업에서 정한 Instance Type과 Storage를 선택합니다.
5. Key Pair를 안전한 로컬 폴더에 저장합니다.
6. Public IPv4와 Public DNS를 기록합니다.

| Port | Source | 목적 |
| ---: | --- | --- |
| `22` | 승인된 관리자·배포 경로 | SSH |
| `8501` | 수강생 또는 운영자 IP | Streamlit Frontend |

Backend `8000`, MCP `8010`, PostgreSQL `5432`, Redis `6379`는 인터넷에 공개하지 않습니다.
Private Key를 Git, 메신저, README 또는 EC2에 업로드하지 않습니다.

현재 Workflow는 GitHub-hosted Runner가 EC2에 직접 SSH할 수 있다는 전제입니다. Security
Group이 내 PC IP만 허용하면 Runner는 접속할 수 없습니다. 실무에서는 self-hosted Runner,
VPN/Bastion, AWS Systems Manager 또는 조직에서 승인한 Runner 접근 정책을 사용합니다. 이를
해결하려고 SSH `22`를 계속 `0.0.0.0/0`으로 열어 두지 않습니다.

### 7-2. Docker와 Compose 설치

로컬 PowerShell에서 실제 Key와 DNS로 변경해 접속합니다.

```powershell
ssh -i "C:\Users\<사용자>\.ssh\weather-stateful.pem" ec2-user@<PUBLIC_DNS>
```

EC2에서 실행합니다.

```bash
sudo yum update -y
sudo yum install -y docker git
sudo service docker start
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
exit
```

SSH로 다시 접속한 후 확인합니다.

```bash
docker info
docker compose version
```

Compose Plugin이 없다면 다음을 시도합니다.

```bash
sudo yum install -y docker-compose-plugin
docker compose version
```

패키지를 찾지 못하면 임의 Script 대신 Docker 공식 설치 절차와 강사가 지정한 버전을
사용합니다.

### 7-3. 최초 Source 전송

Infrastructure는 자동 CD 전에 수동으로 한 번 실행해야 하므로 최초에는 프로젝트 전체를
EC2에 전송합니다. 로컬 PowerShell에서 실행합니다.

```powershell
scp -i "C:\Users\<사용자>\.ssh\weather-stateful.pem" -r `
  "C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\06_weather-mcp-stateful-deployment" `
  ec2-user@<PUBLIC_DNS>:~/weather-stateful
```

EC2에서 파일을 확인합니다.

```bash
cd ~/weather-stateful
ls
```

`backend`, `frontend`, `mcp_server`, `database`, 두 Compose 파일이 보여야 합니다.

### 7-4. EC2 환경 파일

EC2에서 최초 한 번 생성합니다.

```bash
cd ~/weather-stateful
cp .env.example .env
nano .env
chmod 600 .env
```

```ini
OPENAI_API_KEY=<실제 OpenAI API Key>
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=<실제 Gemini API Key>
GEMINI_MODEL=gemini-3.5-flash
POSTGRES_USER=agent_user
POSTGRES_PASSWORD=agent_pwd
POSTGRES_DB=agent_db
WEATHER_CACHE_TTL_SECONDS=600
```

Application 내부 연결은 Compose가 다음 값으로 구성합니다.

```ini
DATABASE_URL=postgresql://agent_user:agent_pwd@database:5432/agent_db
REDIS_URL=redis://redis:6379/0
WEATHER_MCP_URL=http://weather-mcp:8010/mcp
```

Workflow는 EC2의 `.env`를 복사하거나 덮어쓰지 않습니다. `.env`와 API Key를 Actions 로그에
출력하지 않습니다.

## 8단계: AWS Infrastructure 최초 실행

EC2에서 Application보다 먼저 실행합니다.

```bash
cd ~/weather-stateful
docker compose -f compose.infrastructure.yml config --quiet
docker compose -f compose.infrastructure.yml up -d
docker compose -f compose.infrastructure.yml ps
```

PostgreSQL과 Redis가 `healthy`인지 확인합니다.

```bash
docker compose -f compose.infrastructure.yml logs --tail=100 database redis
docker compose -f compose.infrastructure.yml exec database pg_isready -U agent_user -d agent_db
docker compose -f compose.infrastructure.yml exec redis redis-cli PING
```

Schema도 확인합니다.

```bash
docker compose -f compose.infrastructure.yml exec database psql -U agent_user -d agent_db -c "SELECT to_regclass('weather_agent.runs');"
```

이 단계에서 `weather-stateful` Network와 PostgreSQL·Redis Volume이 만들어집니다. 이후 자동
배포에서 Infrastructure Compose에 `down`, `up --force-recreate`, `down -v`를 실행하지
않습니다.

### Application 최초 수동 검증

자동 배포를 연결하기 전에 EC2에서 한 번 직접 실행합니다.

```bash
docker compose -f compose.application.yml config --quiet
docker compose -f compose.application.yml up -d --build
docker compose -f compose.application.yml ps
curl --fail --retry 12 --retry-delay 5 http://127.0.0.1:8000/health/ready
```

Browser에서 `http://<EC2_PUBLIC_IP>:8501`을 열어 실제 날씨 조회, Progress Bar, Cache, 실행
이력을 확인합니다. 최초 수동 실행이 실패하는 상태에서 CD부터 연결하지 않습니다.

## 9단계: GitHub Production Environment

GitHub 저장소에서 다음 순서로 설정합니다.

1. `Settings → Environments`로 이동합니다.
2. `New environment`에서 `production`을 생성합니다.
3. 가능한 계정에서는 `Required reviewers`를 설정합니다.
4. Deployment Branch를 `main`으로 제한합니다.
5. 다음 Environment Secret 네 개를 등록합니다.

| Secret | 값 |
| --- | --- |
| `AWS_HOST` | EC2 Public DNS 또는 Public IPv4 |
| `AWS_USER` | Amazon Linux의 `ec2-user` |
| `AWS_SSH_PRIVATE_KEY` | 배포용 Private Key 전체 내용 |
| `AWS_SSH_KNOWN_HOSTS` | Fingerprint를 검증한 EC2 known_hosts 한 줄 |

Private Key는 시작·끝 줄과 줄바꿈을 포함하여 저장하고 따옴표를 추가하지 않습니다.
known_hosts 값은 EC2 Host Key Fingerprint를 관리자가 확인한 뒤 로컬 결과와 대조합니다.

```powershell
ssh-keyscan -H <PUBLIC_DNS>
```

검증 없이 Host Key 검사를 끄거나 `StrictHostKeyChecking=no`를 사용하지 않습니다.

## 10단계: main 병합과 Application 자동 배포

```text
개인 Branch Push
→ Fake Store 기반 CI
→ Pull Request·CI
→ main 병합
→ main CI 재실행
→ production 승인
→ EC2로 Source 복사
→ Application Compose만 Build·재생성
→ Backend Readiness 검증
```

Deploy Job이 EC2에서 수행하는 핵심 명령은 다음과 같습니다.

```bash
cd ~/weather-stateful
test -f .env
docker compose -f compose.application.yml config --quiet
docker compose -f compose.application.yml up -d --build --force-recreate weather-mcp backend frontend
curl --fail --retry 12 --retry-delay 5 http://127.0.0.1:8000/health/ready
```

`compose.infrastructure.yml`을 실행하지 않는 것이 중요합니다. Application Container는 교체되지만
PostgreSQL·Redis Container, Network, Volume은 유지됩니다.

## 11단계: 배포 후 데이터 보존 검증

EC2에서 두 Compose 상태를 따로 확인합니다.

```bash
cd ~/weather-stateful
docker compose -f compose.infrastructure.yml ps
docker compose -f compose.application.yml ps
docker compose -f compose.application.yml logs --tail=100 weather-mcp backend frontend
curl --fail http://127.0.0.1:8000/health/ready
```

PostgreSQL의 기존 실행 이력을 조회합니다.

```bash
docker compose -f compose.infrastructure.yml exec database psql -U agent_user -d agent_db -c "SELECT run_id, city, provider, created_at FROM weather_agent.runs ORDER BY created_at DESC LIMIT 10;"
```

배포 전 실행 이력이 남아 있고, 배포 후 새 요청도 추가되면 상태 보존 배포가 성공한 것입니다.
Redis Key도 확인할 수 있습니다.

```bash
docker compose -f compose.infrastructure.yml exec redis redis-cli --scan --pattern "weather:*"
```

## 12단계: 배포 실패 진단과 복구

| 증상 | 먼저 확인 | 해결 방향 |
| --- | --- | --- |
| CI가 시작되지 않음 | Workflow 위치·`paths` | 저장소 루트와 변경 경로 확인 |
| Fake Store Test 실패 | 최초 빨간 Test | 로컬 pytest로 재현 |
| SSH timeout | Security Group·배포 Network | 승인된 Runner 접근 경로 준비 |
| Host Key 오류 | known_hosts Secret | EC2 재생성 여부·Fingerprint 재검증 |
| `.env` 없음 | `~/weather-stateful/.env` | EC2에서 최초 환경 파일 생성 |
| External Network 없음 | `docker network ls` | Infrastructure Compose 최초 실행 |
| Database Schema 실패 | `to_regclass` 조회 | 기존 Volume에 init.sql 적용 |
| Backend Readiness 실패 | Backend·MCP·DB·Redis 로그 | 실패한 의존 서비스부터 복구 |
| 배포 후 이력 사라짐 | Volume·Compose 명령 | Infrastructure 재생성·`down -v` 여부 확인 |

입문 예제에는 Blue/Green과 자동 Rollback이 없습니다. 마지막 정상 Commit으로 되돌리는 새
Commit을 만들고 CI와 승인을 다시 거쳐 배포합니다. EC2에서 Application 코드를 직접 수정하면
다음 배포에서 덮어써지고 변경 이력도 남지 않습니다.

AWS 비용을 중단하려면 수업 정책에 따라 EC2를 중지합니다. Instance를 삭제할 때는 PostgreSQL
Volume 역할을 하는 Docker Volume이 EC2 Disk 안에 있다는 점을 기억해야 합니다. 필요한 실행
이력을 먼저 Export·Backup하지 않으면 Instance/EBS 삭제 후 복구할 수 없습니다.

## 완료 체크

```text
[ ] Frontend에서 실제 Open-Meteo Tool Result를 확인했다.
[ ] 같은 도시·날짜를 다시 조회해 Redis Cache 사용 표시를 확인했다.
[ ] Application을 다시 배포해도 PostgreSQL 실행 이력이 남는 것을 확인했다.
[ ] Backend Readiness에서 MCP·PostgreSQL·Schema·Redis 상태를 구분했다.
[ ] 로컬 pytest, 두 Compose 검사, Application Image Build를 통과했다.
[ ] Fake MCP·LLM·Store를 CI에서 사용하는 이유를 설명할 수 있다.
[ ] 개인 Branch와 Pull Request에서 CI 결과를 확인했다.
[ ] EC2에서 Infrastructure를 먼저 한 번 실행하고 Schema를 확인했다.
[ ] EC2에서 Application 최초 수동 실행과 실제 통합을 확인했다.
[ ] GitHub production Environment와 네 개의 Secret을 설정했다.
[ ] 개인 브랜치와 Pull Request에서는 배포되지 않음을 확인했다.
[ ] main 배포가 PostgreSQL·Redis Container를 재생성하지 않음을 확인했다.
[ ] Application 재배포 전후의 PostgreSQL 이력을 비교했다.
[ ] EC2/EBS 삭제 전에 상태 데이터 Backup이 필요한 이유를 설명할 수 있다.
```
