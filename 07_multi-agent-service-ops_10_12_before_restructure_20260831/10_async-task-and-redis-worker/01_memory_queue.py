from queue import Queue

from shared.contracts import TaskRecord
from shared.orchestrator import run_moving_orchestration


queue: Queue[TaskRecord] = Queue()
queue.put(TaskRecord(user_id="demo-user", message="짐과 비용을 알려 주세요."))

if __name__ == "__main__":
    task = queue.get()
    result = run_moving_orchestration(task)
    queue.task_done()
    print(result.model_dump_json(indent=2))

