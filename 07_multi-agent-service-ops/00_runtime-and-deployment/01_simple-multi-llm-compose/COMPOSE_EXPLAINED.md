# 두 Docker Compose 구성 이해하기

## 기본 `compose.yml`

현재 수업 PC에 이미 실행 중인 PostgreSQL·Redis·Ollama를 재사용합니다.

```text
frontend Container → backend Container
                         ├─ host.docker.internal:6379 Redis
                         ├─ host.docker.internal:5433 PostgreSQL
                         ├─ host.docker.internal:11434 Ollama
                         ├─ OpenAI HTTPS API
                         └─ Gemini HTTPS API
```

`host.docker.internal`은 Container에서 Windows Host 방향으로 접근하는 이름입니다.
Backend Container에서 `127.0.0.1`은 Backend Container 자기 자신을 뜻합니다.

## 선택 `compose.full-stack.yml`

공용 Container가 없는 PC에서 전체 환경을 별도로 만듭니다.

```text
frontend → backend → redis
                   → database
                   → 선택 ollama
```

같은 Compose Network에서는 `redis`, `database`, `ollama`, `backend` 같은 Service 이름을
DNS 주소로 사용합니다.

## 설정 주소 비교

| 호출 위치 | PostgreSQL | Redis | Ollama |
| --- | --- | --- | --- |
| Host Python | `127.0.0.1:5433` | `127.0.0.1:6379` | `127.0.0.1:11434` |
| 기본 Backend Container | `host.docker.internal:5433` | `host.docker.internal:6379` | `host.docker.internal:11434` |
| Full Stack Backend | `database:5432` | `redis:6379` | `ollama:11434` |

## 환경 변수 역할

```text
POSTGRES_USER·POSTGRES_PASSWORD·POSTGRES_DB
└─ Full Stack PostgreSQL Container 초기 생성

DATABASE_URL
└─ 기본 Backend가 기존 공용 PostgreSQL에 접속

REDIS_URL
└─ 기본 Backend가 기존 공용 Redis에 접속
```

Full Stack Compose는 Backend 주소를 내부 Service 이름으로 명시적으로 바꾸므로 같은
`.env`를 사용해도 Host 주소와 혼동하지 않습니다.

## Volume

기본 Compose는 Application Container만 만들기 때문에 공용 저장소의 기존 Volume을
변경하지 않습니다. Full Stack Compose는 다음 전용 Volume을 만듭니다.

```text
redis_data    → Redis AOF 데이터
postgres_data → Chat과 여행 메모
ollama_data   → 내려받은 Model
```

일반 `down`은 Volume을 유지하고 `down -v`는 삭제합니다.
