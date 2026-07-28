# Setup

## 1. Python

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
Copy-Item .env.example .env
```

## 2. Docker

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_local-runtime
Copy-Item .env.example .env
docker compose up -d
docker compose ps
docker exec multi-agent-ollama ollama pull llama3.2
```

## 3. 단위 예제

`pip install -e .`로 공통 `shared` 계약을 연결한 뒤 과정 루트에서 실행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python .\01_single-vs-multi-agent\01_concept_example.py
python .\05_agent-orchestration\03_moving_example.py
```

## 4. 통합 서비스

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'

# 터미널 1
uvicorn app.main:app --app-dir .\11_multi-agent-backend --reload --port 8100

# 터미널 2
python .\10_async-task-and-redis-worker\worker.py

# 터미널 3
streamlit run .\12_multi-agent-frontend\app.py
```

## 5. 테스트

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python -m pytest -q
```

실제 Provider 테스트는 기본 테스트와 분리합니다. API Key를 설정하지 않은
상태에서는 Mock과 결정적 Python 예제만 실행됩니다.

## 6. Docker Compose 학습

먼저 Frontend와 Backend만 연결합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\13_observability-docker-and-security\01_simple-compose
docker compose up --build
```

단순 연결을 확인한 뒤 전체 Multi-Agent Compose를 실행합니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops\13_observability-docker-and-security\04_multi-agent-compose
Copy-Item .env.example .env
docker compose up --build
```

GitHub Actions와 최소 AWS 수동 배포는
[13단원 가이드](./13_observability-docker-and-security/README.md)를
따릅니다.
