"""서로 다른 Tool Result가 Agent의 다음 행동과 종료를 바꾸는지 비교합니다."""

from typing import Any
from travel_tools import execute_tool


def choose_place_tool(weather_result: dict[str, Any]) -> dict[str, str]:
    if not weather_result.get("success"):
        return {"action": "stop", "reason": "missing_weather_evidence"}
    if weather_result["condition"] == "비":
        return {"action": "search_indoor_places", "reason": "rain_detected"}
    return {"action": "search_outdoor_places", "reason": "clear_weather_detected"}


def run(city: str) -> dict[str, Any]:
    trace = []
    weather = execute_tool("get_weather", {"city": city})
    trace.append({"stage": "tool_result", "tool": "get_weather", "data": weather})
    decision = choose_place_tool(weather)
    trace.append({"stage": "agent_decision", **decision})
    if decision["action"] == "stop":
        return {"city": city, "weather": weather, "places": [], "selected_action": "stop", "status": "stopped", "termination_reason": decision["reason"], "trace": trace}
    places = execute_tool(decision["action"], {"city": city})
    trace.append({"stage": "tool_result", "tool": decision["action"], "data": places})
    return {"city": city, "weather": weather, "places": places["items"], "selected_action": decision["action"], "status": "completed", "termination_reason": "completed", "trace": trace}


if __name__ == "__main__":
    for city in ("제주", "서울", "없는도시"):
        result = run(city)
        print(f"\n도시: {city}")
        print("날씨:", result["weather"])
        print("다음 행동:", result["selected_action"])
        print("장소:", result["places"])
        print("종료 이유:", result["termination_reason"])
