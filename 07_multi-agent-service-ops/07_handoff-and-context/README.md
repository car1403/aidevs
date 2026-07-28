# 07 Handoff and Context

## 학습 목표

- 함수 호출과 책임 인계인 Handoff를 구분합니다.
- 다음 Agent에 필요한 최소 Context만 전달합니다.
- task ID와 trace ID로 인계 과정을 추적합니다.

## 실행

```powershell
python .\07_handoff-and-context\01_handoff_example.py
python .\07_handoff-and-context\02_context_filter.py
```

Packing Agent는 Budget Agent에 짐 부피와 큰 가구 목록만 전달합니다. 사용자
메시지 전체와 Secret은 전달하지 않습니다.

## 완료 체크

- Handoff 전후 책임 주체를 설명합니다.
- 불필요한 Context를 제거할 수 있습니다.

