"""Lab 02-3: 타입은 맞지만 의미가 틀린 결과를 차단합니다."""

from pydantic import ValidationError

from shared.travel_contracts import BudgetResult, ValidationResult


CASES = [
    (
        "정상 예산",
        BudgetResult,
        {"breakdown": {"교통": 100_000, "숙박": 300_000}, "total": 400_000},
        True,
    ),
    (
        "합계 불일치",
        BudgetResult,
        {"breakdown": {"교통": 100_000, "숙박": 300_000}, "total": 350_000},
        False,
    ),
    (
        "음수 예산",
        BudgetResult,
        {"breakdown": {"할인": -10_000, "숙박": 300_000}, "total": 290_000},
        False,
    ),
    (
        "통과했지만 issue 존재",
        ValidationResult,
        {"passed": True, "issues": ["알레르기 조건 누락"]},
        False,
    ),
]


def is_valid(schema, payload: dict) -> bool:
    try:
        schema.model_validate(payload)
        return True
    except ValidationError as error:
        print("차단 이유:", error.errors()[0]["msg"])
        return False


if __name__ == "__main__":
    for name, schema, payload, expected in CASES:
        actual = is_valid(schema, payload)
        print(f"{name}: {'통과' if actual else '차단'}")
        assert actual is expected

    print("확인: Pydantic 타입 성공과 업무 의미의 정확성은 같은 것이 아닙니다.")
