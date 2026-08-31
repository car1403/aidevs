"""Task 상태는 아무 값으로나 이동하지 않고 허용된 전이만 사용합니다."""

from shared.contracts import TaskStatus


ALLOWED_TRANSITIONS = {
    TaskStatus.QUEUED: {TaskStatus.RUNNING, TaskStatus.CANCELLED},
    TaskStatus.RUNNING: {
        TaskStatus.WAITING_INPUT,
        TaskStatus.WAITING_APPROVAL,
        TaskStatus.COMPLETED,
        TaskStatus.FAILED,
    },
    TaskStatus.WAITING_INPUT: {TaskStatus.QUEUED, TaskStatus.CANCELLED},
    TaskStatus.WAITING_APPROVAL: {TaskStatus.COMPLETED, TaskStatus.CANCELLED},
}


def transition(current: TaskStatus, target: TaskStatus) -> TaskStatus:
    if target not in ALLOWED_TRANSITIONS.get(current, set()):
        raise ValueError(f"허용되지 않은 상태 전이: {current} -> {target}")
    return target


if __name__ == "__main__":
    print(transition(TaskStatus.QUEUED, TaskStatus.RUNNING))
    try:
        transition(TaskStatus.COMPLETED, TaskStatus.RUNNING)
    except ValueError as exc:
        print("차단:", exc)
