"""Supervisor가 남은 Agent를 선택하고 Worker가 다시 Supervisor로 돌아오는 Graph."""

from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from shared.moving_agents import address_agent, budget_agent, packing_agent


class MultiAgentState(TypedDict):
    context: dict[str, Any]
    remaining_agents: list[str]
    current_agent: str
    results: dict[str, Any]
    step_count: int
    max_steps: int
    status: str


def supervisor(state: MultiAgentState) -> dict:
    if state["step_count"] >= state["max_steps"]:
        return {"status": "failed", "current_agent": ""}
    if not state["remaining_agents"]:
        return {"status": "completed", "current_agent": ""}
    return {"status": "running", "current_agent": state["remaining_agents"][0]}


def worker(state: MultiAgentState) -> dict:
    name = state["current_agent"]
    functions = {
        "packing_agent": packing_agent,
        "budget_agent": budget_agent,
        "address_agent": address_agent,
    }
    result = functions[name](state["context"])
    return {
        "context": {**state["context"], **result.data},
        "remaining_agents": state["remaining_agents"][1:],
        "results": {**state["results"], name: result.model_dump()},
        "step_count": state["step_count"] + 1,
    }


def next_after_supervisor(state: MultiAgentState) -> str:
    return "worker" if state["status"] == "running" else "end"


builder = StateGraph(MultiAgentState)
builder.add_node("supervisor", supervisor)
builder.add_node("worker", worker)
builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", next_after_supervisor, {"worker": "worker", "end": END})
builder.add_edge("worker", "supervisor")
graph = builder.compile()


if __name__ == "__main__":
    initial: MultiAgentState = {
        "context": {"box_count": 15, "distance_km": 10},
        "remaining_agents": ["packing_agent", "budget_agent", "address_agent"],
        "current_agent": "",
        "results": {},
        "step_count": 0,
        "max_steps": 5,
        "status": "queued",
    }
    print(graph.invoke(initial, config={"recursion_limit": 12}))
