ALLOWED = {
    "queued": {"running", "cancelled"},
    "running": {"waiting_input", "waiting_approval", "completed", "failed"},
    "waiting_input": {"queued", "cancelled"},
    "waiting_approval": {"completed", "cancelled"},
}


def transition(current: str, target: str) -> str:
    if target not in ALLOWED.get(current, set()):
        raise ValueError(f"허용되지 않은 Task 상태 전이: {current} → {target}")
    return target


if __name__ == "__main__":
    status = transition("queued", "running")
    status = transition(status, "completed")
    print(status)
