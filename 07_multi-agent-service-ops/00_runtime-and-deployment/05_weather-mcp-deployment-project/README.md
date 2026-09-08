# 05 Weather MCP Deployment Project

실제 날씨를 조회하는 MCP Tool 하나를 가진 가장 작은 Agent 배포 프로젝트입니다. Redis,
PostgreSQL, Ollama는 사용하지 않습니다. 목표는 Agent 기능을 늘리는 것이 아니라 Docker
Compose, CI, EC2 자동 배포의 전체 흐름을 확인하는 것입니다.

## 이 실습에서 배우는 것

이 프로젝트는 처음으로 세 개의 Application Process를 각각 Container로 분리합니다.

| Process | 책임 | 다른 Process와 통신하는 방법 |
| --- | --- | --- |
| Frontend | 사용자 입력과 결과 표시 | Backend HTTP API 호출 |
| Backend Agent | 실행 순서 제어, MCP 호출, LLM 호출 | MCP Streamable HTTP·Cloud LLM HTTPS |
| Weather MCP | 실제 날씨 Tool 제공 | Open-Meteo HTTPS 호출 |

중요한 핵심은 `localhost`의 의미입니다. Container 안의 `localhost`는 Host PC가 아니라
그 Container 자신입니다. 따라서 Frontend는 `http://backend:8000`, Backend는
`http://weather-mcp:8010/mcp`처럼 Compose 서비스 이름을 사용합니다.

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

## 1단계: 실행 준비

### 1. 사전 요구 사항

다음을 먼저 확인합니다.

```powershell
docker version
docker compose version
```

Docker Desktop이 실행 중이어야 합니다. 또한 다음 Host Port가 비어 있어야 합니다.

```powershell
Get-NetTCPConnection -LocalPort 8000,8501 -ErrorAction SilentlyContinue
```

출력이 있다면 기존 Backend·Frontend Container를 먼저 확인합니다. 무조건 삭제하지 말고
`docker ps`로 이 프로젝트의 Container인지 확인한 뒤 중지합니다.

### 2. 환경 파일 만들기

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

한 Provider만 실습할 경우 해당 Key만 입력해도 됩니다. 화면에서 Key가 없는 Provider를
선택하면 Backend는 오류를 반환합니다. 이를 가짜 성공 응답으로 바꾸지 않습니다.

환경 파일이 Git에 포함되지 않는지 확인합니다.

```powershell
git check-ignore .env
```

## 2단계: Docker Compose 실행

### 1. 설정 검사

```powershell
docker compose config --quiet
```

아무 출력 없이 끝나면 YAML 문법과 변수 치환이 정상입니다. 이 명령은 Container를 만들지
않습니다.

### 2. Image Build와 실행

```powershell
docker compose up -d --build
docker compose ps
```

기대 순서는 다음과 같습니다.

```text
weather-mcp 시작 → Health 통과
→ backend 시작 → MCP 목록 확인 → Health 통과
→ frontend 시작
```

`docker compose ps`에서 세 서비스가 `Up`이고 Health Check가 있는 서비스는 `healthy`여야
합니다. Frontend가 시작되지 않으면 먼저 Backend Health를 확인합니다.

접속 주소:

| 대상 | 주소 | 공개 여부 |
| --- | --- | --- |
| Frontend | `http://127.0.0.1:8501` | Browser에 공개 |
| Backend 문서 | `http://127.0.0.1:8000/docs` | 로컬 확인용 |
| Backend Readiness | `http://127.0.0.1:8000/health/ready` | 로컬 확인용 |
| Weather MCP | `http://weather-mcp:8010/mcp` | Docker 내부 전용 |

`expose: 8010`은 다른 Container가 MCP에 접근할 수 있게 하지만 Host Port로 공개하지
않습니다. 반면 Backend와 Frontend의 `ports`는 로컬 학습 확인을 위해 Host에 연결됩니다.

## 3단계: 기능과 상태 확인

### 화면 실습

1. Browser에서 `http://127.0.0.1:8501`을 엽니다.
2. 왼쪽 메뉴에서 `Weather Agent`를 선택합니다.
3. 도시 `서울`, 날짜 `내일`, Provider `openai` 또는 `gemini`를 선택합니다.
4. **실제 날씨 조회**를 누릅니다.
5. 최종 답변과 `get_weather` Tool Result를 비교합니다.
6. `구조 이해` 메뉴에서 호출 순서를 확인합니다.
7. `Health Check` 메뉴에서 Backend와 MCP 연결 상태를 확인합니다.

정상 결과에는 다음 정보가 포함됩니다.

