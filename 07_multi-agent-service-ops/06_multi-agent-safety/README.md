# 06 Multi Agent Safety

앞 과정에서 입력 검증과 사람 승인을 배웠습니다. Multi AI Agent에서는 여기에 한 가지가 더 필요합니다. **다른 Agent가 요청했다는 이유만으로 그 요청을 신뢰하면 안 됩니다.**

## 네 개의 안전 경계

```text
Agent가 Tool 요청
→ 사용자 범위 확인
→ Agent별 Tool allowlist 확인
→ 변경 작업이면 승인과 idempotency key 확인
→ 실제 Tool 실행
```

| 경계 | 막는 문제 |
| --- | --- |
| 사용자 범위 | 다른 사용자의 Task나 승인을 재사용 |
| Agent별 권한 | Weather Agent가 일정 저장·결제 같은 Tool 호출 |
| 사람 승인 | 외부 상태가 승인 전에 변경됨 |
| 멱등성 | 재시도 때문에 같은 저장·예약이 두 번 실행됨 |

LLM은 Tool 호출을 제안할 뿐입니다. 실제 허용 여부는 Python 정책이 결정합니다. 실제 예약과 결제는 이번 과정에서 실행하지 않고, 승인된 일정 저장까지만 예로 듭니다.

## 예제

| 파일 | 핵심 |
| --- | --- |
| `01_agent_tool_permissions.py` | Agent별 최소 권한 |
| `02_approval_boundary.py` | 정확히 일치하는 사용자 승인 |
| `03_idempotent_write.py` | 중복 변경 차단 |
| `04_untrusted_agent_request.py` | Agent 간 요청도 다시 검증 |

```powershell
python .\06_multi-agent-safety\01_agent_tool_permissions.py
python .\06_multi-agent-safety\02_approval_boundary.py
python .\06_multi-agent-safety\03_idempotent_write.py
python .\06_multi-agent-safety\04_untrusted_agent_request.py
```

이 예제들은 정책을 이해하기 위한 결정적 코드라 API Key가 필요하지 않습니다. `03`의 메모리 Registry는 `08`에서 실제 Redis 기반 멱등성 저장으로 교체합니다.

## 승인과 검증의 순서

승인이 있다고 모든 행동을 허용하지 않습니다. 먼저 사용자·Agent 권한·입력 형식을 확인하고, 그 뒤 현재 요청과 정확히 일치하는 승인을 확인합니다. 잘못된 Tool을 사람이 승인했더라도 Agent allowlist를 우회할 수 없습니다.

## 직접 확인하기

1. 읽기 Tool과 변경 Tool의 승인 정책이 달라야 하는 이유를 설명해 보세요.
2. idempotency key를 사용자별로 분리하지 않으면 어떤 문제가 생길까요?
3. Supervisor가 만든 Tool 요청도 Guard를 통과해야 하는 이유를 적어 보세요.
