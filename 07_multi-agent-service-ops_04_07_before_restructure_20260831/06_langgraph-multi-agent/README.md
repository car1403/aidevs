# 06 LangGraph Multi-Agent

## 학습 목표

- Python Orchestrator를 `StateGraph`로 변환합니다.
- Supervisor·Worker·Conditional Edge를 구분합니다.
- Graph에 명시적인 종료 조건을 둡니다.
- Worker 실행 후 Supervisor로 돌아오는 Multi-Agent loop를 구현합니다.
- 실행 중 상태와 완료 이력을 Redis와 PostgreSQL에 나누어 저장합니다.

## 실행

```powershell
python .\06_langgraph-multi-agent\01_concept_graph.py
python .\06_langgraph-multi-agent\02_moving_graph.py
python .\06_langgraph-multi-agent\03_supervisor_worker_graph.py
python .\06_langgraph-multi-agent\04_python_vs_langgraph.py
python .\06_langgraph-multi-agent\05_redis_postgres_run.py
```

```text
START → route → packing → budget → validate
                                   ├─ complete → END
                                   └─ approval → END
```

LangGraph는 Orchestration의 구현 도구입니다. 역할·계약·실행 계획·종료 조건은
Graph를 만들기 전에 먼저 설계합니다.

`03`은 `Supervisor → Worker → Supervisor` loop에서 남은 Agent와 `max_steps`를
확인합니다. `04`는 일반 Python과 LangGraph가 같은 Agent 순서와 결과 계약을
유지해야 한다는 점을 비교합니다.

`05`는 실행 전·후 상태를 Redis에 저장하고 완료된 Graph 결과를 PostgreSQL의
`learning_runs`에 저장합니다. Redis는 빠른 현재 상태와 TTL에, PostgreSQL은 조회와
감사가 필요한 영구 이력에 사용합니다. Supabase PostgreSQL을 사용하는 경우
`00_local-runtime/init.sql`의 `learning_runs` 생성문을 SQL Editor에서 먼저 실행합니다.

## 완료 체크

- 각 Node의 한 가지 책임을 설명합니다.
- 종료 Edge와 최대 실행 제한의 필요성을 설명합니다.
- Graph를 쓰지 않아도 되는 단순 흐름을 구분합니다.
- Redis 상태와 PostgreSQL 이력의 수명 차이를 설명합니다.

