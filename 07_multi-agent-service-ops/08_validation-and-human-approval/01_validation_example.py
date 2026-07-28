from datetime import date


def validate_plan(move_date: date, budget: int, max_cost: int) -> list[str]:
    errors = []
    if move_date < date.today():
        errors.append("이사 날짜는 오늘 이후여야 합니다.")
    if budget <= 0 or max_cost < 0:
        errors.append("금액은 올바른 양수 범위여야 합니다.")
    if max_cost > budget:
        errors.append("예상 최대 비용이 예산을 초과합니다.")
    return errors


if __name__ == "__main__":
    print(validate_plan(date.today(), 500_000, 700_000))

