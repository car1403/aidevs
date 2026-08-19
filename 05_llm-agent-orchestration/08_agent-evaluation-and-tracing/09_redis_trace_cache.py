"""최근 평가 Trace를 Redis에 TTL과 함께 캐시하는 선택 예제입니다."""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from redis import Redis
from redis.exceptions import RedisError


API_URL = os.getenv("MINI_AGENT_API_URL", "http://localhost:8000")
REDIS_URL = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
TRACE_TTL_SECONDS = int(os.getenv("EVALUATION_TRACE_TTL_SECONDS", "600"))


def run_evaluation() -> dict:
    """평가 API를 호출해 시나리오별 Trace가 포함된 결과를 받습니다."""
    request = Request(
        f"{API_URL.rstrip('/')}/api/evaluations/run",
        data=b'{"scenarios": []}',
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))["data"]


def cache_failed_traces(client: Redis, evaluation: dict) -> list[str]:
    """장기 이력이 아닌 최근 실패 Trace만 짧게 보관합니다."""
    keys = []
    for index, result in enumerate(evaluation["results"], start=1):
        if result["passed"]:
            continue
        key = f"evaluation:failed-trace:{index}"
        client.setex(key, TRACE_TTL_SECONDS, json.dumps(result["trace"], ensure_ascii=False))
        keys.append(key)
    return keys


def main() -> None:
    try:
        evaluation = run_evaluation()
        client = Redis.from_url(REDIS_URL, decode_responses=True)
        client.ping()
        keys = cache_failed_traces(client, evaluation)
    except (HTTPError, URLError, TimeoutError, RedisError) as error:
        raise SystemExit(f"평가 API 또는 Redis 연결 실패: {error}") from error

    print({"cached_failed_traces": keys, "ttl_seconds": TRACE_TTL_SECONDS})


if __name__ == "__main__":
    main()
