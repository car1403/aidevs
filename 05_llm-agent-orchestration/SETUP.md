# 05 과정 환경 준비

## 1. 기본 환경

- Python 3.11 이상 권장
- VS Code
- Git
- 선택 실연동: Docker Desktop
- GPT·이미지·TTS 실습: OpenAI API Key
- Gemini 비교 실습: Gemini API Key

모든 필수 예제는 `APP_MODE=mock`으로 실행할 수 있습니다.

## 1.1 권장 학습 경로

Docker가 처음이라면 모든 환경을 한 번에 설치하지 않습니다.

| 시점 | 실행 모드 | 필요한 환경 |
| --- | --- | --- |
| `01`~`04` 기본 예제 | Mock | Python과 `.venv` |
| `05` RAG 기본 예제 | Memory Mock | Python과 `.venv` |
| `05` pgvector 확장 | Local Database | Docker Desktop, PostgreSQL/pgvector |
| `06` Memory 확장 | Local Cache/Database | Docker Desktop, Redis, PostgreSQL |
| Provider 비교 | Real 또는 Local LLM | API Key 또는 Docker Ollama |
| `10`~`13` 통합 | Mock부터 시작 | 두 Backend와 Streamlit |

먼저 Mock으로 Agent의 계약과 흐름을 이해한 뒤 필요한 서비스만 추가합니다.
Docker가 설치되지 않았다는 이유로 초반 단원 학습을 중단할 필요는 없습니다.

## 1.2 이전 Cloud 환경과의 관계

- Supabase 대신 로컬 PostgreSQL을 사용해 DB와 pgvector의 내부 동작을 확인합니다.
- Upstash 대신 로컬 Redis를 사용해 Key, TTL, 재시작을 직접 관찰합니다.
- Render 대신 내 PC에서 Container의 Port와 실행 상태를 관리해 봅니다.
- Streamlit은 계속 Frontend로 사용하며 연결 대상만 두 Agent Backend로 바뀝니다.
- OpenAI·Gemini와 별도로 Ollama를 실행해 Cloud LLM과 Local LLM을 비교합니다.

로컬 서비스는 Cloud 서비스보다 우수해서 선택하는 것이 아니라 학습자가 시작,
중지, 데이터, 로그, 장애를 모두 통제할 수 있기 때문에 사용합니다. 운영 환경에서는
관리 편의성, 비용, 보안, 가용성을 검토해 관리형 서비스 사용 여부를 결정합니다.

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
OPENAI_VISION_MODEL=gpt-4.1-mini
OPENAI_TTS_MODEL=gpt-4o-mini-tts
OPENAI_TTS_VOICE=coral
MAX_IMAGE_SIZE_MB=5
PYTHON_AGENT_API_URL=http://127.0.0.1:8000
LANGGRAPH_AGENT_API_URL=http://127.0.0.1:8001
```

실제 OpenAI 연결을 선택하는 경우에만 `OPENAI_API_KEY`를 설정합니다. `.env`는 Git에 올리지 않습니다.

## 4. Local Docker 환경

Docker Desktop만 Windows에 설치하고, Ollama·PostgreSQL·Redis는 각각 Docker
Container로 격리해 실행합니다. 자세한 개념과 명령은
[00_local-runtime](./00_local-runtime/README.md)에서 확인합니다.

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
cd .\09_python-agent-backend
uvicorn app.main:app --reload --port 8000
```

새 PowerShell에서 LangGraph Agent Backend:

```powershell
cd C:\aidevs\05_llm-agent-orchestration\10_langgraph-agent-backend
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
streamlit run .\11_agent-frontend\app.py
```

## 8. 테스트

Python Backend:

```powershell
cd C:\aidevs\05_llm-agent-orchestration\09_python-agent-backend
..\.venv\Scripts\python.exe -m pytest tests -q
```

LangGraph Backend:

```powershell
cd C:\aidevs\05_llm-agent-orchestration\10_langgraph-agent-backend
..\.venv\Scripts\python.exe -m pytest tests -q
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

Frontend에서는 Sidebar에서 Provider를 선택할 수 있습니다. 실제 비교 전에
`환경 상태` 화면에서 설정 여부를 확인합니다. Tool 평가 1회는 현재 시나리오
기준으로 Provider당 3회의 LLM 호출을 사용합니다. 이미지 분석과 TTS는
OpenAI 전용 선택 실습이며 일반 Provider 선택과 분리됩니다.

## 10. 선택 환경

pgvector, Redis, Ollama는 해당 단원의 확장 실습에서만 사용합니다. Dockerfile과 Docker Compose 운영은 `07_multi-agent-service-ops`에서 학습합니다.

`07`에서는 다음 순서로 확장합니다.

```text
Dockerfile 작성
→ Docker Compose로 Frontend와 Backend 연결
→ Worker·Redis·PostgreSQL·Ollama 통합
→ GitHub Actions에서 Test·Compose 검사·Image Build
→ AWS EC2에서 Simple Compose 수동 배포
→ 비용이 발생하는 EC2·EBS·Security Group 정리
```

Docker Compose 파일 자체가 AWS의 모든 운영 문제를 해결하는 것은 아닙니다.
`07`에서는 학습 범위를 명확히 하기 위해 EC2 한 대에서 수동 Compose 배포를 먼저
경험하고, 완전한 CI/CD와 관리형 Container 운영은 선택 확장으로 구분합니다.

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
