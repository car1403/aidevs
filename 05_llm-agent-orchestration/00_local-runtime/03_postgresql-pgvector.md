# Docker PostgreSQL과 pgvector

## 실행

```powershell
docker run -d `
  --name aidevs-pgvector `
  -p 5433:5432 `
  -e POSTGRES_DB=agent_db `
  -e POSTGRES_USER=agent_user `
  -e POSTGRES_PASSWORD=agent_password `
  -v aidevs-pgvector-data:/var/lib/postgresql/data `
  pgvector/pgvector:pg16
```

## 연결과 Schema

```powershell
docker exec -i aidevs-pgvector `
  psql -U agent_user -d agent_db `
  -f /dev/stdin
```

PowerShell에서 SQL 파일을 적용하는 자세한 방법은 환경에 따라 다를 수 있으므로, 다음 명령으로 먼저 extension을 확인합니다.

```powershell
docker exec -it aidevs-pgvector `
  psql -U agent_user -d agent_db `
  -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

Python Schema 적용:

```powershell
python .\00_local-runtime\database\apply_schema.py
```

## 역할

- `documents`: RAG Chunk와 Embedding
- `user_memories`: 사용자 장기 선호
- `conversation_messages`: 대화 이력
- `agent_runs`: Agent 실행 결과

서로 다른 Embedding 모델의 Vector는 같은 collection에서 비교하지 않습니다.
