"""설정된 실제 Provider의 결과 계약을 같은 조건에서 비교합니다.

Mini Backend를 실행하지 않습니다. 과정 루트 .env에 비교할 Provider Key를 설정합니다.
"""

import json
import os

from shared.providers import compare_providers


if __name__ == "__main__":
    providers = os.getenv("COMPARE_PROVIDERS", "openai,gemini,ollama").split(",")
    results = compare_providers(
        "worker",
        [provider.strip() for provider in providers],
        "냉장고와 책이 많은 원룸의 포장 계획을 만들어 주세요.",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))
