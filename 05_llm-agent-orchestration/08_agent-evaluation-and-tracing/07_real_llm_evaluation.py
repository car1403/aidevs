"""실제 LLM의 구조화된 응답을 규칙 기반으로 평가합니다.

Mini Agent 08 Backend가 먼저 실행되어 있어야 합니다. Provider를 지정하지
않으면 Backend의 기본 Provider를 사용하므로 Mock과 실제 LLM을 같은 평가
규칙으로 비교할 수 있습니다.
"""

import argparse
import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DEFAULT_API_URL = os.getenv("MINI_AGENT_API_URL", "http://localhost:8000")


def request_travel_plan(api_url: str, provider: str | None, message: str) -> dict:
    """Backend의 구조화 출력 API를 호출하고 실제 응답 데이터만 반환합니다."""
    payload = {"message": message}
    if provider:
        payload["provider"] = provider

    request = Request(
        f"{api_url.rstrip('/')}/api/providers/travel-plan",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=60) as response:
        body = json.loads(response.read().decode("utf-8"))
    return body["data"]


def evaluate_plan(result: dict, expected_destination: str) -> dict:
    """표현이 달라도 안정적으로 검사할 수 있는 구조와 내용만 평가합니다."""
    content = result.get("content", {})
    destination = str(content.get("destination", ""))
    activities = content.get("activities", [])
    days = content.get("recommended_days")
    checks = {
        "structured_output": isinstance(content, dict),
        "destination_grounded": expected_destination in destination,
        "days_in_range": isinstance(days, int) and 1 <= days <= 30,
        "has_activities": isinstance(activities, list) and len(activities) > 0,
    }
    return {
        "provider": result.get("provider"),
        "model": result.get("model"),
        "latency_ms": result.get("latency_ms"),
        "passed": all(checks.values()),
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="실제 LLM 구조화 응답 평가")
    parser.add_argument("--api-url", default=DEFAULT_API_URL)
    parser.add_argument("--provider", choices=["mock", "openai", "gemini", "ollama"])
    args = parser.parse_args()

    message = "부산의 대표 장소를 포함한 2박 3일 여행 계획을 만들어 주세요."
    try:
        result = request_travel_plan(args.api_url, args.provider, message)
        print(json.dumps(evaluate_plan(result, "부산"), ensure_ascii=False, indent=2))
    except (HTTPError, URLError, TimeoutError) as error:
        raise SystemExit(f"Backend 또는 LLM 호출 실패: {error}") from error


if __name__ == "__main__":
    main()
