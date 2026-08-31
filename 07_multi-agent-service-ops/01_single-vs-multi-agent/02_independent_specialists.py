"""독립 Goal을 가진 실제 LLM Specialist를 아직 Orchestration 없이 직접 실행합니다."""

import json
import os

from shared.travel_contracts import SPECIALIST_GOALS, SpecialistResult
from shared.travel_llm import run_with_metadata


REQUEST = "부산 2박 3일 여행, 해산물 알레르기, 대중교통, 총예산 60만 원"
PROVIDER = os.getenv("LLM_PROVIDER", "openai")

for agent_id in ("weather_agent", "place_agent", "budget_agent"):
    prompt = f"""
당신은 {agent_id}입니다.
Goal: {SPECIALIST_GOALS[agent_id]}
다른 Agent의 역할을 대신하지 말고 자신의 결과만 SpecialistResult 계약으로 반환하세요.
실시간 Tool을 호출하지 않았으므로 확인하지 않은 사실은 missing_information에 넣으세요.
여행 요청: {REQUEST}
""".strip()
    print(json.dumps(run_with_metadata(PROVIDER, prompt, SpecialistResult), ensure_ascii=False, indent=2))
