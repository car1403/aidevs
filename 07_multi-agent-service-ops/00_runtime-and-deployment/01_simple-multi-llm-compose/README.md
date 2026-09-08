# 01 Simple Multi-LLM Docker Compose

하나의 여행 준비 Chat으로 Frontend와 Backend Container 연결을 배웁니다. Multi-Agent와
Orchestration은 아직 넣지 않습니다. 현재 수업 PC에는 PostgreSQL·Redis·Ollama Container가
이미 있으므로 기본 실행에서는 Application Container 두 개만 생성합니다.

## 두 실행 방식을 구분하세요

| 파일 | 실행 대상 | 사용하는 경우 |
| --- | --- | --- |
| `compose.yml` | Frontend·Backend | 현재 수업 환경, 기본 권장 |
| `compose.full-stack.yml` | Frontend·Backend·Redis·PostgreSQL·선택 Ollama | 공용 Container가 없는 별도 PC |

두 Compose를 동시에 실행하지 않습니다. 같은 Host Port를 사용하므로 충돌할 수 있습니다.

## 1. 기본 실행: 기존 공용 Container 사용

```text
기존 공용 Container
├─ PostgreSQL :5433
├─ Redis      :6379
└─ Ollama     :11434

이번 Compose
├─ Backend    :8000
└─ Frontend   :8501
```

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose
Copy-Item .env.example .env
docker compose config --quiet
docker compose up --build -d
docker compose ps
```

Backend도 Container이므로 Host의 공용 서비스에는 `127.0.0.1`이 아니라
`host.docker.internal`로 접근합니다.

```ini
DATABASE_URL=postgresql://agent_user:agent_password@host.docker.internal:5433/agent_db
REDIS_URL=redis://host.docker.internal:6379/0
OLLAMA_BASE_URL=http://host.docker.internal:11434
```

## 2. 전체 실행: 공용 Container가 없는 PC

이 방식은 자체 Network 안에 저장소를 생성합니다.

```powershell
docker compose -f .\compose.full-stack.yml config --quiet
docker compose -f .\compose.full-stack.yml up --build -d
docker compose -f .\compose.full-stack.yml ps
docker compose -f .\compose.full-stack.yml exec redis redis-cli ping
docker compose -f .\compose.full-stack.yml exec database pg_isready -U agent_user -d agent_db
```

Full Stack 내부에서는 Compose Service 이름을 사용합니다.

```text
Backend → redis:6379
Backend → database:5432
Backend → 선택 Ollama: ollama:11434
```

## 3. 실제 LLM 설정

`.env`에 OpenAI 또는 Gemini Key를 입력합니다.

```ini
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.5-flash
```

기존 공용 Ollama를 사용할 때:

```ini
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://host.docker.internal:11434
OLLAMA_MODEL=llama3.2
GEMMA_MODEL=gemma
```

Full Stack이 Ollama까지 새로 만들 때만 Profile을 사용합니다.

```powershell
docker compose -f .\compose.full-stack.yml --profile ollama up --build -d
docker compose -f .\compose.full-stack.yml --profile ollama exec ollama ollama pull llama3.2
docker compose -f .\compose.full-stack.yml --profile ollama exec ollama ollama pull gemma
docker compose -f .\compose.full-stack.yml --profile ollama exec ollama ollama list
```

## 4. 실행 확인

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health/live
Invoke-RestMethod http://127.0.0.1:8000/health
Invoke-RestMethod http://127.0.0.1:8000/health/ready
```

| 확인 대상 | 주소 |
| --- | --- |
| Streamlit | `http://127.0.0.1:8501` |
| FastAPI 문서 | `http://127.0.0.1:8000/docs` |
| Liveness | `http://127.0.0.1:8000/health/live` |
| Readiness | `http://127.0.0.1:8000/health/ready` |

- Liveness: Backend Process가 살아 있는지 확인합니다.
- Readiness: PostgreSQL과 Redis를 포함해 요청을 받을 준비가 됐는지 확인합니다.
- 설정하지 않은 Provider 오류는 Mock 성공으로 바꾸지 않습니다.

## 5. 저장소 역할

| 서비스 | 저장 내용 | 기본 실행에서 관리 위치 |
| --- | --- | --- |
| Redis | 최근 대화·Session·요청 횟수 | 기존 공용 Redis Container |
| PostgreSQL | 전체 Chat 이력·여행 메모 | 기존 공용 PostgreSQL Container |
| Ollama | Llama·Gemma Model | 기존 공용 Ollama Container |

Full Stack 방식에서는 이 폴더의 `redis_data`, `postgres_data`, `ollama_data` Volume을
사용합니다.

## 6. 종료

기본 Application만 종료:

```powershell
docker compose down
```

이 명령은 기존 공용 PostgreSQL·Redis·Ollama를 중단하지 않습니다.

Full Stack 종료:

```powershell
docker compose -f .\compose.full-stack.yml down
```

`down -v`는 PostgreSQL 데이터와 Ollama Model을 삭제합니다. 학습 데이터가 필요 없는지
확인하지 않았다면 실행하지 않습니다.

## 완료 체크

```text
[ ] 기본 Compose가 Frontend와 Backend만 생성하는 것을 확인했다.
[ ] host.docker.internal과 localhost의 차이를 설명할 수 있다.
[ ] Full Stack Compose를 언제 사용하는지 설명할 수 있다.
[ ] Liveness와 Readiness를 구분할 수 있다.
[ ] 실제 Provider 오류가 성공으로 표시되지 않음을 확인했다.
```
