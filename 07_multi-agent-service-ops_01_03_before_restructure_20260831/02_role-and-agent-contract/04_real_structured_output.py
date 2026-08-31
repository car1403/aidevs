"""실제 Provider를 직접 호출하고 결과를 Agent 계약으로 검증합니다.

Mini Backend를 실행하지 않습니다. 과정 루트 .env에 Provider Key를 설정합니다.
"""

import json
import os

from shared.providers import worker_with_metadata


if __name__ == "__main__":
    result = worker_with_metadata(
        os.getenv("LLM_PROVIDER", "openai"),
        "주방, 침실, 욕실 순서로 이사 짐 체크리스트를 만들어 주세요.",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
