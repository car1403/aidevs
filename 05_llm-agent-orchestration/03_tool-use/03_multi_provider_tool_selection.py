"""Backend의 공통 Tool 계약으로 세 Provider의 선택 결과를 비교합니다."""

import os

import httpx
from dotenv import load_dotenv


load_dotenv()
BASE_URL = os.getenv("PYTHON_AGENT_API_URL", "http://127.0.0.1:8000")
message = "8월 10일부터 12일까지 성인 2명 부산 숙소를 찾아줘."

for provider in ("openai", "gemini", "ollama"):
    try:
        response = httpx.post(
            f"{BASE_URL}/api/tools/select",
            json={"provider": provider, "message": message},
            timeout=90,
        )
        response.raise_for_status()
        print(provider, response.json()["data"])
    except httpx.HTTPError as error:
        print(provider, "실행 실패:", error)
