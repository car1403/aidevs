"""State, Node, Conditional Edge 최소 예제."""

from typing import Literal, TypedDict
from langgraph.graph import END, START, StateGraph


class State(TypedDict):
    message: str
    intent: str
    answer: str


def classify(state: State) -> dict:
    intent = "weather" if "날씨" in state["message"] else "general"
    return {"intent": intent}


def route(state: State) -> Literal["weather", "general"]:
    return "weather" if state["intent"] == "weather" else "general"


def weather_answer(_: State) -> dict:
    return {"answer": "교육용 Mock 날씨는 맑음입니다."}


def general_answer(_: State) -> dict:
    return {"answer": "일반 문의로 처리했습니다."}


builder = StateGraph(State)
builder.add_node("classify", classify)
builder.add_node("weather", weather_answer)
builder.add_node("general", general_answer)
builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", route)
builder.add_edge("weather", END)
builder.add_edge("general", END)
graph = builder.compile()


if __name__ == "__main__":
    print(graph.invoke({"message": "부산 날씨를 알려줘.", "intent": "", "answer": ""}))
