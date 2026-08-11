"""LangGraph 실행 중 상태는 Redis, 완료 이력은 PostgreSQL에 저장합니다."""

from uuid import uuid4
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from shared.learning_storage import PostgresLearningHistory, RedisLearningStore


class State(TypedDict):
    remaining: list[str]
    completed: list[str]
    status: str


def work(state: State) -> dict:
    current = state["remaining"][0]
    return {
        "remaining": state["remaining"][1:],
        "completed": [*state["completed"], current],
        "status": "completed" if len(state["remaining"]) == 1 else "running",
    }


builder = StateGraph(State)
builder.add_node("work", work)
builder.add_edge(START, "work")
builder.add_conditional_edges("work", lambda state: "end" if not state["remaining"] else "work", {"work": "work", "end": END})
graph = builder.compile()


def run(
    redis_store: RedisLearningStore | None = None,
    history: PostgresLearningHistory | None = None,
) -> dict:
    live = redis_store or RedisLearningStore()
    permanent = history or PostgresLearningHistory()
    run_id = f"graph-{uuid4().hex[:8]}"
    initial: State = {
        "remaining": ["packing_agent", "budget_agent", "address_agent"],
        "completed": [],
        "status": "running",
    }
    live.save(run_id, "06_langgraph", initial)
    result = graph.invoke(initial, config={"recursion_limit": 10})
    live.save(run_id, "06_langgraph", result)
    history_record = permanent.save(run_id, "06_langgraph", result["status"], initial, result)
    return {
        "run_id": run_id,
        "redis_state": live.load(run_id, "06_langgraph"),
        "postgres_history": history_record,
    }


if __name__ == "__main__":
    print(run())
