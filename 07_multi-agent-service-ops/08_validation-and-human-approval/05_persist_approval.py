"""승인 대기 상태는 Redis, 사람의 최종 결정은 PostgreSQL에 저장합니다."""

from uuid import uuid4

from shared.learning_storage import PostgresLearningHistory, RedisLearningStore


def run(
    decision: str = "approve",
    redis_store: RedisLearningStore | None = None,
    history: PostgresLearningHistory | None = None,
) -> dict:
    if decision not in {"approve", "edit", "reject"}:
        raise ValueError("decision은 approve, edit, reject 중 하나여야 합니다.")
    live = redis_store or RedisLearningStore()
    permanent = history or PostgresLearningHistory()
    run_id = f"approval-{uuid4().hex[:8]}"
    plan = {"tool": "create_mock_quote", "budget": 700_000}
    pending = live.save(run_id, "08_approval", {"status": "waiting_approval", "plan": plan})
    final_status = {"approve": "approved", "edit": "needs_revision", "reject": "cancelled"}[decision]
    current = live.save(
        run_id,
        "08_approval",
        {"status": final_status, "decision": decision, "plan": plan},
    )
    event = permanent.append_event(
        run_id,
        "08_approval",
        "human_decision",
        "student-01",
        {"decision": decision, "status": final_status, "plan": plan},
    )
    return {"run_id": run_id, "pending": pending, "current": current, "postgres_event": event}


if __name__ == "__main__":
    print(run())
