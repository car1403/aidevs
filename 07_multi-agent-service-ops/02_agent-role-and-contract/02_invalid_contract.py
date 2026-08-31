"""잘못된 Agent 이름과 누락된 필드를 Pydantic이 차단합니다."""

from pydantic import ValidationError

from shared.travel_contracts import SpecialistResult


invalid = {
    "agent_id": "payment_agent",
    "goal": "결제",
    "summary": "결제를 실행했습니다.",
    "recommendations": [],
    "completed": True,
}

try:
    SpecialistResult.model_validate(invalid)
except ValidationError as error:
    print("계약 위반 차단:")
    print(error)
