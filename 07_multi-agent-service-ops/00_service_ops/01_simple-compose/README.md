# 01 Gemini Chat with Docker Compose

처음 Docker Compose를 배우는 학생을 위한 작은 완성 프로그램입니다.

```text
Frontend + Backend + Redis + PostgreSQL + Gemini API
```

Multi-Agent, RAG, Tool 호출은 넣지 않습니다. 이번 목표는 여러 서비스를 한 파일로
실행하고 연결·저장·장애를 눈으로 확인하는 것입니다.

## 1. 완성 화면에서 할 수 있는 일

- Gemini에게 이사 준비 질문하기
- PostgreSQL에 전체 사용자·AI 대화 저장하기
- Redis에 현재 Session의 최근 대화 저장하기
- PostgreSQL에 이사 메모 저장하고 다시 조회하기
- Redis 요청 횟수와 최근 요청 확인하기
- 네 서비스의 Health 상태 확인하기

Gemini API Key가 없어도 메모와 저장소 실습은 가능합니다. Chat 호출만 명확한
`503` 오류를 반환하며 Mock 답변으로 바꾸지 않습니다.

## 2. 서비스 지도

```text
Windows Browser :8503
        │
        ▼
frontend:8501
        │  http://backend:8200
        ▼
backend:8200
   ├─ redis:6379
   ├─ database:5432
   └─ HTTPS → Gemini API
```

| 호출하는 위치 | 올바른 주소 | 이유 |
| --- | --- | --- |
| Windows Browser | `http://127.0.0.1:8503` | Compose가 Host 8503을 공개 |
| Windows에서 Backend 확인 | `http://127.0.0.1:8200` | Backend Port를 학습용으로 공개 |
| Frontend Container | `http://backend:8200` | Compose 서비스 이름으로 호출 |
| Backend Container → Redis | `redis://redis:6379/0` | `redis`가 내부 DNS 이름 |
| Backend Container → PostgreSQL | `...@database:5432/...` | `database`가 내부 DNS 이름 |

Container 안의 `localhost`는 Windows가 아니라 **그 Container 자신**입니다.

## 3. 파일 구조

```text
01_simple-compose
├─ compose.yml                 네 서비스를 함께 정의
├─ .env.example               Secret 이름만 제공
├─ database
│  └─ init.sql                최초 Volume 생성 때 Table 생성
├─ backend
│  ├─ app.py                  FastAPI와 API 계약
│  ├─ services.py             Redis·PostgreSQL·Gemini 연결
│  ├─ test_app.py             외부 서비스 없는 단위 테스트
│  ├─ requirements.txt
│  └─ Dockerfile
└─ frontend
   ├─ app.py                  Streamlit Chat·메모·상태 화면
   ├─ requirements.txt
   └─ Dockerfile
```

Redis와 PostgreSQL은 공식 Image를 사용하므로 별도 Dockerfile이 없습니다.

## 4. 시작 전 확인

[Windows Docker 사전 준비](../00_windows-docker-setup.md)를 먼저 완료합니다.

```powershell
docker version
docker compose version
docker run --rm hello-world
```

`docker version`에는 Client와 Server가 모두 보여야 합니다.

## 5. 환경 변수 준비

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_service_ops\01_simple-compose
Copy-Item .env.example .env
```

`.env`를 열어 Gemini Key를 입력합니다.

```dotenv
GEMINI_API_KEY=본인의_API_KEY
GEMINI_MODEL=gemini-3.6-flash
```

Key가 없다면 빈 값으로 두고 메모·Redis·PostgreSQL부터 실습합니다. `.env`는 Git에
Commit하지 않습니다. Backend는 Key를 환경 변수로만 읽습니다.

## 6. 처음 실행

```powershell
docker compose up --build
```

첫 실행은 Image와 Python 패키지를 내려받기 때문에 시간이 걸릴 수 있습니다.

```text
--build : Dockerfile로 Backend·Frontend Image 생성
up      : Network·Volume·Container 생성 후 실행
```

로그가 계속 보이는 것이 정상입니다. 별도 PowerShell을 열어 상태를 확인합니다.

```powershell
docker compose ps
```

기대 서비스:

```text
frontend
backend
redis
database
```

## 7. 접속

- Streamlit: `http://127.0.0.1:8503`
- FastAPI 문서: `http://127.0.0.1:8200/docs`
- 전체 Health: `http://127.0.0.1:8200/health`
- Backend Process: `http://127.0.0.1:8200/health/live`

