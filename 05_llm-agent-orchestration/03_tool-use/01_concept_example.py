"""여러 Tool 중 하나를 선택하고 실행하는 최소 예제."""

from collections.abc import Callable
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    left: float
    right: float


class WeatherInput(BaseModel):
    city: str = Field(min_length=1)


def calculator(payload: dict) -> dict:
    data = CalculatorInput.model_validate(payload)
    return {"value": data.left + data.right}


def weather(payload: dict) -> dict:
    data = WeatherInput.model_validate(payload)
    return {"city": data.city, "condition": "맑음", "source": "mock"}


TOOLS: dict[str, Callable[[dict], dict]] = {
    "calculator": calculator,
    "weather": weather,
}


def run_tool(name: str, payload: dict) -> dict:
    if name not in TOOLS:
        return {"success": False, "error": "허용되지 않은 Tool입니다."}
    try:
        return {"success": True, "data": TOOLS[name](payload)}
    except Exception as error:
        return {"success": False, "error": str(error)}


if __name__ == "__main__":
    print(run_tool("weather", {"city": "부산"}))
    print(run_tool("calculator", {"left": 10, "right": 20}))
    print(run_tool("delete_database", {}))
