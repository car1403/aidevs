"""LLM Tool 선택과 Backend Tool 실행을 분리해서 확인합니다."""

import os

import httpx
from dotenv import load_dotenv


load_dotenv()
BASE_URL = os.getenv("PYTHON_AGENT_API_URL", "http://127.0.0.1:8000")
provider = os.getenv("LLM_PROVIDER", "ollama")

selected = httpx.post(
    f"{BASE_URL}/api/tools/select",
    json={
        "provider": provider,
        "message": "8월 10일부터 12일까지 성인 2명 부산 숙소를 찾아줘.",
    },
    timeout=90,
)
selected.raise_for_status()
decision = selected.json()["data"]
print("LLM 선택:", decision)

if decision["tool_name"]:
    executed = httpx.post(
        f"{BASE_URL}/api/tools/run",
        json={
            "tool_name": decision["tool_name"],
            "arguments": decision["arguments"],
        },
        timeout=30,
    )
    executed.raise_for_status()
    print("Backend 실행:", executed.json()["data"])
