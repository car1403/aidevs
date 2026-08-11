# 07 Handoff and Context

## 학습 목표

- 함수 호출과 책임 인계인 Handoff를 구분합니다.
- 다음 Agent에 필요한 최소 Context만 전달합니다.
- task ID와 trace ID로 인계 과정을 추적합니다.
- 대상 Agent·사용자·최대 인계 횟수를 검증합니다.
- 현재 Handoff 상태는 Redis에, 수락·차단 감사 이벤트는 PostgreSQL에 저장합니다.

## 실행

```powershell
python .\07_handoff-and-context\01_handoff_example.py
python .\07_handoff-and-context\02_context_filter.py
python .\07_handoff-and-context\03_handoff_contract.py
python .\07_handoff-and-context\04_handoff_guard.py
python .\07_handoff-and-context\05_persist_handoff.py
```

Packing Agent는 Budget Agent에 짐 부피와 큰 가구 목록만 전달합니다. 사용자
메시지 전체와 Secret은 전달하지 않습니다. Handoff는 단순 함수 호출이 아니라
`누가 → 누구에게 → 어떤 책임과 Context를 넘겼는지` 기록하는 계약입니다.

```text
Packing Agent
→ 최소 Context 생성
→ Handoff 계약 검증
→ 사용자·대상·hop_count 확인
→ Budget Agent가 책임 인수
```

`05`는 최소 Context와 현재 인계 상태를 Redis에 저장하고 `agent_handoff` 이벤트를
PostgreSQL `learning_events`에 append합니다. 차단된 인계도 감사 기록에서 삭제하지
않습니다.

## 완료 체크

- Handoff 전후 책임 주체를 설명합니다.
- 불필요한 Context를 제거할 수 있습니다.
- 잘못된 사용자·대상·반복 인계를 차단할 수 있습니다.
- Redis 상태와 PostgreSQL 감사 이벤트의 목적 차이를 설명합니다.

