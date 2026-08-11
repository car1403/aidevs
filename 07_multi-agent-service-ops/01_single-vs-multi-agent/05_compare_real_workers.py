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
