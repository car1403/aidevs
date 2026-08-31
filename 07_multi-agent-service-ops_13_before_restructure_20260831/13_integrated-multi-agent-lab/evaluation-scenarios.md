# 통합 평가 시나리오

| ID | 입력·조건 | 기대 상태 | 확인 |
| --- | --- | --- | --- |
| M01 | 짐·거리·예산이 있는 요청 | `completed` | Packing→Handoff→Budget→Validation |
| M02 | 필요한 정보가 없는 요청 | `waiting_input` | 질문과 허용 Context 필드 |
| M03 | 경고가 발생하는 낮은 예산 | `waiting_approval` | 승인 전 변경 실행 차단 |
| M04 | 승인 대기 Task 승인·거절 | `completed` 또는 `cancelled` | PostgreSQL 결정 이벤트 |
| M05 | 실제 Provider 설정 오류 | `failed` | 오류를 Mock 성공으로 숨기지 않음 |
| M06 | 동일 Idempotency Key 재접수 | 기존 `task_id` | Queue 중복 방지 |
| M07 | Handoff 필드 누락 | 계약 오류 | 다음 Worker 실행 차단 |
| M08 | 허용되지 않은 Tool | `blocked` | allowlist 차단 |
| M09 | `max_steps=1` | `failed` | 무한 실행 방지 |
| M10 | 완료 Task의 Redis·PostgreSQL 조회 | 동일 최종 상태 | 현재 상태와 이벤트 이력 구분 |

평가에서는 LLM 문장 전체를 비교하지 않습니다. Route·Schema·상태·Agent 순서·
Tool 권한·종료 조건을 확인합니다.

