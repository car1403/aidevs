# 00 Local Runtime

Docker에서 Ollama/Llama, PostgreSQL/pgvector, Redis를 실행하고 Python에서 연결을 확인합니다.

## 서비스 역할

| 서비스 | 역할 | Host Port |
| --- | --- | ---: |
| Ollama | Llama 로컬 실행 | `11434` |
| PostgreSQL/pgvector | RAG, 장기 Memory, 실행 이력 | `5433` |
| Redis | 단기 상태, Cache, TTL | `6379` |

## 진행 순서

1. [Docker 상태 확인](./01_docker-health-check.md)
2. [Ollama/Llama 실행](./02_ollama-llama.md)
3. [PostgreSQL/pgvector 실행](./03_postgresql-pgvector.md)
4. [Redis 실행](./04_redis.md)
5. `05_environment_diagnostics.py` 실행

## 빠른 실행

PowerShell에서 다음 스크립트를 실행합니다.

```powershell
.\00_local-runtime\scripts\start-local-services.ps1
```

모델 다운로드:

```powershell
docker exec -it aidevs-ollama ollama pull llama3.2
```

연결 점검:

```powershell
python .\00_local-runtime\05_environment_diagnostics.py
```

## 종료

```powershell
.\00_local-runtime\scripts\stop-local-services.ps1
```

종료는 컨테이너와 데이터를 삭제하지 않습니다. 컨테이너·Volume 삭제는 실습 데이터가 사라지는 작업이므로 학생이 대상을 확인한 뒤 별도로 수행합니다.

## 05와 07의 경계

`05`에서는 각각의 인프라 도구를 `docker run`으로 실행합니다. Dockerfile, Docker Compose, 배포와 운영 자동화는 `07`에서 다룹니다.
