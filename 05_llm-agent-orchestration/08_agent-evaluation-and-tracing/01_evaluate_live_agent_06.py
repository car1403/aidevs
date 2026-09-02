"""실행 중인 Mini Agent 06의 Travel Agent를 평가합니다."""

import json
import os
from urllib.request import Request, urlopen


API_URL = os.getenv("MINI_AGENT_06_API_URL", "http://127.0.0.1:8000/api/agents/run")
QUESTION = "제주 날씨를 확인하고 비가 오면 실내 관광지를 추천해줘"
EXPECTED_TOOLS = ["get_weather", "search_indoor_places"]


def post_json(url: str, body: dict) -> dict:
    data = json.dumps(body).encode("utf-8")
    request = Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    with urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


actual = post_json(API_URL, {"agent_id": "travel", "question": QUESTION})
actual_tools = [
    event["tool"]
    for event in actual["trace"]
    if event.get("stage") == "tool_executed"
]

checks = {
    "정상 완료": actual["status"] == "completed",
    "정상 종료": actual["termination_reason"] == "model_finished",
    "Tool 실행 순서": actual_tools == EXPECTED_TOOLS,
}

print("평가 대상: Mini Agent 06 · Travel Agent")
print("질문:", QUESTION)
print("실행된 Tool:", actual_tools)
for name, passed in checks.items():
    print(f"- {name}: {'PASS' if passed else 'FAIL'}")
print("최종 평가:", "PASS" if all(checks.values()) else "FAIL")
