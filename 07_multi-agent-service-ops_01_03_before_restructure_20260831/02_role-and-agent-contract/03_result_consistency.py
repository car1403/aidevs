"""Schema뿐 아니라 필드 사이의 의미도 계약으로 검증합니다."""

from pydantic import ValidationError

from shared.contracts import AgentResult


CASES = [
    {
        "name": "정상 성공",
        "payload": {"agent_name": "packing_agent", "success": True},
    },
    {
        "name": "정상 실패",
        "payload": {
            "agent_name": "packing_agent",
            "success": False,
            "error": "짐 종류가 필요합니다.",
        },
    },
    {
        "name": "모순된 성공",
        "payload": {
            "agent_name": "packing_agent",
            "success": True,
            "error": "실패했다고 기록됨",
        },
    },
    {
        "name": "이유 없는 실패",
        "payload": {"agent_name": "packing_agent", "success": False},
    },
]


def validate_case(case: dict) -> dict:
    try:
        result = AgentResult.model_validate(case["payload"])
        return {"name": case["name"], "valid": True, "result": result.model_dump()}
    except ValidationError as exc:
        return {"name": case["name"], "valid": False, "error": str(exc.errors()[0]["msg"])}


if __name__ == "__main__":
    for item in CASES:
        print(validate_case(item))
