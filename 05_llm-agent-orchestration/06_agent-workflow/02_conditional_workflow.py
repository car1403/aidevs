"""고정 Workflow에 개발자 규칙에 의한 조건 분기를 추가합니다.

전체 학습 흐름에서 이 파일은 01의 고정 실행과 03의 반복 Agent Loop 사이에 있습니다.
실행 순서를 전부 고정하는 대신 날씨 Tool Result를 확인하여 실내 또는 야외 장소
Tool로 이동합니다.

이번 파일에서 하는 일
----------------------
1. ``run_workflow``로 항상 야외 장소를 찾는 고정 Workflow를 다시 실행합니다.
2. ``choose_action_by_rule``에서 날씨 결과를 Python if 문으로 판정합니다.
3. ``run_conditional_workflow``에서 판정 결과에 따라 다음 Tool을 선택합니다.
4. 두 결과를 나란히 출력하여 고정 순서와 조건부 라우팅을 비교합니다.

분기는 생겼지만 판단 주체는 LLM이 아니라 개발자가 작성한 규칙이며, 판단과 행동을
반복하는 Loop도 없습니다. 따라서 아직 AI Agent가 아니라 Conditional Workflow입니다.
"""

from travel_tools import get_weather, search_indoor_places, search_outdoor_places


def run_workflow(city: str) -> dict:
    weather = get_weather(city)
    places = search_outdoor_places(city)
    return {"decision_maker": "developer", "weather": weather, "places": places, "selected_action": "search_outdoor_places"}


def choose_action_by_rule(weather_result: dict) -> str:
    """개발자가 작성한 규칙으로 다음 행동을 선택합니다."""
    if not weather_result.get("success"):
        return "stop"
    return "search_indoor_places" if weather_result["condition"] == "비" else "search_outdoor_places"


def run_conditional_workflow(city: str) -> dict:
    weather = get_weather(city)
    action = choose_action_by_rule(weather)
    if action == "search_indoor_places":
        places = search_indoor_places(city)
    elif action == "search_outdoor_places":
        places = search_outdoor_places(city)
    else:
        places = {"success": False, "error": "WEATHER_EVIDENCE_REQUIRED", "items": []}
    return {"decision_maker": "developer_rule", "weather": weather, "places": places, "selected_action": action}


if __name__ == "__main__":
    workflow = run_workflow("제주")
    conditional = run_conditional_workflow("제주")
    print("Workflow 선택:", workflow["selected_action"], workflow["places"]["items"])
    print("Conditional Workflow 선택:", conditional["selected_action"], conditional["places"]["items"])
    print("\n차이는 Tool 개수가 아니라 다음 행동을 언제, 어떤 근거로 선택하는가입니다.")
