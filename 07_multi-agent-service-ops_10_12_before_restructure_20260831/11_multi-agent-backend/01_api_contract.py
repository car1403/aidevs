def accepted_task(task_id: str) -> dict:
    return {
        "status_code": 202,
        "task_id": task_id,
        "status_url": f"/api/tasks/{task_id}",
        "meaning": "요청을 접수했으며 처리는 아직 끝나지 않았습니다.",
    }


if __name__ == "__main__":
    print(accepted_task("task-01"))
