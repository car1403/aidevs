# 01 Simple Multi-LLM Docker Compose

하나의 여행 준비 Chat으로 Container 연결을 배웁니다. Multi AI Agent와 Orchestration은 아직 넣지 않습니다. 이 폴더는 자체 Redis·PostgreSQL을 사용하므로 `00_local-services`를 먼저 실행하지 않습니다.

```text
Frontend + Backend + Redis + PostgreSQL
                    ↓
        OpenAI·Gemini·Ollama 중 선택
                              └─ Ollama는 선택 Profile
```

## 실행

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\01_simple-multi-llm-compose
Copy-Item .env.example .env
docker compose up --build
```

- Streamlit: `http://127.0.0.1:8503`
- FastAPI: `http://127.0.0.1:8200/docs`
- Health: `http://127.0.0.1:8200/health`

`.env`에는 사용할 실제 Provider 하나 이상을 설정합니다. OpenAI나 Gemini를 사용할 때는 위 명령만 실행합니다.

## Ollama 선택 실행

`.env`를 다음처럼 바꿉니다.

```dotenv
OLLAMA_ENABLED=true
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama3.2
```

Ollama Profile을 함께 실행하고 Model을 최초 한 번 내려받습니다.

```powershell
docker compose --profile ollama up -d --build
docker compose --profile ollama exec ollama ollama pull llama3.2
docker compose --profile ollama exec ollama ollama list
```

Backend Container는 Compose 내부 주소 `http://ollama:11434`로 호출합니다. Host Port를 공개하지 않으므로 Windows의 다른 프로그램에서는 이 Ollama에 직접 접근하지 않습니다.

## 저장소 역할

| 서비스 | 저장 내용 | 유지 방식 |
| --- | --- | --- |
| Redis | 최근 대화·현재 Session·요청 횟수 | 임시 상태, 별도 Volume 없음 |
| PostgreSQL | 전체 Chat 이력·여행 메모 | `postgres_data` Volume |
| Ollama | 내려받은 Model | `ollama_data` Volume |

## 확인 순서

1. `docker compose ps`에서 네 서비스가 실행 중인지 확인합니다.
2. 화면에서 실제 Provider를 선택합니다.
3. 부산 여행 준비 질문을 보냅니다.
4. Redis 최근 Session과 PostgreSQL 전체 이력의 차이를 확인합니다.
5. 설정하지 않은 Provider를 선택해 `503` 오류가 Mock 성공으로 바뀌지 않는지 확인합니다.
6. `docker compose logs --tail=100 backend`에서 첫 실패 지점을 찾습니다.

## 종료

```powershell
docker compose down
```

PostgreSQL 이력과 Ollama Model까지 지우려는 것이 확실할 때만 `docker compose --profile ollama down -v`를 사용합니다. 일반 `down`은 Volume을 유지합니다.

## 직접 확인하기

- 같은 질문을 두 Provider로 실행하고 실제 Provider·Model Metadata를 비교합니다.
- Backend Container를 중지했을 때 Frontend 오류를 확인합니다.
- Redis를 중지했을 때 Health와 로그가 어떻게 달라지는지 확인합니다.
