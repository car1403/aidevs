"""Rule-based Agent Loop: 개발자 규칙으로 판단·실행·관찰·종료를 반복합니다."""

from typing import Any
from travel_tools import execute_tool

MAX_STEPS = 5


def create_state(city: str) -> dict[str, Any]:
    return {"goal": f"{city} 날씨에 맞는 장소 추천", "city": city, "weather": None, "places": [], "completed_actions": [], "status": "running", "termination_reason": None, "step": 0, "errors": [], "trace": []}


def decide(state: dict[str, Any]) -> dict[str, Any]:
    """실제 Model의 다음 행동 결정을 학습용 규칙으로 모사합니다."""
    if state["weather"] is None:
        return {"action": "get_weather", "reason_code": "WEATHER_REQUIRED"}
    if not state["weather"].get("success"):
        return {"action": "stop", "reason_code": "WEATHER_TOOL_FAILED"}
    if not state["places"]:
        action = "search_indoor_places" if state["weather"]["condition"] == "비" else "search_outdoor_places"
        return {"action": action, "reason_code": "PLACE_SEARCH_REQUIRED"}
    return {"action": "finish", "reason_code": "GOAL_COMPLETED"}


def observe(state: dict[str, Any], action: str, result: dict[str, Any]) -> None:
    if action == "get_weather":
        state["weather"] = result
    elif action in {"search_indoor_places", "search_outdoor_places"}:
        state["places"] = result.get("items", [])
    state["completed_actions"].append(action)
    if not result.get("success"):
        state["errors"].append(result)


def run_agent(city: str) -> dict[str, Any]:
    state = create_state(city)
    for step in range(1, MAX_STEPS + 1):
        state["step"] = step
        decision = decide(state)
        action = decision["action"]
        state["trace"].append({"step": step, "stage": "reason", **decision})
        if action == "finish":
            state["status"] = "completed"
            state["termination_reason"] = "completed"
            return state
        if action == "stop":
            state["status"] = "stopped"
            state["termination_reason"] = decision["reason_code"].lower()
            return state
        result = execute_tool(action, {"city": state["city"]})
        state["trace"].append({"step": step, "stage": "act_and_observe", "tool": action, "result": result})
        observe(state, action, result)
    state["status"] = "stopped"
    state["termination_reason"] = "max_steps_exceeded"
    return state


if __name__ == "__main__":
    result = run_agent("제주")
    print("목표:", result["goal"])
    print("날씨:", result["weather"])
    print("장소:", result["places"])
    print("상태:", result["status"])
    print("종료 이유:", result["termination_reason"])
    print("실행 Trace:")
    for event in result["trace"]:
        print("-", event)
