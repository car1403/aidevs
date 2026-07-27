"""LangGraph interrupt를 사용한 Mock 예약 승인 예제."""

from typing import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command, interrupt


class ApprovalState(TypedDict):
    reservation: dict
    approved: bool
    status: str
    result: str


def prepare(state: ApprovalState) -> dict:
    return {"status": "waiting_approval"}


def request_approval(state: ApprovalState) -> dict:
    decision = interrupt(
        {
            "question": "이 Mock 예약 요청을 승인하시겠습니까?",
            "reservation": state["reservation"],
            "allowed_actions": ["approve", "reject"],
        }
    )
    return {"approved": decision == "approve"}


def execute_mock(state: ApprovalState) -> dict:
    if not state["approved"]:
        return {"status": "rejected", "result": "사용자가 요청을 거절했습니다."}
    return {"status": "completed", "result": "Mock 예약 요청이 기록되었습니다."}


builder = StateGraph(ApprovalState)
builder.add_node("prepare", prepare)
builder.add_node("request_approval", request_approval)
builder.add_node("execute_mock", execute_mock)
builder.add_edge(START, "prepare")
builder.add_edge("prepare", "request_approval")
builder.add_edge("request_approval", "execute_mock")
builder.add_edge("execute_mock", END)
graph = builder.compile(checkpointer=InMemorySaver())


if __name__ == "__main__":
    config = {"configurable": {"thread_id": "approval-demo-001"}}
    initial: ApprovalState = {
        "reservation": {
            "hotel": "바다 호텔",
            "check_in": "2026-08-10",
            "check_out": "2026-08-12",
            "guests": 2,
        },
        "approved": False,
        "status": "started",
        "result": "",
    }
    paused = graph.invoke(initial, config=config)
    print("중단 결과:", paused)
    resumed = graph.invoke(Command(resume="approve"), config=config)
    print("재개 결과:", resumed)
