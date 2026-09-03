"""Lab 02-1: 자유 문자열과 구조화된 Agent 계약의 차이를 확인합니다."""

from shared.travel_contracts import BudgetResult, SpecialistResult, WeatherResult


result = SpecialistResult(
    agent_id="budget_agent",
    goal="여행 예산 항목과 계산 입력 확인",
    summary="교통·숙박·식비 예산을 분리해야 합니다.",
    recommendations=["숙박비 한도를 먼저 정하세요.", "예비비를 별도로 두세요."],
    missing_information=["숙박 가격", "출발지 교통비"],
    completed=False,
)

print(result.model_dump_json(indent=2))

weather = WeatherResult(
    forecast_summary="둘째 날 비 가능성",
    cautions=["작은 우산 준비", "실내 대체 일정 준비"],
    source_confirmed=True,
)
budget = BudgetResult(
    breakdown={"교통": 100_000, "숙박": 300_000, "식비": 150_000, "예비비": 50_000},
    total=600_000,
)

print("\n역할별 Weather 계약:")
print(weather.model_dump_json(indent=2))
print("\n역할별 Budget 계약:")
print(budget.model_dump_json(indent=2))

assert weather.agent_id == "weather_agent"
assert sum(budget.breakdown.values()) == budget.total
print("\n확인: 역할별 계약은 서로 다른 업무 필드와 검증 규칙을 가집니다.")
