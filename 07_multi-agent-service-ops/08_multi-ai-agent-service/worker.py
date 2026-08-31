import time

from app.repositories import PostgresHistory, RedisTasks
from app.service import append_trace, run_multi_agent


def process_one(tasks: RedisTasks, history: PostgresHistory, timeout: int = 5):
    task_id = tasks.dequeue(timeout=timeout)
    if task_id is None:
        return None
    task = tasks.get(task_id)
    if task is None or task.status != "queued":
        return None
    try:
        task = run_multi_agent(task)
    except Exception as error:
        task.status = "failed"
        task.error = f"{type(error).__name__}: {error}"
        append_trace(task, "worker", "orchestrate", "failed", error=task.error)
    tasks.save(task)
    history.save(task)
    return task


def main() -> None:
    tasks = RedisTasks()
    history = PostgresHistory()
    tasks.ping()
    history.ping()
    print("Travel Worker가 Redis Queue를 기다립니다. 종료: Ctrl+C")
    while True:
        task = process_one(tasks, history)
        if task:
            print(task.task_id, task.status)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Worker를 종료합니다.")
    except Exception:
        time.sleep(1)
        raise