## 8. 첫 번째 확인: Frontend와 Backend

Streamlit의 `서비스 상태`에서 Health를 확인합니다.

```json
{
  "status": "ok",
  "checks": {
    "backend": true,
    "redis": true,
    "database": true,
    "gemini_configured": true
  }
}
```

`gemini_configured`가 `false`여도 Redis와 Database가 `true`라면 메모 실습은
진행할 수 있습니다.

## 9. 두 번째 확인: Redis

메모를 저장하거나 Chat을 한 번 호출한 뒤 확인합니다.

```powershell
docker compose exec redis redis-cli GET service_ops:request_count
docker compose exec redis redis-cli GET service_ops:recent_request
docker compose exec redis redis-cli KEYS "service_ops:session:*"
```

Redis에는 현재 대화에 필요한 최근 메시지만 최대 12개, 기본 30분 동안 유지합니다.
전체 이력 저장소로 사용하지 않습니다.

## 10. 세 번째 확인: PostgreSQL

화면에서 메모를 저장한 뒤 실행합니다.

```powershell
docker compose exec database `
  psql -U service_ops -d service_ops `
  -c "SELECT id, name, message, created_at FROM notes ORDER BY id DESC;"
```

Chat 이력:

```powershell
docker compose exec database `
  psql -U service_ops -d service_ops `
  -c "SELECT session_id, role, content FROM chat_messages ORDER BY id;"
```

`database/init.sql`은 PostgreSQL Volume을 처음 만들 때만 실행됩니다. SQL을 수정했는데
Table이 바뀌지 않는다면 기존 Volume이 유지되고 있는지 먼저 확인합니다.

## 11. 네 번째 확인: Gemini Chat

Streamlit의 `Gemini Chat`에서 질문합니다.

```text
냉장고 1대와 상자 10개를 이사할 때 준비 순서를 알려줘.
```

확인할 것:

1. 사용자 질문이 PostgreSQL에 저장됩니다.
2. Backend가 Redis의 최근 Session을 읽습니다.
3. Backend가 Gemini API를 호출합니다.
4. Gemini 답변이 PostgreSQL과 Redis에 저장됩니다.
5. Frontend가 답변과 실제 Model 이름을 표시합니다.

API Key 오류는 Backend 로그에서 확인합니다.

```powershell
docker compose logs --tail=100 backend
```

## 12. 종료와 다시 시작

일반 종료:

```powershell
docker compose down
```

다시 시작:

```powershell
docker compose up -d
```

PostgreSQL 메모와 Chat 이력은 `postgres_data` Volume에 남습니다. Redis에는 Volume을
연결하지 않았으므로 Container를 제거하면 현재 Session은 사라질 수 있습니다.

## 13. 완전 초기화

먼저 Volume 이름을 확인합니다.

```powershell
docker volume ls
```

이 실습의 PostgreSQL 데이터까지 지우려는 것이 확실할 때만 실행합니다.

```powershell
docker compose down -v
```

`-v`는 복구 명령이 아니라 영구 데이터 초기화 명령입니다.

## 14. 다음 학습

- [compose.yml 줄별 이해](./COMPOSE_EXPLAINED.md)
- [장애 실습과 문제 해결](./TROUBLESHOOTING.md)
- [GitHub Actions](../02_simple-github-actions/README.md)
- [AWS EC2](../03_simple-aws-deployment/README.md)
- [로컬 Docker와 관리형 Cloud 선택](../04_local-or-managed-cloud.md)

## 공식 문서

- [Gemini API Key와 Python 예제](https://ai.google.dev/gemini-api/docs/generate-content/api-key)
- [Docker Compose](https://docs.docker.com/compose/)
- [Docker Compose 실행](https://docs.docker.com/reference/cli/docker/compose/up/)