```text
Cloud LLM 답변
사용 Provider와 실제 Model
MCP Tool 이름: get_weather
Open-Meteo의 날짜·최고/최저 기온·강수 확률
```

도시명을 찾지 못하거나 외부 API가 실패하면 성공처럼 표시하지 않습니다.

### API로 직접 확인

Frontend 문제와 Backend 문제를 분리하려면 PowerShell에서 API를 직접 호출합니다.

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health/live
Invoke-RestMethod http://127.0.0.1:8000/health/ready
```

```powershell
$body = @{
    city = "서울"
    day = "tomorrow"
    provider = "openai"
} | ConvertTo-Json

Invoke-RestMethod `
    -Method Post `
    -Uri http://127.0.0.1:8000/api/weather `
    -ContentType "application/json" `
    -Body $body
```

- `/health/live`: Backend Process 자체가 살아 있는지 확인합니다.
- `/health/ready`: Backend가 Weather MCP Tool을 사용할 준비가 되었는지 확인합니다.
- `/api/weather`: MCP와 LLM까지 포함한 실제 Agent 흐름을 실행합니다.

코드나 `.env`를 수정한 뒤에는 Container를 다시 만듭니다.

```powershell
docker compose up -d --build --force-recreate backend frontend weather-mcp
```

### 로그와 종료

```powershell
docker compose logs --tail=100 weather-mcp backend frontend
docker compose down
```

이 프로젝트에는 Volume이 없으므로 대화나 날씨 결과를 영구 저장하지 않습니다.

### 로컬 실행에서 자주 발생하는 오류

| 증상 | 먼저 확인할 명령 | 가능한 원인 |
| --- | --- | --- |
| Frontend가 시작되지 않음 | `docker compose ps` | Backend Health 실패로 의존성 대기 |
| `/health/ready`가 503 | `docker compose logs backend weather-mcp` | MCP 시작 실패·내부 URL 오류 |
| LLM 설정 오류 | `docker compose logs backend` | 선택 Provider API Key 누락 |
| 도시를 찾지 못함 | Tool Result 확인 | 도시명 오류·Open-Meteo 검색 결과 없음 |
| 8000 또는 8501 충돌 | `docker ps` | 기존 Container가 Port 사용 중 |
| 수정한 코드가 반영되지 않음 | Image 생성 시간 확인 | 재빌드하지 않고 기존 Container 사용 |

Container 하나의 로그를 계속 보려면 다음을 사용하고, 종료할 때 `Ctrl+C`를 누릅니다.

```powershell
docker compose logs -f backend
```

`Ctrl+C`는 로그 보기만 종료하며 Container는 계속 실행됩니다.

## 4단계: 로컬에서 CI 명령 미리 실행

CI는 **Continuous Integration(지속적 통합)**의 약자입니다. 개발자가 Push하거나 Pull
Request를 만들 때 Test, 설정 검사, Image Build를 자동 실행하여 변경 사항을 병합해도 되는지
확인합니다. CD는 검증된 코드를 실제 EC2에 반영하는 **Continuous Delivery/Deployment**
단계입니다.

