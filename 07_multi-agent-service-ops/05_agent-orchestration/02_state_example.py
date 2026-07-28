from shared.contracts import TaskRecord


state = TaskRecord(
    user_id="demo-user",
    message="짐과 비용을 확인해 주세요.",
)

if __name__ == "__main__":
    print(state.model_dump_json(indent=2))

