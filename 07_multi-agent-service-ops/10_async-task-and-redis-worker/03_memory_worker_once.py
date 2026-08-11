from queue import Empty, Queue


def run_worker_once(queue: Queue, tasks: dict) -> dict | None:
    try:
        task_id = queue.get_nowait()
    except Empty:
        return None
    task = tasks[task_id]
    task["status"] = "running"
    task["trace"].append({"event": "worker_started"})
    task["status"] = "completed"
    task["trace"].append({"event": "worker_completed"})
    queue.task_done()
    return task


if __name__ == "__main__":
    memory_queue = Queue()
    memory_tasks = {"task-01": {"task_id": "task-01", "status": "queued", "trace": []}}
    memory_queue.put("task-01")
    print(run_worker_once(memory_queue, memory_tasks))
