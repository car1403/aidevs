"""같은 여행 요청을 Fixed Workflow와 Conditional Workflow로 비교합니다."""

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
