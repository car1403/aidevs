r"""Mini Agent 02의 TravelPlan·SupportTicket 결과를 Provider별로 비교합니다.

실행 전 준비:
    cd C:\mini_agent_st\mini_agent_02_structured_output\backend
    uvicorn app.main:app --reload --port 8000

다른 주소를 사용하면 BACKEND_API_URL 환경 변수로 지정합니다.
"""

import os

import httpx
from dotenv import load_dotenv


load_dotenv()
BASE_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")


SAMPLES = {
    "travel_plan": "부산에서 대중교통으로 즐기는 2박 3일 여행을 제안해 주세요.",
    "support_ticket": "결제가 두 번 된 것 같습니다. 주문 번호는 아직 찾지 못했습니다.",
}


def compare_providers(schema_type: str, message: str) -> None:
    response = httpx.post(
        f"{BASE_URL}/api/structured/compare",
        json={
            "providers": ["mock", "gemini", "openai", "ollama"],
            "schema_type": schema_type,
            "message": message,
        },
        timeout=90,
    )
    response.raise_for_status()

    for item in response.json()["results"]:
        print(f"\n[{item['provider']}] {item['status']}")
        if item["status"] == "success":
            print(f"{item['model']} · {item['latency_ms']}ms")
            print(item["content"])
        else:
            print(item["error"])


if __name__ == "__main__":
    try:
        for selected_schema, sample_message in SAMPLES.items():
            print(f"\n===== {selected_schema} =====")
            compare_providers(selected_schema, sample_message)
    except httpx.HTTPError as error:
        print("Mini Agent 02 Backend 호출 실패:", error)
        print("Backend를 먼저 실행하고 BACKEND_API_URL을 확인하세요.")
