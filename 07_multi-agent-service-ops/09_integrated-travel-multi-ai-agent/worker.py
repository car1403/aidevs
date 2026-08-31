from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path


COURSE_ROOT = Path(__file__).resolve().parents[1]
SERVICE_ROOT = COURSE_ROOT / "08_multi-ai-agent-service"
sys.path.insert(0, str(SERVICE_ROOT))

from app.repositories import PostgresHistory, RedisTasks  # noqa: E402
from integrated_orchestrator import run_integrated  # noqa: E402


def process_one(tasks: RedisTasks, history: PostgresHistory, timeout: int = 5):
    task_id = tasks.dequeue(timeout=timeout)
    if task_id is None:
        return None
    task = tasks.get(task_id)
    if task is None or task.status != "queued":
        return None
    try:
        task = asyncio.run(run_integrated(task))
    except Exception as error:
        task.status = "failed"
        task.error = f"{type(error).__name__}: {error}"
        task.trace.append(
            {
                "actor": "integrated_worker",
                "action": "orchestrate",
                "status": "failed",
                "error_type": type(error).__name__,
                "error": str(error),
            }
        )
    tasks.save(task)
    history.save(task)
    return task


def main() -> None:
    tasks = RedisTasks()
    history = PostgresHistory()
    tasks.ping()
    history.ping()
    print("Integrated Worker가 Redis Queue를 기다립니다. 종료: Ctrl+C")
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
