from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor, as_completed

from shared.travel_contracts import SPECIALIST_GOALS, SpecialistResult
from shared.travel_llm import run_structured


REQUEST = "부산 2박 3일, 해산물 알레르기, 대중교통, 예산 60만원"


def run_specialist(agent_id: str) -> SpecialistResult:
    provider = os.getenv(f"{agent_id.removesuffix('_agent').upper()}_AGENT_PROVIDER", os.getenv("LLM_PROVIDER", "openai"))
    prompt = f"""당신은 {agent_id}입니다.
독립 목표: {SPECIALIST_GOALS[agent_id]}
사용자 요청: {REQUEST}
아직 다른 Agent의 결과는 추측하지 말고 SpecialistResult 계약으로 답하세요.
agent_id는 반드시 {agent_id}로 반환하세요."""
    return run_structured(provider, prompt, SpecialistResult)


agent_ids = ["weather_agent", "place_agent", "budget_agent"]
results: dict[str, SpecialistResult] = {}

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {executor.submit(run_specialist, agent_id): agent_id for agent_id in agent_ids}
    for future in as_completed(futures):
        agent_id = futures[future]
        results[agent_id] = future.result()
        print(f"완료: {agent_id}")

print("\nJoin 완료:", list(results))
print("이제 세 결과를 입력으로 itinerary_agent를 실행할 수 있습니다.")
