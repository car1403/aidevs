# 장애 실습과 문제 해결

오류를 만들기 전에 정상 화면과 `docker compose ps`를 먼저 기록합니다. 한 번에 한
서비스만 중단해야 원인과 결과를 연결할 수 있습니다.

## 공통 관찰 명령

```powershell
docker compose ps
docker compose logs --tail=100
docker compose logs --tail=100 backend
docker compose logs --tail=100 frontend
```

## 1. Redis 중단

```powershell
docker compose stop redis
```

예상:

- PostgreSQL의 기존 메모와 Chat 이력은 조회 가능
- 메모 저장은 가능하지만 Redis 통계 경고가 함께 반환될 수 있음
- Redis 통계와 새 Chat 처리는 503 오류
- 오류를 가짜 성공으로 표시하지 않음

복구:

```powershell
docker compose start redis
```

## 2. PostgreSQL 중단

```powershell
docker compose stop database
```

예상:

- Redis 통계는 조회 가능
- 메모 저장·조회와 Chat 영구 이력은 503 오류
- Gemini가 응답할 수 있어도 Chat 전체 처리는 완료로 표시하지 않음

복구:

```powershell
docker compose start database
```

## 3. Backend 중단

```powershell
docker compose stop backend
```

예상:

- Streamlit 화면 자체는 열릴 수 있음
- 모든 API 동작은 Backend 연결 실패 표시

복구:

```powershell
docker compose start backend
```

## 4. 잘못된 Container 주소

Frontend의 `BACKEND_URL`을 `http://localhost:8200`으로 바꾸면 Frontend Container는
자기 자신에서 Backend를 찾습니다. 올바른 값은 다음과 같습니다.

```text
http://backend:8200
```

## 5. LLM Provider 설정 오류

Ollama를 선택했다면 `.env`의 `OLLAMA_ENABLED=true`, `--profile ollama` 실행과 Model 다운로드를 모두 확인합니다.

```powershell
docker compose --profile ollama ps
docker compose --profile ollama exec ollama ollama list
docker compose logs --tail=100 backend ollama
```

증상:

- Health의 `gemini_configured`가 `false`
- `/api/chat`이 503 반환
- 메모·Redis·PostgreSQL 기능은 계속 동작

확인:

```powershell
docker compose config
docker compose logs --tail=100 backend
```

`docker compose config` 출력에는 Secret 값이 표시될 수 있으므로 화면 공유·과제 제출에
그 출력을 그대로 첨부하지 않습니다.

## 6. SQL 수정이 반영되지 않음

`init.sql`은 빈 PostgreSQL Volume을 처음 초기화할 때 실행됩니다. 학습 데이터를
삭제해도 되는지 먼저 확인한 뒤에만 다음 명령으로 Volume을 새로 만듭니다.

```powershell
docker compose down -v
docker compose up --build
```

## 완료 체크

```text
[ ] 중단한 서비스 하나를 정확히 찾았다.
[ ] 다른 저장소에 남아 있는 기능을 확인했다.
[ ] 로그에서 첫 오류를 찾았다.
[ ] 복구 후 Health가 정상으로 돌아왔다.
[ ] down -v가 왜 위험한지 설명한다.
```
