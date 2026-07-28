from shared.contracts import TaskRecord
from shared.orchestrator import run_moving_orchestration


if __name__ == "__main__":
    task = TaskRecord(
        user_id="demo-user",
        message="짐 목록과 비용, 주소 변경 목록을 만들어 주세요.",
        result={"context": {"box_count": 24, "distance_km": 15, "budget": 900_000}},
    )
    print(run_moving_orchestration(task).model_dump_json(indent=2))

