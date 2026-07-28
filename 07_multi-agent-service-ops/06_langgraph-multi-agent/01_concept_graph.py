from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    message: str
    route: str
    result: str


def route(state: State) -> dict:
    return {"route": "budget" if "비용" in state["message"] else "packing"}


def packing(_: State) -> dict:
    return {"result": "상자 20개가 필요합니다."}


def budget(_: State) -> dict:
    return {"result": "예상 비용은 50만~70만원입니다."}


builder = StateGraph(State)
builder.add_node("route", route)
builder.add_node("packing", packing)
builder.add_node("budget", budget)
builder.add_edge(START, "route")
builder.add_conditional_edges(
    "route",
    lambda state: state["route"],
    {"packing": "packing", "budget": "budget"},
)
builder.add_edge("packing", END)
builder.add_edge("budget", END)
graph = builder.compile()


if __name__ == "__main__":
    print(graph.invoke({"message": "이사 비용", "route": "", "result": ""}))

