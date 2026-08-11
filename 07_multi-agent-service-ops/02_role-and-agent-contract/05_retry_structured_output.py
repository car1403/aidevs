"""실제 Provider의 구조화 출력 실패를 제한된 횟수로 다시 요청합니다.

Mini Backend를 실행하지 않습니다. 과정 루트 .env에 Provider Key를 설정합니다.
"""

import json
import os

from pydantic import ValidationError

from shared.providers import worker_with_metadata


def run_with_one_retry(provider: str, message: str) -> dict:
    errors = []
    for attempt in range(1, 3):
        try:
            result = worker_with_metadata(provider, message, allow_mock_fallback=False)
            return {"attempts": attempt, "errors": errors, **result}
        except (ValidationError, RuntimeError, KeyError) as exc:
            errors.append(f"{type(exc).__name__}: {exc}")
    raise RuntimeError(f"구조화 출력 검증에 2회 실패했습니다: {errors}")


if __name__ == "__main__":
    output = run_with_one_retry(
        os.getenv("LLM_PROVIDER", "openai"),
        "학생도 이해하기 쉬운 이사 짐 분류 결과를 작성해 주세요.",
    )
    print(json.dumps(output, ensure_ascii=False, indent=2))
