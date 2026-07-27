# 05 과정 환경 준비

## 1. 기본 환경

- Python 3.11 이상 권장
- VS Code
- Git
- 선택: Docker Desktop
- 필수 실연동: Docker Desktop
- 필수 실연동: OpenAI API Key
- Provider 비교: Gemini API Key

모든 필수 예제는 `APP_MODE=mock`으로 실행할 수 있습니다.

## 2. 가상환경과 패키지

```powershell
cd C:\aidevs\05_llm-agent-orchestration
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Python 경로를 확인합니다.

```powershell
python -c "import sys; print(sys.executable)"
```

## 3. 환경 변수

```powershell
Copy-Item .env.example .env
```

기본값:

```dotenv
APP_MODE=mock
LLM_PROVIDER=mock
OPENAI_MODEL=gpt-4.1-mini
PYTHON_AGENT_API_URL=http://127.0.0.1:8000
LANGGRAPH_AGENT_API_URL=http://127.0.0.1:8001
```

실제 OpenAI 연결을 선택하는 경우에만 `OPENAI_API_KEY`를 설정합니다. `.env`는 Git에 올리지 않습니다.

## 4. Local Docker 환경

[00_local-runtime](./00_local-runtime/README.md)의 순서로 다음 컨테이너를 준비합니다.

```text
Ollama/Llama          http://127.0.0.1:11434
PostgreSQL/pgvector   127.0.0.1:5433
Redis                 127.0.0.1:6379
```

Docker 상태와 연결을 확인합니다.

```powershell
docker ps
python .\00_local-runtime\05_environment_diagnostics.py
```

## 5. 단위 예제

```powershell
python .\01_llm-to-agent\01_concept_example.py
python .\01_llm-to-agent\02_travel_example.py
```

각 단원의 README에 실행 순서가 있습니다.

## 6. 두 Backend

Python Agent Backend:

```powershell
cd .\10_python-agent-backend
uvicorn app.main:app --reload --port 8000
```

새 PowerShell에서 LangGraph Agent Backend:

```powershell
cd C:\aidevs\05_llm-agent-orchestration\11_langgraph-agent-backend
uvicorn app.main:app --reload --port 8001
```

확인 주소:

```text
Health: http://127.0.0.1:8000/health
Docs:   http://127.0.0.1:8000/docs
Health: http://127.0.0.1:8001/health
Docs:   http://127.0.0.1:8001/docs
```

## 7. 통합 Frontend

새 PowerShell에서 실행합니다.

```powershell
cd C:\aidevs\05_llm-agent-orchestration
.\.venv\Scripts\Activate.ps1
streamlit run .\12_agent-frontend\app.py
```

## 8. 테스트

Python Backend:

```powershell
cd C:\aidevs\05_llm-agent-orchestration
$env:PYTHONPATH="C:\aidevs\05_llm-agent-orchestration\10_python-agent-backend"
pytest .\10_python-agent-backend\tests
```

LangGraph Backend:

```powershell
$env:PYTHONPATH="C:\aidevs\05_llm-agent-orchestration\11_langgraph-agent-backend"
pytest .\11_langgraph-agent-backend\tests
```

두 Backend가 각각 `app` 패키지를 사용하므로 테스트도 별도 프로세스로 실행합니다.

## 9. 실행 모드

Mock:

```dotenv
APP_MODE=mock
LLM_PROVIDER=mock
STORAGE_MODE=memory
```

GPT와 Docker 저장소:

```dotenv
APP_MODE=real
LLM_PROVIDER=openai
STORAGE_MODE=postgres
```

Gemini 또는 Ollama 비교:

```dotenv
LLM_PROVIDER=gemini
```

```dotenv
LLM_PROVIDER=ollama
```

## 10. 선택 환경

pgvector, Redis, Ollama는 해당 단원의 확장 실습에서만 사용합니다. Dockerfile과 Docker Compose 운영은 `07_multi-agent-service-ops`에서 학습합니다.

## 11. 자주 발생하는 문제

| 증상 | 확인 |
| --- | --- |
| 모듈을 찾지 못함 | 가상환경과 현재 폴더 확인 |
| API Key 오류 | `APP_MODE=mock`으로 먼저 실행 |
| Backend 연결 실패 | 두 Uvicorn 포트와 `PYTHON_AGENT_API_URL`, `LANGGRAPH_AGENT_API_URL` 확인 |
| 날짜 검증 오류 | ISO 날짜 `YYYY-MM-DD` 사용 |
| Streamlit 상태 초기화 | `st.session_state` key 확인 |
| LangGraph 재개 실패 | 동일한 `thread_id` 사용 여부 확인 |
| `xxhash` DLL 차단 | 교육장 PC의 애플리케이션 제어 정책 확인 또는 허용된 개발 컨테이너/WSL 사용 |

일부 Windows 교육장 PC는 가상환경 내부의 네이티브 DLL을 차단할 수 있습니다.
이 경우 Python Workflow와 Mock/API 실습은 계속할 수 있지만 LangGraph import는
실패할 수 있습니다. 이는 예제 로직이 아니라 PC 보안 정책 문제입니다.
