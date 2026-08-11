# 07 과정 환경 준비

## 1. 필수 환경

- Python 3.11 이상
- VS Code
- Git

Docker Desktop, AWS 계정, Redis, PostgreSQL은 과정 시작의 필수 조건이 아닙니다.
다만 01~03의 실제 LLM 실습에는 GPT 또는 Gemini API Key 하나를 준비하는 것을 권장합니다.

## 2. Python 가상환경

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
Copy-Item .env.example .env
```

단위 스크립트가 공통 `shared` 계약을 찾을 수 있도록 `pip install -e .`를
실행합니다.

```powershell
python -c "import shared; print(shared.__file__)"
```

## 3. 기본 실행 모드

01~03은 작은 결정적 Python 예제로 개념을 이해한 뒤 실제 LLM을 호출합니다.
Mock은 테스트와 강사가 명시적으로 fallback을 보여줄 때만 사용합니다.

```dotenv
LLM_PROVIDER=openai
ALLOW_MOCK_FALLBACK=false
COMPARE_PROVIDERS=openai,gemini,ollama
REDIS_URL=redis://127.0.0.1:6380/0
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5434/multi_agent
LEARNING_STATE_TTL_SECONDS=1800
```

01~03은 실제 LLM, 04~06은 실제 Redis·PostgreSQL을 사용합니다. 테스트는 외부
서비스 없이 결정적으로 실행하며, 실제 연결 실습에서는 오류를 Memory 성공으로
바꾸지 않습니다.

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python .\01_single-vs-multi-agent\01_concept_example.py
python .\01_single-vs-multi-agent\04_real_llm_worker.py
python .\02_role-and-agent-contract\04_real_structured_output.py
python .\03_supervisor-and-routing\03_real_provider_router.py
python .\04_workflow-patterns\05_redis_workflow_state.py
python .\05_agent-orchestration\06_redis_orchestration_state.py
python .\06_langgraph-multi-agent\05_redis_postgres_run.py
```

## 4. LLM Provider 선택 비교

GPT 또는 Gemini 하나를 먼저 연결하고, Ollama는 로컬 모델 준비 후 선택합니다.

```dotenv
LLM_PROVIDER=openai
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
```

```dotenv
LLM_PROVIDER=gemini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash
```

```dotenv
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://127.0.0.1:11435
OLLAMA_MODEL=llama3.2
```

Provider 비교는 01 Worker, 03 Supervisor, 마지막 평가에서 진행합니다. 모든
단원에서 세 Provider를 반복 호출하지 않습니다.

## 5. 데이터와 Queue 선택

개념 단위 테스트와 실제 실습은 다음처럼 구분합니다.

| 목적 | 기본 학습 | 선택 실연동 |
| --- | --- | --- |
| Workflow 현재 상태 | Redis 또는 Upstash | 단위 테스트용 Fake |
| 완료·감사 이력 | PostgreSQL 또는 Supabase | 단위 테스트용 Fake |
| LLM | GPT 또는 Gemini | Local Llama, 테스트용 Mock |

이전 과정에서 사용한 Supabase와 Upstash를 그대로 사용할 수 있습니다. Local
PostgreSQL·Redis는 04~06부터 실제 연결합니다. Docker Compose 작성은 아직 하지
않으며, 이전 과정의 Supabase·Upstash 또는 강사가 준비한 접속 URL을 사용합니다.
PostgreSQL에는 `00_local-runtime/init.sql`의 `learning_runs`, `learning_events`,
`task_runs`, `handoff_events`, `task_events` 테이블을 먼저 생성합니다.

## 6. Backend와 Frontend

현재 구현은 Redis와 PostgreSQL이 준비된 경우 다음처럼 실행합니다.

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'

# 터미널 1
uvicorn app.main:app --app-dir .\11_multi-agent-backend --reload --port 8100

# 터미널 2
python .\10_async-task-and-redis-worker\worker.py

# 터미널 3
streamlit run .\12_multi-agent-frontend\app.py
```

10~12의 통합 서비스에서는 같은 `REDIS_URL`과 `DATABASE_URL`을 재사용합니다.

## 7. 테스트

```powershell
cd C:\aidevs\07_multi-agent-service-ops
python -m pytest -q
```

기본 테스트는 외부 API, 실제 변경 작업, AWS를 호출하지 않아야 합니다. 실제
Provider와 저장소 테스트는 별도 선택 테스트로 구분합니다.

## 8. 선택 운영 실습

Docker Compose·GitHub Actions·AWS EC2는 01~13 완료 후 다음 선택 단원에서 진행합니다.

```text
00_service_ops
├─ 00_windows-docker-setup.md
├─ 01_simple-compose
├─ 02_simple-github-actions
├─ 03_simple-aws-deployment
└─ 04_local-or-managed-cloud.md
```

이 실습에서는 작은 Gemini Chat에 필요한 Redis·PostgreSQL만 사용하고 Multi-Agent
전체 구성은 배포하지 않습니다.

```text
Simple FastAPI Backend + Streamlit Frontend
+ Redis Session + PostgreSQL Chat 이력 + Gemini API
→ Docker Compose
→ GitHub Actions Test·Compose 검사·Build
→ AWS EC2 한 대 수동 배포
→ 장애와 로그 확인
→ EC2·EBS·Security Group 정리
```

## 9. 자주 발생하는 문제

| 증상 | 먼저 확인 |
| --- | --- |
| `shared`를 찾지 못함 | 과정 루트에서 `pip install -e .` 실행 |
| Provider 오류 | API Key·모델명·Ollama 주소 확인, fallback은 오류 확인 후에만 허용 |
| Redis 연결 오류 | `REDIS_URL`, TLS가 필요한 `rediss://`, 비밀번호 확인 |
| PostgreSQL 연결 오류 | `DATABASE_URL`, `learning_runs` 테이블, SSL 설정 확인 |
| Backend가 `degraded` | 현재 Redis 중심 구현인지 확인 |
| Worker가 멈춘 것처럼 보임 | Queue를 기다리는 중인지 로그 확인 |
| Frontend 연결 실패 | Backend 8100 Port와 `MULTI_AGENT_API_URL` 확인 |
| Task가 종료되지 않음 | 최대 단계와 종료 조건 확인 |
