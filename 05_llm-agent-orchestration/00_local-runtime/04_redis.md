# Docker Redis

## 실행

```powershell
docker run -d `
  --name aidevs-redis `
  -p 6379:6379 `
  -v aidevs-redis-data:/data `
  redis:7 `
  redis-server --appendonly yes
```

## 연결 확인

```powershell
docker exec -it aidevs-redis redis-cli PING
```

예상 결과:

```text
PONG
```

## TTL 실습

```powershell
docker exec -it aidevs-redis redis-cli SETEX agent:session:demo 60 active
docker exec -it aidevs-redis redis-cli TTL agent:session:demo
docker exec -it aidevs-redis redis-cli GET agent:session:demo
```

## Key 규칙

```text
agent:session:{user_id}:{session_id}
agent:run:{run_id}
agent:cache:{provider}:{prompt_hash}
```

사용자별 Prefix와 TTL을 적용합니다. Redis를 장기 보존이 필요한 사용자 데이터의 유일한 저장소로 사용하지 않습니다.
