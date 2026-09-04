# 00 Local Runtime

## 역할

이 Compose는 이후 01~09 과정의 독립 Python 예제와 Multi AI Agent Service 개발에 공통으로 사용하는 저장소·Ollama 환경입니다. `01_simple-multi-llm-compose`를 실행할 때는 그 폴더가 자체 Redis·PostgreSQL과 선택 Ollama를 제공하므로 이 공용 환경을 함께 실행할 필요가 없습니다.

| 서비스 | 주소 | 용도 |
| --- | --- | --- |
| Ollama | `http://127.0.0.1:11435` | 로컬 Llama·Gemma |
| PostgreSQL | `127.0.0.1:5434` | Task·Trace 이력 |
| Redis | `127.0.0.1:6380` | Queue·상태·TTL |

05 과정과 동시에 실행해도 포트가 충돌하지 않도록 별도 호스트 포트를 사용합니다.

## 1. 실행 위치 확인

```powershell
cd C:\aidevs\07_multi-agent-service-ops\00_runtime-and-deployment\00_local-services
Get-Location
Get-ChildItem -Force
```

출력에 `docker-compose.yml`과 `.env.example`이 보여야 합니다. 다른 폴더에서 실행하면
다른 Compose 프로젝트를 조작할 수 있으므로 위치부터 확인합니다.

## 2. 환경 변수와 Compose 설정 확인

```powershell
Copy-Item .env.example .env
Get-Content .env
docker compose config --quiet
```

`docker compose config --quiet`가 메시지 없이 끝나면 YAML과 환경 변수 해석에 성공한
것입니다. 오류가 나타나면 `up` 전에 누락 변수와 들여쓰기를 수정합니다.

## 3. 저장소부터 실행

```powershell
docker compose up -d redis postgres
docker compose ps
```

Redis와 PostgreSQL의 상태가 `running` 또는 `healthy`여야 합니다. `exited`이면 먼저
해당 서비스 로그를 확인합니다.

```powershell
docker compose logs --tail=100 redis
docker compose logs --tail=100 postgres
```

## 4. 서비스별 연결 확인

```powershell
docker compose exec redis redis-cli ping
docker compose exec postgres pg_isready -U postgres -d multi_agent
```

Redis는 `PONG`, PostgreSQL은 `accepting connections`를 반환해야 합니다.

```text
Host Python → 127.0.0.1:6380, 127.0.0.1:5434
Compose Service → redis:6379, postgres:5432
```

## 5. Ollama 선택 실행

Ollama를 사용할 때 최초 한 번 Model을 받습니다.

```powershell
docker compose up -d ollama
docker compose exec ollama ollama pull llama3.2
docker compose exec ollama ollama pull gemma
docker compose exec ollama ollama list
```

OpenAI 또는 Gemini만 사용한다면 Ollama를 실행하거나 Model을 받을 필요가 없습니다.

컨테이너 내부 서비스끼리는 기본 포트 `11434`, `5432`, `6379`로 연결합니다.

## 6. 종료와 다시 시작

```powershell
docker compose down
docker compose up -d redis postgres
docker compose ps
```

일반 `docker compose down`은 Volume을 유지합니다. `docker compose down -v`는
PostgreSQL·Redis 데이터와 내려받은 Ollama Model을 삭제하므로 현재 Volume과 학습
데이터를 확인한 뒤 완전 초기화가 확실할 때만 사용합니다.

## 7. 완료 체크

```text
[ ] Compose 설정 검사를 통과했다.
[ ] Redis가 PONG을 반환한다.
[ ] PostgreSQL이 accepting connections를 반환한다.
[ ] Host Port와 Container Port의 차이를 설명할 수 있다.
[ ] down과 down -v의 차이를 설명할 수 있다.
```