GitHub에 올리기 전에 로컬 PowerShell에서 CI와 같은 명령을 실행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\05_weather-mcp-deployment-project
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r .\backend\requirements.txt
python -m pip install pytest
python -m pytest .\backend\test_app.py -q
docker compose config --quiet
docker compose build
```

`.venv`는 Python Test 패키지를 프로젝트별로 분리합니다. `docker compose`는 가상환경 안에
설치하는 명령이 아니라 Docker Desktop의 Docker Engine에 요청하는 명령이므로 같은
PowerShell에서 그대로 실행하면 됩니다.

### CI가 확인하는 것과 확인하지 않는 것

```text
소스 Checkout
→ Python 3.12 준비
→ Backend 의존성·pytest 설치
→ Fake Weather MCP·Fake LLM Backend Test
→ Compose YAML과 환경 변수 참조 검사
→ Frontend·Backend·Weather MCP Image Build
```

| 검사 | CI가 확인하는 것 | CI가 확인하지 않는 것 |
| --- | --- | --- |
| Backend Test | Health와 Weather Agent 응답 계약 | 실제 OpenAI·Gemini 호출 |
| Fake MCP | Tool Result가 응답에 포함되는지 | 실제 Open-Meteo 연결 |
| Compose config | YAML 문법·변수 치환 | Container의 실제 장시간 운영 |
| Docker Build | 세 Dockerfile로 Image 생성 가능 | Registry Push·EC2 실행 |

CI Runner는 GitHub가 실행할 때마다 새로 만드는 Linux 가상 머신입니다. 수강생 PC의 `.env`,
실행 중인 Container, API Key가 Runner로 자동 전달되지 않습니다. 그래서 CI Test는 외부 API를
Fake 함수로 교체합니다. CI 성공 후에도 실제 API 통합은 로컬 또는 EC2에서 별도로 확인해야
합니다.

## 5단계: GitHub Actions Workflow 준비

Workflow 파일은 저장소 루트의 다음 위치에 있어야 합니다.

```text
.github/workflows/07-weather-mcp-cicd.yml
```

`.github`는 `05_weather-mcp-deployment-project` 안이 아니라 Git 저장소 최상위 폴더에 둡니다.
GitHub는 기본적으로 이 위치의 `.yml` 또는 `.yaml`만 Workflow로 인식합니다.

이 프로젝트의 Workflow는 다음 이벤트를 사용합니다.

| 이벤트 | CI Job | AWS Deploy Job |
| --- | --- | --- |
| 개인 브랜치 Push | 실행 | 실행하지 않음 |
| Pull Request 생성·갱신 | 실행 | 실행하지 않음 |
| `main` Branch Push·병합 | 실행 | CI 성공 후 실행 가능 |
| Actions의 `Run workflow` | CI 실행 | 현재 조건에서는 실행하지 않음 |
| 로컬 `git pull` | 실행하지 않음 | 실행하지 않음 |

`paths` 조건 때문에 다음 프로젝트 또는 Workflow 파일이 변경되었을 때만 실행됩니다.

```yaml
on:
  push:
    paths:
      - "07_multi-agent-service-ops/00_runtime-and-deployment/05_weather-mcp-deployment-project/**"
      - ".github/workflows/07-weather-mcp-cicd.yml"
  pull_request:
    paths:
      - "07_multi-agent-service-ops/00_runtime-and-deployment/05_weather-mcp-deployment-project/**"
      - ".github/workflows/07-weather-mcp-cicd.yml"
  workflow_dispatch:
```

배포 Job의 다음 조건은 `main` Push에서만 배포하도록 제한합니다. Pull Request는 코드 검증만
하며 AWS를 변경하지 않습니다.

```yaml
deploy:
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  needs: test-and-build
  environment: production
