"""Multi-Tool Agent가 조회 후 사용자 승인을 받아 변경 Tool을 한 번 실행합니다.

`choose_next_action`은 학습용 규칙입니다. 실제 AI Agent에서는 Model Tool Calling으로
교체할 수 있지만 Tool 정책, 소유권, 승인과 중복 실행 검사는 그대로 유지합니다.
"""

from dataclasses import dataclass, field
from typing import Any, Literal


Status = Literal["running", "waiting_approval", "completed", "rejected", "blocked"]


@dataclass
class AgentState:
    run_id: str
    owner_id: str
    city: str
    weather: dict[str, Any] | None = None
    places: list[str] = field(default_factory=list)
    draft: dict[str, Any] | None = None
    status: Status = "running"
    trace: list[dict[str, Any]] = field(default_factory=list)


WEATHER = {"제주": {"condition": "비", "temperature_c": 21}}
PLACES = {"제주": ["비자림", "제주현대미술관"]}
PROCESSED_RUNS: set[str] = set()
AUDIT_LOG: list[dict[str, Any]] = []


def get_weather(city: str) -> dict[str, Any]:
    return {"city": city, **WEATHER.get(city, {"condition": "정보 없음"})}


def search_places(city: str) -> list[str]:
    return PLACES.get(city, [])


def save_itinerary(owner_id: str, draft: dict[str, Any]) -> dict[str, Any]:
    return {"owner_id": owner_id, "saved": True, "itinerary": draft}


TOOL_POLICIES = {
    "get_weather": "read",
    "search_places": "read",
    "create_draft": "draft",
    "save_itinerary": "change",
    "make_payment": "forbidden",
}


def choose_next_action(state: AgentState) -> str:
    if state.weather is None:
        return "get_weather"
    if not state.places:
        return "search_places"
    if state.draft is None:
        return "create_draft"
    return "request_approval"


def run_until_pause(state: AgentState, max_steps: int = 5) -> dict[str, Any]:
    """읽기 Tool과 초안을 실행하고 변경 직전에 중단합니다."""
    for step in range(1, max_steps + 1):
        action = choose_next_action(state)
        risk = "control" if action == "request_approval" else TOOL_POLICIES.get(action, "unknown")
        state.trace.append({"step": step, "stage": "decision", "action": action, "risk": risk})

        if action == "get_weather":
            state.weather = get_weather(state.city)
        elif action == "search_places":
            state.places = search_places(state.city)
        elif action == "create_draft":
            state.draft = {
                "city": state.city,
                "place": state.places[0],
                "weather": state.weather["condition"],
            }
        elif action == "request_approval":
            state.status = "waiting_approval"
            return {
                "status": state.status,
                "question": "이 여행 일정을 저장할까요?",
                "approval_target": state.draft,
                "allowed_decisions": ["approve", "reject"],
                "trace": state.trace.copy(),
            }
        else:
            state.status = "blocked"
            return {"status": state.status, "reason": "UNKNOWN_ACTION", "trace": state.trace.copy()}

    state.status = "blocked"
    return {"status": state.status, "reason": "MAX_STEPS_EXCEEDED", "trace": state.trace.copy()}


def resume_after_approval(state: AgentState, decision: dict[str, Any]) -> dict[str, Any]:
    """승인자와 승인 대상을 재검사한 뒤 변경 Tool을 한 번만 실행합니다."""
    if state.run_id in PROCESSED_RUNS:
        return {"status": "completed", "reason": "ALREADY_PROCESSED", "trace": state.trace.copy()}
    if state.status != "waiting_approval":
        return {"status": "blocked", "reason": "NOT_WAITING_APPROVAL"}
    if decision.get("actor") != state.owner_id:
        return {"status": "blocked", "reason": "ACTOR_NOT_OWNER"}
    if decision.get("decision") not in {"approve", "reject"}:
        return {"status": "blocked", "reason": "INVALID_DECISION"}
    if decision.get("decision") == "reject":
        state.status = "rejected"
        state.trace.append({"stage": "approval", "decision": "reject", "actor": decision["actor"]})
        return {"status": state.status, "reason": "USER_REJECTED", "trace": state.trace.copy()}
    if decision.get("approval_target") != state.draft:
        return {"status": "blocked", "reason": "APPROVAL_TARGET_CHANGED"}
    # Side Effect는 모든 검사와 승인 뒤에 위치합니다.
    result = save_itinerary(state.owner_id, state.draft or {})
    PROCESSED_RUNS.add(state.run_id)
    event = {
        "run_id": state.run_id,
        "actor": decision["actor"],
        "tool": "save_itinerary",
        "target": state.draft,
    }
    AUDIT_LOG.append(event)
    state.status = "completed"
    state.trace.extend([
        {"stage": "approval", "decision": "approve", "actor": decision["actor"]},
        {"stage": "tool_result", "tool": "save_itinerary", "data": result},
    ])
    return {"status": state.status, "result": result, "audit": event, "trace": state.trace.copy()}


if __name__ == "__main__":
    agent_state = AgentState(run_id="travel-001", owner_id="user-a", city="제주")
    paused = run_until_pause(agent_state)
    print("승인 대기:", paused)

    command = {
        "decision": "approve",
        "actor": "user-a",
        "approval_target": paused["approval_target"],
    }
    print("승인 후 실행:", resume_after_approval(agent_state, command))
    print("중복 재개:", resume_after_approval(agent_state, command))
    print("감사 로그:", AUDIT_LOG)
