# 10 Async Task and Redis Worker

## 학습 목표

- 요청 접수와 긴 Agent 실행을 분리합니다.
- Redis List Queue와 Task 상태를 확인합니다.
- idempotency key와 TTL을 설명합니다.

## 구조

```text
Backend RPUSH
→ Redis Queue
→ Worker BLPOP
→ Orchestrator
→ Redis Task 갱신
```

## 실행

```powershell
$env:PYTHONPATH='C:\aidevs\07_multi-agent-service-ops'
python .\10_async-task-and-redis-worker\01_memory_queue.py
python .\10_async-task-and-redis-worker\worker.py
```

`worker.py`는 Redis가 필요하며 Ctrl+C로 종료합니다. 연결 실패를 Mock 성공으로
숨기지 않습니다.

## 완료 체크

- Backend와 Worker의 책임을 설명합니다.
- queued·running·waiting_approval·completed 상태를 구분합니다.

