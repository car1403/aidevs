"""여행 요청에서 Mock Tool을 선택하고 안전하게 실행하는 예제."""

from collections.abc import Callable
from datetime import date
from pydantic import BaseModel, Field


class WeatherArgs(BaseModel):
    city: str = Field(min_length=1)
    target_date: date


class HotelArgs(BaseModel):
    city: str = Field(min_length=1)
    check_in: date
    check_out: date
    guests: int = Field(ge=1, le=10)


def get_weather(payload: dict) -> dict:
    args = WeatherArgs.model_validate(payload)
    return {
        "city": args.city,
        "date": args.target_date.isoformat(),
        "condition": "맑음",
        "temperature_c": 26,
        "source": "mock",
    }


def search_hotels(payload: dict) -> dict:
    args = HotelArgs.model_validate(payload)
    if args.check_out <= args.check_in:
        raise ValueError("체크아웃은 체크인 이후여야 합니다.")
    return {
        "items": [
            {"name": "바다 호텔", "price_per_night": 120000},
            {"name": "도시 호텔", "price_per_night": 90000},
        ],
        "guests": args.guests,
        "source": "mock",
    }


TOOLS: dict[str, Callable[[dict], dict]] = {
    "get_weather": get_weather,
    "search_hotels": search_hotels,
}


def select_tool(message: str) -> str | None:
    if any(word in message for word in ("날씨", "비", "기온")):
        return "get_weather"
    if any(word in message for word in ("호텔", "숙소")):
        return "search_hotels"
    return None


def execute(name: str, payload: dict) -> dict:
    if name not in TOOLS:
        return {"success": False, "error": {"code": "TOOL_NOT_ALLOWED"}}
    try:
        return {"success": True, "data": TOOLS[name](payload)}
    except Exception as error:
        return {"success": False, "error": {"code": "TOOL_ERROR", "message": str(error)}}


if __name__ == "__main__":
    request = "부산 호텔을 찾아줘."
    selected = select_tool(request)
    print("선택:", selected)
    print(
        execute(
            selected or "",
            {
                "city": "부산",
                "check_in": "2026-08-10",
                "check_out": "2026-08-12",
                "guests": 2,
            },
        )
    )
