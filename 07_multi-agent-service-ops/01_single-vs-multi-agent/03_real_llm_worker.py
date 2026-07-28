import os

from shared.providers import worker_with_provider


if __name__ == "__main__":
    provider = os.getenv("LLM_PROVIDER", "mock")
    result = worker_with_provider(
        provider,
        "침대와 냉장고가 있는 원룸 이사 짐 목록을 정리해 주세요.",
    )
    print(result.model_dump_json(indent=2))

