from typing import TypedDict

from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    trace: list[str]


def research(state: State) -> State:
    return {"trace": state["trace"] + ["weather", "place", "budget"]}


def join(state: State) -> State:
    required = {"weather", "place", "budget"}
    if not required.issubset(state["trace"]):
        raise RuntimeError("전문 Agent 결과가 모두 준비되지 않았습니다.")
    return {"trace": state["trace"] + ["joined"]}


def itinerary(state: State) -> State:
    return {"trace": state["trace"] + ["itinerary"]}


builder = StateGraph(State)
builder.add_node("research", research)
builder.add_node("join", join)
builder.add_node("itinerary", itinerary)
builder.add_edge(START, "research")
builder.add_edge("research", "join")
builder.add_edge("join", "itinerary")
builder.add_edge("itinerary", END)

print(builder.compile().invoke({"trace": []}))
