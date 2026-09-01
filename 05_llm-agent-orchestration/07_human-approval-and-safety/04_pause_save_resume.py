"""일반 Python State로 Agent 실행의 중단, 저장과 재개를 구분합니다.

변경 직전의 실행 위치와 승인 대상을 State로 반환하고, 이후 구조화된 Command를 받아
같은 실행을 재개합니다. 실제 영구 저장소 없이 pause/resume에 필요한 최소 State 계약을
학습하기 위한 결정적 예제입니다.
"""


ALLOWED_DECISIONS = {"approve", "reject"}


def pause(run_id: str, owner_id: str, draft: dict) -> dict:
    """변경 직전의 실행 정보를 승인 대기 State로 만듭니다.

    Args:
        run_id: 중단과 재개를 연결하는 실행 식별자입니다.
        owner_id: 승인할 수 있는 실행 소유자입니다.
        draft: 승인 화면에 표시하고 이후 다시 검증할 변경 초안입니다.

    Returns:
        현재 Node, 소유자, 초안과 ``waiting_approval`` 상태를 담은 dict입니다.
    """
    return {
        "run_id": run_id,
        "owner_id": owner_id,
        "status": "waiting_approval",
        "current_node": "approval",
        "draft": draft,
    }


def resume(saved_state: dict, command: dict) -> dict:
    """저장된 승인 대기 State를 구조화된 사용자 결정으로 재개합니다.

    승인 대기 상태, 허용된 decision과 실행 소유자를 다시 검사합니다. 검증을 통과하면
    ``completed`` 또는 ``rejected``로 이동하며, 이 함수 자체는 외부 변경을 실행하지
    않고 상태 전이만 보여줍니다.
    """
    if saved_state["status"] != "waiting_approval":
        raise ValueError("승인 대기 상태만 재개할 수 있습니다.")
    if command.get("decision") not in ALLOWED_DECISIONS:
        raise ValueError("decision은 approve 또는 reject여야 합니다.")
    if command.get("actor") != saved_state["owner_id"]:
        raise ValueError("실행 소유자만 결정할 수 있습니다.")
    approved = command["decision"] == "approve"
    return {
        **saved_state,
        "status": "completed" if approved else "rejected",
        "current_node": "end",
        "decision": command["decision"],
        "decision_actor": command["actor"],
    }


if __name__ == "__main__":
    saved = pause("run-001", "user-a", {"action": "create_mock_reservation"})
    print("저장된 상태:", saved)
    print("승인 재개:", resume(saved, {"decision": "approve", "actor": "user-a"}))
    print("거절 재개:", resume(saved, {"decision": "reject", "actor": "user-a"}))
