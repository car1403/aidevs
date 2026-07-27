"""세 Provider가 동일한 TravelPlan Schema를 반환하는지 비교합니다."""

import os

import httpx
from dotenv import load_dotenv


load_dotenv()
BASE_URL = os.getenv("PYTHON_AGENT_API_URL", "http://127.0.0.1:8000")

for provider in ("mock", "openai", "gemini", "ollama"):
    try:
        response = httpx.post(
            f"{BASE_URL}/api/providers/travel-plan",
            json={
                "provider": provider,
                "message": "부산에서 대중교통으로 즐기는 2박 3일 여행을 제안해 주세요.",
            },
            timeout=90,
        )
        response.raise_for_status()
        result = response.json()["data"]
        print(f"\n[{provider}] {result['latency_ms']}ms")
        print(result["content"])
    except httpx.HTTPError as error:
        print(f"\n[{provider}] 호출 실패: {error}")
