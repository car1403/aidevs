"""복구 진행 상태는 Redis, 각 Trace 이벤트는 PostgreSQL에 append합니다."""

from uuid import uuid4

from shared.learning_storage import PostgresLearningHistory, RedisLearningStore


def run(
    redis_store: RedisLearningStore | None = None,
    history: PostgresLearningHistory | None = None,
) -> dict:
    live = redis_store or RedisLearningStore()
    permanent = history or PostgresLearningHistory()
    run_id = f"recovery-{uuid4().hex[:8]}"
    trace = [
        {"attempt": 1, "event": "tool_call", "status": "timeout"},
        {"attempt": 2, "event": "retry", "status": "completed"},
    ]
    stored_events = []
    for item in trace:
        live.save(
            run_id,
            "09_recovery",
            {"status": item["status"], "last_event": item, "trace": trace[: item["attempt"]]},
        )
        stored_events.append(
            permanent.append_event(
                run_id,
                "09_recovery",
                item["event"],
                "quote_agent",
                item,
            )
        )
    return {
        "run_id": run_id,
        "redis_state": live.load(run_id, "09_recovery"),
        "postgres_events": stored_events,
    }


if __name__ == "__main__":
    print(run())
