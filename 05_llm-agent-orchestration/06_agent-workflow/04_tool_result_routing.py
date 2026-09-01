"""Tool Result가 다음 행동과 종료를 바꾸는 라우팅을 집중적으로 살펴봅니다.

03의 Agent Loop 안에도 Tool Result 기반 분기가 포함되어 있습니다. 이번 파일은 전체
Loop보다 ``관찰한 결과 → 다음 행동 선택`` 관계에 집중할 수 있도록 그 부분을 떼어
제주, 서울, 없는 도시라는 서로 다른 입력으로 비교합니다.

이번 파일에서 하는 일
----------------------
1. 날씨 Tool을 먼저 실행하여 성공 여부와 날씨 조건을 얻습니다.
2. 실패하면 근거 부족으로 중단합니다.
3. 비가 오면 실내 장소 Tool, 그 외에는 야외 장소 Tool로 라우팅합니다.
4. 각 Tool Result와 결정 이유를 trace에 남깁니다.

이 파일은 정해진 두 단계만 실행하며 반복 State Loop가 없습니다. 또한 라우팅 판단도
개발자의 if 문이 수행합니다. 즉, 새로운 AI Agent 구현이 아니라 03에서 사용한
Tool-result routing과 안전한 종료 조건을 별도로 연습하는 예제입니다.
"""

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
    trace.append({"stage": "routing_decision", **decision})
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
