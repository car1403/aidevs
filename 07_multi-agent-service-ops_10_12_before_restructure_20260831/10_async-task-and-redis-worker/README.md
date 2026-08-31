# 10 Async Task and Redis Worker

## 학습 목표

- 요청 접수와 긴 Agent 실행을 분리합니다.
- Redis List Queue와 Task 상태를 확인합니다.
- idempotency key와 TTL을 설명합니다.
- 실제 LLM Routing 결과와 최종 상태를 PostgreSQL에 저장합니다.

Redis를 설치하기 전에 같은 구조를 Memory Queue로 한 번 완주합니다.

## 구조

```text
Backend RPUSH
→ Redis Queue
→ Worker BLPOP
→ Orchestrator
→ Redis Task 갱신
→ PostgreSQL Task·Handoff·Event 이력
```

## 실행

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
python .\10_async-task-and-redis-worker\01_memory_queue.py
python .\10_async-task-and-redis-worker\02_task_lifecycle.py
python .\10_async-task-and-redis-worker\03_memory_worker_once.py
python .\10_async-task-and-redis-worker\04_idempotency_and_ttl.py
python .\10_async-task-and-redis-worker\05_real_worker_once.py
python .\10_async-task-and-redis-worker\worker.py
```

앞의 네 예제는 Redis가 필요 없습니다. `05`는 Queue의 Task 한 건만 처리해 연결을
빠르게 확인하고, `worker.py`는 계속 대기하는 실제 Worker입니다. 실제 Worker는 Redis와
PostgreSQL 연결을 시작할 때 모두 확인하며 연결 실패를 Mock 성공으로 숨기지 않습니다.

| 저장·Queue | 사용 시점 |
| --- | --- |
| Python Memory | 구조를 처음 배우고 한 Process에서 확인 |
| 로컬 Redis | Backend와 Worker를 별도 Process로 실행 |
| Upstash 등 관리형 Redis | 배포 후 Redis 서버 운영을 줄이고 싶을 때 |

## 완료 체크

- Backend와 Worker의 책임을 설명합니다.
- queued·running·waiting_approval·completed 상태를 구분합니다.
- Memory와 Redis에서 바뀌는 부분이 저장소뿐임을 설명합니다.
- Worker 실패와 PostgreSQL 감사 저장 실패를 Trace에서 구분합니다.

