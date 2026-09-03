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
missing = set(agent_ids) - set(results)
if missing:
    raise RuntimeError(f"Join에 필요한 결과가 없습니다: {sorted(missing)}")

itinerary_provider = os.getenv("ITINERARY_AGENT_PROVIDER", os.getenv("LLM_PROVIDER", "openai"))
joined_context = {name: result.model_dump() for name, result in results.items()}
itinerary = run_structured(
    itinerary_provider,
    f"""당신은 itinerary_agent입니다.
사용자 요청: {REQUEST}
검증된 전문 Agent 결과: {joined_context}
세 결과를 종합해 SpecialistResult 계약으로 일정 초안을 반환하세요.
agent_id는 반드시 itinerary_agent로 반환하세요.""",
    SpecialistResult,
)
if itinerary.agent_id != "itinerary_agent":
    raise RuntimeError("Join 결과를 처리한 Agent가 itinerary_agent가 아닙니다.")

print("일정 Join 결과:", itinerary.model_dump_json(indent=2))
