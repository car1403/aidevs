import json
import os

from shared.providers import worker_with_metadata


if __name__ == "__main__":
    provider = os.getenv("LLM_PROVIDER", "openai")
    result = worker_with_metadata(
        provider,
        "침대와 냉장고가 있는 원룸 이사 짐 목록을 정리해 주세요.",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
