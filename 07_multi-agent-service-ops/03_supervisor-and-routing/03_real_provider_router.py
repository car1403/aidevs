import os

from shared.providers import pretty_route


if __name__ == "__main__":
    message = "짐 목록과 예상 비용을 알려 주세요."
    provider = os.getenv("LLM_PROVIDER", "mock")
    print(pretty_route(provider, message))
