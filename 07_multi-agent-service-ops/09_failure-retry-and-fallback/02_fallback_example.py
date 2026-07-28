def quote_with_fallback(tool) -> dict:
    try:
        return {"status": "completed", "source": "quote_tool", "data": tool()}
    except TimeoutError:
        return {
            "status": "completed_with_fallback",
            "source": "education_estimate",
            "data": {"min_cost": 500_000, "max_cost": 800_000},
            "warning": "실제 견적 조회 실패로 교육용 예상 범위를 사용했습니다.",
        }


if __name__ == "__main__":
    def failed_tool():
        raise TimeoutError

    print(quote_with_fallback(failed_tool))

