"""Backend를 통해 GPT, Gemini, Ollama/Llama를 같은 방식으로 호출합니다."""

import os

import httpx
from dotenv import load_dotenv


load_dotenv()
BASE_URL = os.getenv("PYTHON_AGENT_API_URL", "http://127.0.0.1:8000")

for provider in ("openai", "gemini", "ollama"):
    try:
        response = httpx.post(
            f"{BASE_URL}/api/providers/generate",
            json={
                "provider": provider,
                "message": "부산 2박 여행을 준비할 때 먼저 확인할 것은 무엇인가요?",
            },
            timeout=60,
        )
        response.raise_for_status()
        data = response.json()["data"]
        print(provider, data["model"], data["latency_ms"], data["content"])
    except httpx.HTTPError as error:
        print(provider, "호출 실패:", error)
