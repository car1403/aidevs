# 04 Workflow Patterns

## 학습 목표

- 순차·병렬 실행을 의존성으로 구분합니다.
- 병렬 Worker의 부분 실패를 기록합니다.
- 독립 작업을 병렬 실행한 뒤 Join 단계에서 결과를 합칩니다.
- 실제 Redis에 Workflow 상태를 저장하고 다시 읽습니다.

## 실행

```powershell
python .\04_workflow-patterns\01_sequential_example.py
python .\04_workflow-patterns\02_parallel_example.py
python .\04_workflow-patterns\03_partial_failure.py
python .\04_workflow-patterns\04_parallel_then_join.py
python .\04_workflow-patterns\05_redis_workflow_state.py
```

Packing 결과가 필요한 Budget은 순차 실행합니다. Address와 Cleaning처럼 입력이
독립적인 작업만 병렬 실행합니다.

`03`은 Cleaning 실패와 Address 성공을 함께 보존합니다. `04`는 두 병렬 결과가
모두 준비된 뒤에만 Summary를 실행하는 `fan-out → join` 흐름입니다.

`05`는 `REDIS_URL`에 연결해 실행 상태를 JSON으로 저장한 뒤 같은 Key에서 다시
읽습니다. Upstash Redis URL 또는 강사가 준비한 로컬 Redis URL을 사용할 수 있습니다.
Docker Compose 파일 작성은 이 단원에서 다루지 않습니다.

## 완료 체크

- 병렬 실행 가능한 이유를 설명합니다.
- 부분 실패 시 성공 결과를 버리지 않습니다.
- Join 단계가 필요한 이유를 설명합니다.
- Redis Key와 TTL이 Workflow 상태에 적합한 이유를 설명합니다.

