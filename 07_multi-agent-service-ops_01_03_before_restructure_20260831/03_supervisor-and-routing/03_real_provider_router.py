"""실제 Provider를 직접 호출해 Supervisor Routing 결과를 만듭니다.

Mini Backend를 실행하지 않습니다. 과정 루트 .env에 Provider Key를 설정합니다.
"""

import os
import json

from shared.providers import route_with_metadata


if __name__ == "__main__":
    message = "짐 목록과 예상 비용을 알려 주세요."
    provider = os.getenv("LLM_PROVIDER", "openai")
    result = route_with_metadata(provider, message)
    print(json.dumps(result, ensure_ascii=False, indent=2))
