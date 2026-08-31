# 00 Local Runtime

## 역할

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

컨테이너 내부 서비스끼리는 기본 포트 `11434`, `5432`, `6379`로 연결합니다.

