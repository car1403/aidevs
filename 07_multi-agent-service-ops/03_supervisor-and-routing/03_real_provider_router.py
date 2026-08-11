import os
import json

from shared.providers import route_with_metadata


if __name__ == "__main__":
    message = "짐 목록과 예상 비용을 알려 주세요."
    provider = os.getenv("LLM_PROVIDER", "openai")
    result = route_with_metadata(provider, message)
    print(json.dumps(result, ensure_ascii=False, indent=2))
