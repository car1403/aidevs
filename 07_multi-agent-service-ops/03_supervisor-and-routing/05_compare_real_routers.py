import json
import os

from shared.providers import compare_providers


if __name__ == "__main__":
    providers = os.getenv("COMPARE_PROVIDERS", "openai,gemini,ollama").split(",")
    results = compare_providers(
        "route",
        [provider.strip() for provider in providers],
        "서울에서 부산으로 이사할 때 짐 목록과 예상 비용, 주소 변경을 도와주세요.",
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))
