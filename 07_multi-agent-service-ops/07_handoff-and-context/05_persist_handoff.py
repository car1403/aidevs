r"""Handoff 현재 상태는 Redis, 감사 이벤트는 PostgreSQL에 저장합니다.

Mini Backend를 실행하지 않습니다. 과정 루트 .env의 REDIS_URL과 DATABASE_URL로
두 저장소에 직접 연결합니다.
"""

from uuid import uuid4

from shared.learning_storage import PostgresLearningHistory, RedisLearningStore


def run(
    redis_store: RedisLearningStore | None = None,
    history: PostgresLearningHistory | None = None,
) -> dict:
    live = redis_store or RedisLearningStore()
    permanent = history or PostgresLearningHistory()
    run_id = f"handoff-{uuid4().hex[:8]}"
    handoff = {
        "from_agent": "packing_agent",
        "to_agent": "budget_agent",
        "status": "accepted",
        "context": {"estimated_volume_m3": 12.5, "distance_km": 15},
    }
    redis_state = live.save(run_id, "07_handoff", handoff)
    event = permanent.append_event(
        run_id,
        "07_handoff",
        "agent_handoff",
        "packing_agent",
        handoff,
    )
    return {"run_id": run_id, "redis_state": redis_state, "postgres_event": event}


if __name__ == "__main__":
    print(run())
