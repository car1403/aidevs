"""승인 후 Mock 변경 작업을 run_id별로 한 번만 실행합니다.

메모리 set은 멱등성 개념을 관찰하기 위한 결정적 예제일 뿐 영구 저장소가 아닙니다.
프로세스 중단과 동시 실행을 다루는 DB Transaction은 운영 확장 주제로 남깁니다.
"""


PROCESSED_RUNS: set[str] = set()
AUDIT_LOG: list[dict] = []


def execute_once(run_id: str, owner_id: str, decision: dict) -> dict:
    """승인된 Mock 변경을 동일 run_id에서 한 번만 실행합니다.

    Args:
        run_id: 중복 실행 여부를 판정하는 교육용 Idempotency Key입니다.
        owner_id: 변경 실행의 소유자입니다.
        decision: 구조화된 decision과 actor를 포함한 승인 결과입니다.

    Returns:
        소유권·승인 실패, 이미 처리됨 또는 완료 상태를 반환합니다. 메모리 set과
        Audit Log는 개념 확인용이며 프로세스 재시작과 동시 Transaction을 보장하지 않습니다.
    """
    if decision.get("actor") != owner_id:
        return {"status": "blocked", "reason": "실행 소유자가 아님"}
    if decision.get("decision") != "approve":
        return {"status": "rejected", "reason": "승인되지 않음"}
    if run_id in PROCESSED_RUNS:
        return {"status": "already_processed", "run_id": run_id}

    # 학습용 Mock에서는 처리 표시 후 실패가 없다고 가정합니다.
    PROCESSED_RUNS.add(run_id)
    event = {"run_id": run_id, "actor": decision["actor"], "action": "create_mock_reservation"}
    AUDIT_LOG.append(event)
    return {"status": "completed", "event": event}


if __name__ == "__main__":
    approved = {"decision": "approve", "actor": "user-a"}
    print("첫 실행:", execute_once("run-001", "user-a", approved))
    print("중복 실행:", execute_once("run-001", "user-a", approved))
    print("다른 사용자:", execute_once("run-002", "user-a", {"decision": "approve", "actor": "user-b"}))
    print("감사 로그:", AUDIT_LOG)
