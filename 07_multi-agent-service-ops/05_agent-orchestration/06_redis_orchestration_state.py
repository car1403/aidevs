"""Agent 한 단계가 끝날 때마다 실제 Redis 상태를 갱신합니다."""

from uuid import uuid4

from shared.learning_storage import RedisLearningStore


def run(agents: list[str], store: RedisLearningStore | None = None) -> dict:
    storage = store or RedisLearningStore()
    run_id = f"orchestration-{uuid4().hex[:8]}"
    state = {"status": "running", "completed": [], "remaining": agents, "trace": []}
    storage.save(run_id, "05_orchestration", state)

    for step, agent in enumerate(agents, start=1):
        state["completed"].append(agent)
        state["remaining"] = agents[step:]
        state["trace"].append({"step": step, "agent": agent, "status": "completed"})
        state["status"] = "completed" if not state["remaining"] else "running"
        storage.save(run_id, "05_orchestration", state)

    return {
        "run_id": run_id,
        "redis_connected": storage.ping(),
        "restored_state": storage.load(run_id, "05_orchestration"),
    }


if __name__ == "__main__":
    print(run(["packing_agent", "budget_agent", "summary_agent"]))
