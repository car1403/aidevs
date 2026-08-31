"""잘못된 Trace에서 기대 경계를 처음 위반한 단계를 찾습니다."""

bad_trace = [
    {"step": 1, "stage": "read_tool_executed", "tool": "search_product"},
    {"step": 2, "stage": "read_tool_executed", "tool": "check_inventory"},
    {"step": 3, "stage": "approved_change_executed", "tool": "place_order"},
    {"step": 4, "stage": "paused_for_approval", "tool": "place_order"},
]

approval_seen = False
first_failure = None
for event in bad_trace:
    if event["stage"] == "paused_for_approval":
        approval_seen = True
    if event["stage"] == "approved_change_executed" and not approval_seen:
        first_failure = {
            "event": event,
            "reason": "place_order가 승인 대기보다 먼저 실행됐습니다.",
        }
        break

print("최초 실패:", first_failure)
