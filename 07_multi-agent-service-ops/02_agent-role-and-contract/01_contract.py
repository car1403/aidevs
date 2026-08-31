"""Agent 결과는 자유 문자열이 아니라 검증 가능한 계약으로 전달합니다."""

from shared.travel_contracts import SpecialistResult


result = SpecialistResult(
    agent_id="budget_agent",
    goal="여행 예산 항목과 계산 입력 확인",
    summary="교통·숙박·식비 예산을 분리해야 합니다.",
    recommendations=["숙박비 한도를 먼저 정하세요.", "예비비를 별도로 두세요."],
    missing_information=["숙박 가격", "출발지 교통비"],
    completed=False,
)

print(result.model_dump_json(indent=2))
