ALLOWED_TRANSITIONS = {
    "planned": {"running"},
    "running": {"waiting_input", "completed", "failed"},
    "waiting_input": {"running", "failed"},
    "completed": set(),
    "failed": set(),
}


def transition(current: str, next_status: str) -> str:
    if next_status not in ALLOWED_TRANSITIONS[current]:
        raise ValueError(f"허용되지 않은 전이: {current} -> {next_status}")
    return next_status


print("정상:", transition("planned", "running"))
for current, next_status in [("completed", "running"), ("failed", "running")]:
    try:
        transition(current, next_status)
    except ValueError as error:
        print("차단:", error)

print("종료 상태에서는 LLM이 다시 Agent를 선택해도 실행하지 않습니다.")
