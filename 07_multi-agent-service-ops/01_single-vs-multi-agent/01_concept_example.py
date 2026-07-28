def single_agent(request: dict) -> dict:
    """한 함수가 모든 책임을 가진 비교용 예제."""
    boxes = request.get("box_count", 20)
    return {
        "packing": {"box_count": boxes},
        "budget": {"estimated_cost": 120_000 + boxes * 8_000},
    }


if __name__ == "__main__":
    print(single_agent({"box_count": 15}))

