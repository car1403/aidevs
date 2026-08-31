# Compose 핵심 이해

## 기본 실행 서비스

```text
frontend → backend → redis
                   → database
                   → OpenAI 또는 Gemini API
```

Frontend와 Backend만 자체 Dockerfile로 Image를 만들고 Redis와 PostgreSQL은 공식 Image를 사용합니다.

## 선택 Ollama Profile

```yaml
ollama:
  profiles: ["ollama"]
  image: ollama/ollama:latest
  volumes:
    - ollama_data:/root/.ollama
```

기본 `docker compose up`에서는 Ollama를 만들지 않습니다. 다음 명령에서만 실행합니다.

```powershell
docker compose --profile ollama up -d --build
```

Backend에서 Ollama Container를 호출하는 주소는 `http://ollama:11434`입니다. `ollama`는 Compose 내부 DNS 서비스 이름입니다.

## Redis와 PostgreSQL 주소

```text
Backend → redis://redis:6379/0
Backend → postgresql://...@database:5432/service_ops
```

Container 내부에서는 Windows의 `localhost`가 아니라 Compose 서비스 이름을 사용합니다.

## Volume

```text
postgres_data → 전체 Chat과 여행 메모
ollama_data   → 내려받은 Model
Redis         → 이 예제에서는 임시 상태라 Volume 없음
```

`docker compose down`은 Volume을 유지합니다. `down -v`는 PostgreSQL 데이터와 Ollama Model을 삭제합니다.

## Provider 환경 변수

```text
OpenAI  → OPENAI_API_KEY, OPENAI_MODEL
Gemini  → GEMINI_API_KEY, GEMINI_MODEL
Ollama  → OLLAMA_ENABLED, OLLAMA_BASE_URL, OLLAMA_MODEL
```

설정하지 않은 Provider는 `503`을 반환하며 Mock으로 대체되지 않습니다.
