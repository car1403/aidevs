def next_screen_state(current: dict, event: str, payload: dict | None = None) -> dict:
    state = dict(current)
    if event == "task_created":
        state.update({"task_id": payload["task_id"], "task_snapshot": payload})
    elif event == "task_refreshed":
        state["task_snapshot"] = payload
    elif event == "task_cleared":
        state.update({"task_id": "", "task_snapshot": None})
    return state


if __name__ == "__main__":
    initial = {"task_id": "", "task_snapshot": None}
    print(next_screen_state(initial, "task_created", {"task_id": "task-01", "status": "queued"}))
