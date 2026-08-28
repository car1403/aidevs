"""Workflow: Tool Result와 관계없이 개발자가 정한 순서로 실행합니다."""

from travel_tools import get_weather, search_outdoor_places


def run_workflow(city: str) -> dict:
    trace = []
    weather = get_weather(city)
    trace.append({"step": 1, "action": "get_weather", "result": weather})
    # 비가 와도 다음 단계는 항상 야외 장소 검색으로 고정되어 있습니다.
    places = search_outdoor_places(city)
    trace.append({"step": 2, "action": "search_outdoor_places", "result": places})
    return {"type": "fixed_workflow", "city": city, "weather": weather, "places": places, "status": "completed", "termination_reason": "fixed_steps_completed", "trace": trace}


if __name__ == "__main__":
    result = run_workflow("제주")
    print("날씨:", result["weather"])
    print("추천 장소:", result["places"]["items"])
    print("종료 이유:", result["termination_reason"])
    print("\n비가 와도 야외 장소를 검색합니다. 다음 단계가 코드에 고정된 Workflow이기 때문입니다.")
