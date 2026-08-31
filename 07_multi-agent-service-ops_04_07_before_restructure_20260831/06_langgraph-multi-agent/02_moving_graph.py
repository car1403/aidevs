from typing import Any, TypedDict

from langgraph.graph import END, START, StateGraph

from shared.moving_agents import budget_agent, packing_agent, validation_agent


class MovingState(TypedDict):
    message: str
    context: dict[str, Any]
    results: dict[str, Any]
    status: str


def packing_node(state: MovingState) -> dict:
    result = packing_agent(state["context"])
    return {
        "context": {**state["context"], **result.data},
        "results": {**state["results"], "packing": result.model_dump()},
    }


def budget_node(state: MovingState) -> dict:
    result = budget_agent(state["context"])
    return {
        "context": {**state["context"], **result.data},
        "results": {**state["results"], "budget": result.model_dump()},
    }


def validation_node(state: MovingState) -> dict:
    result = validation_agent(state["context"])
    return {
        "results": {**state["results"], "validation": result.model_dump()},
        "status": "waiting_approval" if result.warnings else "completed",
    }


builder = StateGraph(MovingState)
builder.add_node("packing_agent", packing_node)
builder.add_node("budget_agent", budget_node)
builder.add_node("validation_agent", validation_node)
builder.add_edge(START, "packing_agent")
builder.add_edge("packing_agent", "budget_agent")
builder.add_edge("budget_agent", "validation_agent")
builder.add_edge("validation_agent", END)
graph = builder.compile()


if __name__ == "__main__":
    initial: MovingState = {
        "message": "짐 목록과 비용",
        "context": {"box_count": 20, "budget": 800_000},
        "results": {},
        "status": "running",
    }
    print(graph.invoke(initial, config={"recursion_limit": 8}))

