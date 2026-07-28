# 통합 평가 시나리오

| ID | 입력·조건 | 기대 상태 | 확인 |
| --- | --- | --- | --- |
| M01 | 짐 목록과 비용 | `completed` | Packing→Handoff→Budget |
| M02 | 의미가 불명확한 요청 | 추가 질문 설계 | 안전한 기본 Route |
| M03 | 예산 10만원 | `waiting_approval` | 예산 경고 |
| M04 | Packing 예외 | `failed` 또는 부분 성공 | 실패 Agent 기록 |
| M05 | 견적 timeout | `completed_with_fallback` | fallback 경고 |
| M06 | Handoff 필드 누락 | 계약 오류 | Worker 실행 차단 |
| M07 | Supervisor의 결제 Tool | 권한 오류 | allowlist 차단 |
| M08 | `max_steps=1` | `failed` | 무한 실행 방지 |

평가에서는 LLM 문장 전체를 비교하지 않습니다. Route·Schema·상태·Agent 순서·
Tool 권한·종료 조건을 확인합니다.

