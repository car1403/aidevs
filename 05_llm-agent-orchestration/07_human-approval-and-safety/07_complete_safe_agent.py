"""Multi-Tool Agent가 조회 후 사용자 승인을 받아 변경 Tool을 한 번 실행합니다.

`choose_next_action`은 학습용 규칙입니다. 실제 AI Agent에서는 Model Tool Calling으로
교체할 수 있지만 Tool 정책, 소유권, 승인과 중복 실행 검사는 그대로 유지합니다.
"""

from dataclasses import dataclass, field
from typing import Any, Literal


Status = Literal["running", "waiting_approval", "completed", "rejected", "blocked"]


@dataclass
class AgentState:
    """승인 전후에 유지되는 Rule-based Agent의 실행 State입니다.

    Goal을 수행하며 얻은 날씨와 장소, 변경 초안, 현재 상태와 Trace를 한 객체에
    보관합니다. ``places=None``과 빈 목록을 구분해 미검색과 검색 결과 없음이 서로
    다른 종료 경로를 갖게 합니다.
    """
    run_id: str
    owner_id: str
    city: str
    weather: dict[str, Any] | None = None
    # None은 아직 검색하지 않음, []는 검색했지만 결과가 없음을 뜻합니다.
    places: list[str] | None = None
    draft: dict[str, Any] | None = None
    status: Status = "running"
    trace: list[dict[str, Any]] = field(default_factory=list)


WEATHER = {"제주": {"condition": "비", "temperature_c": 21}}
PLACES = {"제주": ["비자림", "제주현대미술관"]}
PROCESSED_RUNS: set[str] = set()
AUDIT_LOG: list[dict[str, Any]] = []


def get_weather(city: str) -> dict[str, Any]:
    """도시의 날씨 근거를 반환하는 읽기 전용 학습 Tool입니다."""
    return {"city": city, **WEATHER.get(city, {"condition": "정보 없음"})}


def search_places(city: str) -> list[str]:
    """도시의 장소 후보를 반환하며 외부 상태를 변경하지 않습니다."""
    return PLACES.get(city, [])


def save_itinerary(owner_id: str, draft: dict[str, Any]) -> dict[str, Any]:
    """승인 후에만 호출할 수 있는 Mock 변경 Tool Result를 만듭니다.

    이 함수 자체는 권한을 판단하지 않습니다. 호출 전에 ``resume_after_approval``이
    소유자, 결정값과 승인 Snapshot을 검사해야 합니다.
    """
    return {"owner_id": owner_id, "saved": True, "itinerary": draft}


TOOL_POLICIES = {
    "get_weather": "read",
    "search_places": "read",
    "create_draft": "draft",
    "save_itinerary": "change",
    "make_payment": "forbidden",
}


def choose_next_action(state: AgentState) -> str:
    """현재 State에서 필요한 다음 읽기, 초안, 중단 또는 종료 행동을 선택합니다.

    실제 AI Agent에서는 이 역할을 Model Tool Calling이 수행할 수 있습니다. 여기서는
    안전 정책과 상태 전이를 결정적으로 관찰하기 위해 명시적인 규칙을 사용합니다.
    """
    if state.weather is None:
        return "get_weather"
    if state.places is None:
        return "search_places"
    if not state.places:
        return "stop_no_places"
    if state.draft is None:
        return "create_draft"
    return "request_approval"


def run_until_pause(state: AgentState, max_steps: int = 5) -> dict[str, Any]:
    """읽기 Tool과 초안을 실행하고 변경 직전에 안전하게 중단합니다.

    각 단계에서 다음 행동과 위험도를 Trace에 기록합니다. 날씨와 장소를 조회하고
    초안을 만든 뒤 ``waiting_approval``을 반환하며, 장소 없음·알 수 없는 Action·최대
    단계 초과는 변경 Tool을 실행하지 않고 ``blocked``로 종료합니다.
    """
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
        elif action == "stop_no_places":
            state.status = "blocked"
            return {"status": state.status, "reason": "NO_PLACES_FOUND", "trace": state.trace.copy()}
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
    """승인자와 승인 대상을 재검사한 뒤 변경 Tool을 한 번만 실행합니다.

    Args:
        state: ``run_until_pause``가 남긴 승인 대기 State입니다.
        decision: decision, actor와 approval_target을 담은 비신뢰 사용자 입력입니다.

    Returns:
        승인, 거절, 차단 또는 이미 처리된 상태를 반환합니다. 실제 Side Effect는 상태,
        소유권, 결정값과 Snapshot 검사가 모두 성공한 뒤에만 실행하고 Audit에 기록합니다.
    """
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
