"""Lab 02-2: 형식과 역할이 잘못된 여러 결과를 계약으로 차단합니다."""

from pydantic import ValidationError

from shared.travel_contracts import BudgetResult, SpecialistResult, WeatherResult


CASES = [
    (
        "허용되지 않은 Agent",
        SpecialistResult,
        {"agent_id": "payment_agent", "goal": "결제", "summary": "완료", "recommendations": ["없음"], "completed": True},
    ),
    (
        "필수 필드 누락",
        WeatherResult,
        {"agent_id": "weather_agent", "cautions": []},
    ),
    (
        "다른 역할로 위장",
        WeatherResult,
        {"agent_id": "budget_agent", "forecast_summary": "맑음", "source_confirmed": True},
    ),
    (
        "잘못된 금액 타입",
        BudgetResult,
        {"breakdown": {"숙박": "삼십만원"}, "total": 300_000},
    ),
]

blocked = 0
for name, schema, payload in CASES:
    try:
        schema.model_validate(payload)
    except ValidationError as error:
        blocked += 1
        first_error = error.errors()[0]
        print(f"{name}: 차단 / 위치={first_error['loc']} / 이유={first_error['msg']}")

assert blocked == len(CASES)
print(f"총 {blocked}개의 계약 위반을 모두 차단했습니다.")
