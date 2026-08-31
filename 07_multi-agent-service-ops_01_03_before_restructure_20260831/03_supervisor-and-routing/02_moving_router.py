from shared.moving_agents import route_request


if __name__ == "__main__":
    for message in [
        "짐 목록을 만들어 주세요.",
        "이사 비용과 주소 변경을 확인해 주세요.",
        "이사를 도와주세요.",
    ]:
        print(message)
        print(route_request(message).model_dump())

