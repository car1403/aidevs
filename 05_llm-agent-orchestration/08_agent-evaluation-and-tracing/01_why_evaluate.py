"""프로그램 실행 성공과 Agent 행동의 올바름은 다릅니다."""

actual = {
    "status": "completed",
    "trace": [
        {"stage": "approved_change_executed", "tool": "place_order"},
    ],
}

changed_without_approval = any(
    event.get("stage") == "approved_change_executed" and event.get("tool") == "place_order"
    for event in actual["trace"]
)

print("프로그램은 오류 없이 끝났는가?", actual["status"] == "completed")
print("승인 대기 없이 주문을 실행했는가?", changed_without_approval)
print("결론: 실행 성공만으로 안전하고 올바른 Agent라고 판단할 수 없습니다.")
