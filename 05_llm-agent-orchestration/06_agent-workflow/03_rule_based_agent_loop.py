"""State를 사용하는 규칙 기반 Agent Loop를 구현합니다.

01과 02에서는 개발자가 작성한 Workflow가 한 방향으로 실행되었습니다. 이번 파일은
목표와 현재 State를 매 단계 다시 확인하며 ``판단(Reason) → 실행(Act) →
관찰(Observe)``을 반복하는 Agent Loop 구조를 처음 도입합니다.

이번 파일에서 하는 일
----------------------
1. ``create_state``가 목표, Tool 결과, 오류, 진행 상태와 trace를 만듭니다.
2. ``decide``가 현재 State를 보고 다음 행동, 완료 또는 중단을 선택합니다.
3. ``execute_tool``이 선택된 행동을 실행합니다.
4. ``observe``가 Tool Result를 State에 반영하여 다음 판단의 근거로 만듭니다.
5. ``run_agent``가 목표 달성, 실패 또는 최대 단계 도달까지 이 과정을 반복합니다.

구조적으로는 Agent Loop이지만 다음 행동을 정하는 주체는 Python if 문입니다. LLM이나
AI 모델이 판단하지 않으므로 이 예제는 AI Agent가 아니라 Rule-based/Mock Agent입니다.
06에서는 이 ``decide`` 역할을 OpenAI 모델이 수행하도록 교체합니다.
"""

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
