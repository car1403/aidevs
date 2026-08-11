from datetime import date


def validate_plan(
    move_date: date,
    budget: int,
    max_cost: int,
    *,
    reference_date: date | None = None,
) -> list[str]:
    today = reference_date or date.today()
    errors = []
    if move_date <= today:
        errors.append("이사 날짜는 오늘 이후여야 합니다.")
    if budget <= 0 or max_cost < 0:
        errors.append("금액은 올바른 양수 범위여야 합니다.")
    if max_cost > budget:
        errors.append("예상 최대 비용이 예산을 초과합니다.")
    return errors


if __name__ == "__main__":
    fixed_today = date(2026, 8, 11)
    print(validate_plan(fixed_today, 500_000, 700_000, reference_date=fixed_today))

