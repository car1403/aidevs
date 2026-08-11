# compose.yml 줄별 이해

Compose 파일은 여러 `docker run` 명령을 한 YAML 파일에 기록한 것입니다. YAML은
들여쓰기가 구조이므로 Tab 대신 Space를 사용합니다.

## 최상위 `services`

```yaml
services:
  redis:
  database:
  backend:
  frontend:
```

각 이름은 Container 사이에서 사용할 DNS 이름이 됩니다. 따라서 Backend는 Redis를
`redis`, PostgreSQL을 `database`라는 Hostname으로 찾습니다.

## `image`와 `build`

```yaml
redis:
  image: redis:7-alpine

backend:
  build: ./backend
```

- `image`: 이미 만들어진 Image를 Registry에서 받음
- `build`: 우리 Dockerfile을 읽어 새 Image를 만듦
- `alpine`: 작은 Linux 기반 Image 변형

Redis·PostgreSQL은 공식 Image를 사용하고, 우리가 작성한 Frontend·Backend만 Build합니다.

## `ports`

```yaml
ports:
  - "8503:8501"
```

```text
왼쪽 8503: Windows Host Port
오른쪽 8501: Container 내부 Port
```

Redis와 PostgreSQL에는 `ports`가 없습니다. Backend만 접근하므로 Windows와 인터넷에
공개할 이유가 없기 때문입니다.

## `environment`

```yaml
environment:
  REDIS_URL: redis://redis:6379/0
  GEMINI_API_KEY: ${GEMINI_API_KEY:-}
```

첫 값은 Compose 내부 주소입니다. 두 번째 값은 `.env`의 `GEMINI_API_KEY`를 Container에
전달합니다. `${이름:-}`은 값이 없을 때 빈 문자열을 사용한다는 뜻입니다.

## `depends_on`과 Healthcheck

```yaml
depends_on:
  database:
    condition: service_healthy
```

Container Process가 시작됐다고 Database가 즉시 Query를 받을 준비가 된 것은 아닙니다.
`healthcheck`가 `healthy`가 될 때까지 Backend 시작을 기다립니다.

Healthcheck는 애플리케이션 기능 전체를 보장하지 않습니다. “다음 서비스가 시작해도
되는 최소 준비 상태인가?”를 확인합니다.

## Named Volume

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

`postgres_data`는 Docker가 관리하는 Named Volume입니다. PostgreSQL Container를
지웠다가 다시 만들어도 데이터가 Volume에 남을 수 있습니다.

```yaml
volumes:
  postgres_data:
```

최하단 선언은 이 Compose가 사용할 Named Volume을 등록합니다.

## Bind Mount

```yaml
- ./database/init.sql:/docker-entrypoint-initdb.d/01-init.sql:ro
```

Windows의 `init.sql`을 PostgreSQL Container 안에 읽기 전용(`ro`)으로 연결합니다.
PostgreSQL 공식 Image는 빈 데이터 폴더를 처음 만들 때 이 위치의 SQL을 실행합니다.

## 자동 Network

별도의 `networks`를 쓰지 않아도 Compose는 Project 전용 기본 Network를 만듭니다.

```text
frontend → backend
backend → redis
backend → database
```

Windows Browser는 이 내부 이름을 알지 못하므로 공개된 `127.0.0.1:8503`을 사용합니다.

## 자주 쓰는 명령

| 명령 | 의미 |
| --- | --- |
| `docker compose up --build` | Image Build 후 앞에서 실행 |
| `docker compose up -d` | 뒤에서 실행 |
| `docker compose ps` | 서비스 상태 확인 |
| `docker compose logs -f backend` | Backend 로그 계속 보기 |
| `docker compose exec redis redis-cli ping` | 실행 중 Redis 안에서 명령 |
| `docker compose stop redis` | Redis만 중단 |
| `docker compose start redis` | 기존 Redis 다시 시작 |
| `docker compose down` | Container와 Network 정리 |
| `docker compose down -v` | Volume까지 삭제 |

처음에는 명령을 외우기보다 “무엇을 만들고, 무엇을 유지하고, 무엇을 삭제하는가”를
말로 설명한 다음 실행합니다.
