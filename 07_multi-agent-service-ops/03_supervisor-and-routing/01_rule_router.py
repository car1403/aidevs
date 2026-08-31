"""LLM 없이 명시적인 규칙으로 요청을 Agent에 배정합니다."""

from shared.travel_contracts import RouteDecision


def route(message: str) -> RouteDecision:
    selected = []
    if any(word in message for word in ("날씨", "비", "기온")):
        selected.append("weather_agent")
    if any(word in message for word in ("장소", "관광", "맛집")):
        selected.append("place_agent")
    if any(word in message for word in ("예산", "비용", "가격")):
        selected.append("budget_agent")
    return RouteDecision(
        selected_agents=selected or ["itinerary_agent"],
        reason="개발자가 정의한 Keyword 규칙",
        missing_information=[],
    )


print(route("부산 날씨와 예산을 고려해 장소를 추천해 줘.").model_dump_json(indent=2))
