# 00 Local Runtime

## 역할

이 Compose는 이후 01~09 과정의 독립 Python 예제와 Multi AI Agent Service 개발에 공통으로 사용하는 저장소·Ollama 환경입니다. `01_simple-multi-llm-compose`를 실행할 때는 그 폴더가 자체 Redis·PostgreSQL과 선택 Ollama를 제공하므로 이 공용 환경을 함께 실행할 필요가 없습니다.

| 서비스 | 주소 | 용도 |
| --- | --- | --- |
| Ollama | `http://127.0.0.1:11435` | 로컬 Llama |
| PostgreSQL | `127.0.0.1:5434` | Task·Trace 이력 |
| Redis | `127.0.0.1:6380` | Queue·상태·TTL |

05 과정과 동시에 실행해도 포트가 충돌하지 않도록 별도 호스트 포트를 사용합니다.

```powershell
Copy-Item .env.example .env
docker compose up -d
docker compose ps
```

Ollama를 사용할 때 최초 한 번 Model을 받습니다.

```powershell
docker compose exec ollama ollama pull llama3.2
docker compose exec ollama ollama list
```

컨테이너 내부 서비스끼리는 기본 포트 `11434`, `5432`, `6379`로 연결합니다.

일반 `docker compose down`은 Volume을 유지합니다. `docker compose down -v`는 PostgreSQL·Redis 데이터와 내려받은 Ollama Model을 삭제하므로 완전 초기화가 확실할 때만 사용합니다.

