# 05 Memory

## 학습 목표

- 대화 이력, 단기 Memory, 장기 Memory를 구분합니다.
- 사용자별 기억을 격리합니다.
- 기억을 조회·수정·삭제합니다.
- 저장하면 안 되는 정보를 구분합니다.

## 실행

```powershell
python .\01_concept_example.py
python .\02_travel_example.py
python .\03_redis_session_example.py
python .\04_postgres_memory_example.py
```

## 핵심

Memory는 대화 전체를 무조건 저장하는 기능이 아닙니다. 다음 요청에 필요하고 사용자가 확인·수정·삭제할 수 있는 정보만 저장합니다.

- Redis: 현재 Node, 임시 대화 상태, Cache처럼 만료가 필요한 데이터
- PostgreSQL: 사용자가 관리하는 장기 선호와 Agent 실행 이력
