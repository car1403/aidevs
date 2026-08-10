"""정보 부족과 예산 검증을 포함한 여행 LangGraph 예제."""

from typing import Literal, TypedDict
from langgraph.graph import END, START, StateGraph


class TravelState(TypedDict):
    destination: str
    nights: int
    budget: int
    missing_fields: list[str]
    draft_plan: dict
    validation_errors: list[str]
    iteration: int
    max_iterations: int
    status: str
    final_answer: str


def inspect_request(state: TravelState) -> dict:
    missing = []
    if not state.get("destination"):
        missing.append("destination")
    if state.get("nights", 0) < 1:
        missing.append("nights")
    if state.get("budget", 0) <= 0:
        missing.append("budget")
    return {"missing_fields": missing}


def after_inspection(state: TravelState) -> Literal["ask_user", "create_plan"]:
    return "ask_user" if state["missing_fields"] else "create_plan"


def ask_user(state: TravelState) -> dict:
    return {
        "status": "needs_input",
        "final_answer": f"다음 정보를 알려주세요: {', '.join(state['missing_fields'])}",
    }


def create_plan(state: TravelState) -> dict:
    daily_budget = 170000 if state["iteration"] == 0 else 110000
    total = daily_budget * (state["nights"] + 1)
    return {
        "draft_plan": {
            "destination": state["destination"],
            "days": state["nights"] + 1,
            "estimated_budget": total,
        }
    }


def validate_plan(state: TravelState) -> dict:
    errors = []
    if state["draft_plan"]["estimated_budget"] > state["budget"]:
        errors.append("budget_exceeded")
    return {"validation_errors": errors}


def after_validation(state: TravelState) -> Literal["revise", "finish", "fail"]:
    if not state["validation_errors"]:
        return "finish"
    if state["iteration"] < state["max_iterations"]:
        return "revise"
    return "fail"


def revise(state: TravelState) -> dict:
    return {"iteration": state["iteration"] + 1}


def finish(state: TravelState) -> dict:
    return {"status": "waiting_approval", "final_answer": "일정 초안이 준비되었습니다."}


def fail(_: TravelState) -> dict:
    return {"status": "failed", "final_answer": "예산에 맞는 일정을 만들지 못했습니다."}


builder = StateGraph(TravelState)
for name, node in {
    "inspect_request": inspect_request,
    "ask_user": ask_user,
    "create_plan": create_plan,
    "validate_plan": validate_plan,
    "revise": revise,
    "finish": finish,
    "fail": fail,
}.items():
    builder.add_node(name, node)
builder.add_edge(START, "inspect_request")
builder.add_conditional_edges("inspect_request", after_inspection)
builder.add_edge("ask_user", END)
builder.add_edge("create_plan", "validate_plan")
builder.add_conditional_edges("validate_plan", after_validation)
builder.add_edge("revise", "create_plan")
builder.add_edge("finish", END)
builder.add_edge("fail", END)
graph = builder.compile()


if __name__ == "__main__":
    initial: TravelState = {
        "destination": "부산",
        "nights": 2,
        "budget": 400000,
        "missing_fields": [],
        "draft_plan": {},
        "validation_errors": [],
        "iteration": 0,
        "max_iterations": 1,
        "status": "started",
        "final_answer": "",
    }
    print(graph.invoke(initial))
