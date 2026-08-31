ALLOWED_TARGETS = {
    "packing_agent": {"budget_agent"},
    "budget_agent": {"summary_agent"},
}


def guard_handoff(handoff: dict, *, active_user_id: str, max_hops: int = 3) -> dict:
    if handoff["user_id"] != active_user_id:
        return {"accepted": False, "reason": "다른 사용자의 Context입니다."}
    if handoff["hop_count"] > max_hops:
        return {"accepted": False, "reason": "최대 Handoff 횟수를 초과했습니다."}
    allowed = ALLOWED_TARGETS.get(handoff["source_agent"], set())
    if handoff["target_agent"] not in allowed:
        return {"accepted": False, "reason": "허용되지 않은 Agent 전달입니다."}
    return {"accepted": True, "reason": "Handoff 계약을 통과했습니다."}


if __name__ == "__main__":
    demo = {
        "user_id": "student-01",
        "source_agent": "packing_agent",
        "target_agent": "budget_agent",
        "hop_count": 1,
    }
    print(guard_handoff(demo, active_user_id="student-01"))
    print(guard_handoff({**demo, "user_id": "other-user"}, active_user_id="student-01"))
