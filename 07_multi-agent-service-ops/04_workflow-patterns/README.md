# 04 Workflow Patterns

## 학습 목표

- 순차·병렬 실행을 의존성으로 구분합니다.
- 병렬 Worker의 부분 실패를 기록합니다.

## 실행

```powershell
python .\04_workflow-patterns\01_sequential_example.py
python .\04_workflow-patterns\02_parallel_example.py
```

Packing 결과가 필요한 Budget은 순차 실행합니다. Address와 Cleaning처럼 입력이
독립적인 작업만 병렬 실행합니다.

## 완료 체크

- 병렬 실행 가능한 이유를 설명합니다.
- 부분 실패 시 성공 결과를 버리지 않습니다.