```

`needs: test-and-build`는 CI가 실패하면 Deploy Job을 시작하지 않는다는 뜻입니다.
`environment: production`은 GitHub의 Production 승인과 Secret을 사용한다는 뜻입니다.

### 개인 Branch에서 CI 확인

```powershell
git switch -c weather-mcp-lab
git add 07_multi-agent-service-ops/00_runtime-and-deployment/05_weather-mcp-deployment-project
git add .github/workflows/07-weather-mcp-cicd.yml
git commit -m "Add weather MCP deployment lab"
git push -u origin weather-mcp-lab
```

GitHub 저장소의 `Actions` 탭에서 **07 Weather MCP CI CD**를 선택합니다. 실행한 Branch와
Commit이 맞는지 확인하고 `test-and-build` Job을 엽니다. 실패했으면 마지막 줄만 보지 말고
처음 빨간색이 된 Step의 첫 오류부터 확인합니다.

| 실패 Step | 먼저 확인할 내용 |
| --- | --- |
| Install dependencies | Python 버전, requirements 경로·패키지 이름 |
| Test backend contract | 최초 실패 Test, Import·응답 계약 변경 |
| Validate Compose | YAML 들여쓰기, 환경 변수, 파일 경로 |
| Build three images | Dockerfile의 `COPY`, Base Image, requirements |

수정하고 새 Commit을 Push하면 새 CI 실행이 만들어집니다. 이전 실패 실행이 성공으로 바뀌는
것은 아닙니다.

## 6단계: AWS EC2 최초 준비

### 6-1. EC2 생성

AWS Console에서 다음 기준으로 생성합니다. AWS 화면과 제공 Instance Type은 계정·시점에 따라
달라질 수 있으므로 수업에서 지정한 Region과 비용 한도를 우선합니다.

1. EC2의 `Instances`에서 `Launch instances`를 선택합니다.
2. 이름을 `weather-mcp-deployment`로 입력합니다.
3. Amazon Linux 2023 x86_64 AMI를 선택합니다.
4. 수업에서 지정한 Instance Type과 Storage를 선택합니다.
5. 새 Key Pair를 만들거나 지정된 Key Pair를 선택합니다.
6. Public IPv4가 할당되는 Network인지 확인합니다.
7. 생성 후 Instance ID, Public IPv4, Public DNS를 기록합니다.

Private Key는 Git, 메신저, README 또는 EC2 안에 올리지 않습니다. Windows 예시 경로는
다음과 같습니다.

```text
C:\Users\<사용자>\.ssh\weather-mcp-course.pem
```

### 6-2. Security Group

| Port | Source | 목적 |
| ---: | --- | --- |
| `22` | 관리자 접속 경로만 | SSH 배포·관리 |
| `8501` | 수강생 또는 운영자 IP | Streamlit 화면 |

Backend `8000`과 MCP `8010`은 인터넷에 공개하지 않습니다. 특히 `22`를 단순히
`0.0.0.0/0`으로 열어 두지 않습니다.

중요: 현재 예제 Workflow의 CD는 GitHub-hosted Runner가 EC2에 직접 `ssh`와 `scp`를 할 수
있다는 전제가 있습니다. Security Group이 내 PC IP만 허용하면 Runner는 접속할 수 없습니다.
실무에서는 조직 정책에 따라 self-hosted Runner, VPN/Bastion, AWS Systems Manager 또는
검증된 Runner IP 허용 방식을 설계해야 합니다. 네트워크 경로가 준비되지 않은 수업에서는
CI까지만 자동화하고 EC2 배포 명령은 강사가 수동으로 시연합니다.

### 6-3. EC2 접속과 Docker 설치

로컬 PowerShell에서 실제 Key 경로와 DNS로 바꿉니다.

```powershell
ssh -i "C:\Users\<사용자>\.ssh\weather-mcp-course.pem" ec2-user@<PUBLIC_DNS>
```

EC2 터미널에서 실행합니다.

```bash
sudo yum update -y
sudo yum install -y docker git
sudo service docker start
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user
exit
```

SSH로 다시 접속하여 권한과 Compose를 확인합니다.

```bash
docker info
docker compose version
```

`docker compose`가 없다면 다음을 시도합니다.

```bash
sudo yum install -y docker-compose-plugin
docker compose version
```

패키지를 찾지 못하면 임의 설치 Script를 실행하지 말고 Docker 공식 Compose Plugin 설치
절차와 강사가 지정한 버전을 사용합니다.

### 6-4. EC2 배포 폴더와 환경 파일

EC2에서 최초 한 번 만듭니다.

```bash
mkdir -p ~/weather-mcp-deployment
cd ~/weather-mcp-deployment
nano .env
chmod 600 .env
```

```ini
OPENAI_API_KEY=<실제 OpenAI API Key>
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=<실제 Gemini API Key>
GEMINI_MODEL=gemini-3.5-flash
```

한 Provider만 사용한다면 해당 Key만 입력합니다. Workflow는 `.env`를 복사하거나 덮어쓰지
않으며, 로그로 출력하지도 않습니다. `cat .env` 결과를 화면 공유하지 않습니다.

## 7단계: GitHub Production Environment 설정

GitHub 저장소에서 다음 순서로 설정합니다.

1. `Settings`를 선택합니다.
2. `Environments`를 선택합니다.
3. `New environment`에서 이름을 정확히 `production`으로 만듭니다.
4. 사용 가능한 계정에서는 `Required reviewers`에 승인자를 지정합니다.
5. Deployment Branch를 `main`으로 제한합니다.
6. `Environment secrets`에 아래 네 항목을 등록합니다.

| Secret | 입력 내용 |
| --- | --- |
| `AWS_HOST` | EC2 Public DNS 또는 Public IPv4 |
| `AWS_USER` | Amazon Linux 2023의 `ec2-user` |
| `AWS_SSH_PRIVATE_KEY` | 배포 전용 Private Key 전체 내용 |
| `AWS_SSH_KNOWN_HOSTS` | 지문을 검증한 EC2의 known_hosts 한 줄 |

Private Key는 `-----BEGIN ... PRIVATE KEY-----`부터 `-----END ... PRIVATE KEY-----`까지
줄바꿈을 포함해 등록합니다. 값 앞뒤에 따옴표를 추가하지 않습니다.

`AWS_SSH_KNOWN_HOSTS`는 단순히 접속 경고를 무시하기 위한 값이 아닙니다. 먼저 EC2 Console
또는 관리자가 제공한 Host Key Fingerprint를 확인한 뒤, 로컬에서 다음 결과와 대조합니다.

```powershell
ssh-keyscan -H <PUBLIC_DNS>
```

검증한 해당 한 줄을 Secret에 저장합니다. Workflow는 이 값을 `~/.ssh/known_hosts`에 넣어
접속 대상이 예상한 EC2인지 확인합니다.

## 8단계: main 병합과 자동 배포

개인 Branch CI가 성공하면 Pull Request를 만들고 검토 후 `main`에 병합합니다.

```text
개인 Branch Push
→ CI 성공
→ Pull Request 생성·CI 재실행
→ main 병합
→ main CI 재실행
→ production 승인 대기
→ 승인
→ EC2로 Source 복사
→ docker compose config
→ docker compose up -d --build
→ Backend /health/ready 검증
```

Deploy Job은 EC2의 `~/weather-mcp-deployment`에 소스를 복사합니다. 이후 기존 `.env`가 있는지
확인하고 다음과 같은 동작을 원격으로 수행합니다.

```bash
cd ~/weather-mcp-deployment
test -f .env
docker compose config --quiet
docker compose up -d --build
curl --fail --retry 12 --retry-delay 5 http://127.0.0.1:8000/health/ready
```

`.env`가 없거나 Readiness가 끝까지 실패하면 Deploy Job도 실패합니다. GitHub Actions에서
승인 요청이 보이면 변경 Commit과 CI 성공 여부를 확인한 뒤 승인합니다.

## 9단계: 배포 결과 확인

Browser에서 다음 주소를 엽니다.

```text
http://<EC2_PUBLIC_IP>:8501
```

EC2 SSH 터미널에서도 확인합니다.

```bash
cd ~/weather-mcp-deployment
docker compose ps
docker compose logs --tail=100 weather-mcp backend frontend
curl --fail http://127.0.0.1:8000/health/live
curl --fail http://127.0.0.1:8000/health/ready
```

화면에서 실제 날씨를 한 번 조회하여 MCP Tool Result와 LLM 답변까지 확인해야 배포가 완료된
것입니다. Container가 `Up`이라는 사실만으로 외부 API 연동 성공을 판단하지 않습니다.

## 10단계: 실패 진단과 복구

| 증상 | 확인할 곳 | 조치 |
| --- | --- | --- |
| CI가 시작되지 않음 | 변경 경로·Workflow 위치 | `paths`와 저장소 루트 `.github/workflows` 확인 |
| Test 실패 | 최초 빨간 Test Step | 로컬 pytest로 같은 오류 재현 |
| Production 승인 대기 | GitHub Environment | 승인자가 Commit 확인 후 승인 |
| SSH timeout | Security Group·Network 경로 | Runner에서 EC2로 갈 수 있는 승인된 경로 준비 |
| Host key 오류 | `AWS_SSH_KNOWN_HOSTS` | EC2 재생성 여부와 Fingerprint 재검증 |
| `.env` 없음 | EC2 배포 폴더 | EC2에서 최초 환경 파일 생성·권한 `600` 설정 |
| Backend Readiness 실패 | Backend·MCP 로그 | MCP Health, API Key, 내부 URL 확인 |
| 화면 접속 불가 | Frontend 상태·8501 Rule | Container와 허용 Source IP 확인 |

입문 예제는 Blue/Green과 자동 Rollback을 구현하지 않습니다. 문제가 발생하면 마지막 정상
Commit으로 되돌리는 **새 Commit**을 만들고, CI와 Production 승인을 다시 거쳐 배포합니다.
서버에서 임의로 소스만 수정하면 다음 자동 배포에서 덮어써지고 변경 이력도 남지 않습니다.

실습 종료 후에는 비용이 계속 발생하지 않도록 EC2를 중지하거나, 더 이상 사용하지 않는다면
Instance와 관련 Volume·Elastic IP를 확인한 뒤 삭제합니다. 조직 또는 강사가 관리하는 AWS
자원은 임의로 삭제하지 않습니다.

## 완료 체크

```text
[ ] Frontend에서 실제 Open-Meteo Tool Result를 확인했다.
[ ] Weather MCP 8010이 Host에 공개되지 않음을 확인했다.
[ ] Backend Readiness가 MCP Tool 목록을 확인하는 이유를 설명할 수 있다.
[ ] 로컬 pytest·Compose 검사·세 Image Build를 통과했다.
[ ] 개인 Branch Push와 Pull Request에서 CI 결과를 확인했다.
[ ] CI와 CD의 차이 및 Fake MCP·LLM을 쓰는 이유를 설명할 수 있다.
[ ] EC2에 Docker·Compose와 비공개 `.env`를 준비했다.
[ ] GitHub production Environment와 네 개의 Secret을 설정했다.
[ ] 개인 브랜치와 Pull Request에서는 배포되지 않음을 확인했다.
[ ] main CI 성공 후 production 승인을 거쳐 EC2에 배포했다.
[ ] EC2에서 Health와 실제 날씨·LLM 통합 동작을 확인했다.
```
