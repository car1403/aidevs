"""과정 루트 .env의 LLM 설정으로 Provider를 직접 호출합니다.

Mini Backend를 실행하지 않습니다. 과정 루트에서 `pip install -e .` 후 실행합니다.
"""

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
