"""06 Agent Workflow의 모든 예제가 공유하는 여행 mock Tool 계층입니다.

각 예제가 동일한 입력과 Tool Result를 사용하게 하여 Workflow/Agent 실행 구조의 차이에
집중하도록 만든 공용 모듈입니다. 외부 날씨·장소 API를 호출하지 않고 메모리의 고정
데이터를 반환하므로 비용과 네트워크 없이 반복 실행할 수 있습니다.

이번 파일이 제공하는 것
-----------------------
* ``get_weather``: 성공 또는 도시 없음 결과를 반환하는 읽기 전용 날씨 Tool
* ``search_indoor_places`` / ``search_outdoor_places``: 조건별 장소 검색 Tool
* ``TOOLS``: Agent가 실행할 수 있는 Tool allowlist
* ``execute_tool``: Tool 이름과 arguments를 검증한 뒤 허용된 함수만 실행하는 dispatcher

이 파일은 판단하거나 다음 Tool을 선택하지 않으므로 Agent가 아닙니다. Workflow 또는
AI Agent가 선택한 행동을 실제 Python 함수로 수행하고 관찰 가능한 결과를 돌려주는
Tool 실행 계층입니다.
"""

from typing import Any

WEATHER = {"서울": {"condition": "맑음", "temperature_c": 24}, "제주": {"condition": "비", "temperature_c": 21}}
INDOOR_PLACES = {"서울": ["국립중앙박물관", "서울시립미술관"], "제주": ["제주현대미술관", "아쿠아플라넷"]}
OUTDOOR_PLACES = {"서울": ["서울숲", "북한산"], "제주": ["비자림", "성산일출봉"]}


def get_weather(city: str) -> dict[str, Any]:
    """도시의 현재 날씨를 조회하는 읽기 전용 mock Tool입니다."""
    data = WEATHER.get(city)
    if data is None:
        return {"success": False, "error": "CITY_NOT_FOUND", "retryable": False, "city": city, "source": "mock-weather"}
    return {"success": True, "city": city, **data, "source": "mock-weather"}


def search_indoor_places(city: str) -> dict[str, Any]:
    """비 오는 날에 적합한 실내 장소를 검색하는 mock Tool입니다."""
    return {"success": True, "city": city, "category": "indoor", "items": INDOOR_PLACES.get(city, []), "source": "mock-places"}


def search_outdoor_places(city: str) -> dict[str, Any]:
    """맑은 날에 적합한 야외 장소를 검색하는 mock Tool입니다."""
    return {"success": True, "city": city, "category": "outdoor", "items": OUTDOOR_PLACES.get(city, []), "source": "mock-places"}


TOOLS = {"get_weather": get_weather, "search_indoor_places": search_indoor_places, "search_outdoor_places": search_outdoor_places}


def execute_tool(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    """학습용 Allowlist에서 찾은 Tool만 실행합니다."""
    tool = TOOLS.get(tool_name)
    if tool is None:
        return {"success": False, "error": "TOOL_NOT_ALLOWED", "retryable": False}
    city = arguments.get("city")
    if not isinstance(city, str) or not city.strip():
        return {"success": False, "error": "INVALID_CITY", "retryable": False}
    return tool(city.strip())
