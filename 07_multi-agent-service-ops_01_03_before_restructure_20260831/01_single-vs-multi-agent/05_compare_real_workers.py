"""과정 루트 .env에 설정한 실제 Provider Worker 결과를 직접 비교합니다.

Mini Backend를 실행하지 않습니다. 과정 루트에서 `pip install -e .` 후 실행합니다.
"""

import json
import os

from shared.providers import compare_providers


if __name__ == "__main__":
    providers = os.getenv("COMPARE_PROVIDERS", "openai,gemini,ollama").split(",")
    results = compare_providers(
        "worker",
        [provider.strip() for provider in providers],
        "원룸 이사를 위해 짐을 어떻게 분류하면 좋을까요?",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))
