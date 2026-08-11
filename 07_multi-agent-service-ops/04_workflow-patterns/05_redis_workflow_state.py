"""병렬 Workflow 결과를 실제 Redis에 저장하고 다시 읽습니다."""

from uuid import uuid4

from shared.learning_storage import RedisLearningStore


def run(store: RedisLearningStore | None = None) -> dict:
    storage = store or RedisLearningStore()
    run_id = f"workflow-{uuid4().hex[:8]}"
    state = {
        "status": "completed",
        "completed": {
            "address_agent": {"new_address": "서울시 강남구 학습로 7"},
            "cleaning_agent": {"available_date": "2026-08-20"},
        },
        "failed": {},
    }
    saved = storage.save(run_id, "04_workflow", state)
    loaded = storage.load(run_id, "04_workflow")
    return {"redis_connected": storage.ping(), "saved": saved, "loaded": loaded}


if __name__ == "__main__":
    print(run())
