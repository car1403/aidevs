from __future__ import annotations

import os

from shared.travel_contracts import SPECIALIST_GOALS, SpecialistResult
from shared.travel_llm import run_structured
from shared.travel_orchestration import OrchestrationState


REQUEST = "부산 2박 3일, 해산물 알레르기, 대중교통, 예산 60만원"
ORDER = ["weather_agent", "place_agent", "budget_agent", "itinerary_agent"]
MAX_STEPS = int(os.getenv("MAX_ORCHESTRATION_STEPS", "8"))


def execute(agent_id: str, state: OrchestrationState) -> SpecialistResult:
    provider = os.getenv(f"{agent_id.removesuffix('_agent').upper()}_AGENT_PROVIDER", os.getenv("LLM_PROVIDER", "openai"))
    previous = {name: result.model_dump() for name, result in state.results.items()}
    prompt = f"""당신은 {agent_id}입니다.
목표: {SPECIALIST_GOALS[agent_id]}
사용자 요청: {state.request}
검증된 이전 결과: {previous}
자신의 목표 범위만 수행하고 SpecialistResult로 답하세요.
agent_id는 반드시 {agent_id}로 반환하세요."""
    return run_structured(provider, prompt, SpecialistResult)


state = OrchestrationState(request=REQUEST, status="running")
try:
    for agent_id in ORDER:
        if state.step_count >= MAX_STEPS:
            raise RuntimeError("최대 실행 단계를 초과했습니다.")
        if agent_id == "itinerary_agent" and len(state.results) < 3:
            raise RuntimeError("Join 이전에는 일정 Agent를 실행할 수 없습니다.")
        state.current_step = agent_id
        state.trace.append(f"started:{agent_id}")
        result = execute(agent_id, state)
        if result.agent_id != agent_id or not result.completed:
            raise RuntimeError(f"{agent_id}가 계약대로 완료되지 않았습니다.")
        state.results[agent_id] = result
        state.step_count += 1
        state.trace.append(f"completed:{agent_id}")
    state.current_step = None
    state.status = "completed"
except Exception as error:
    state.status = "failed"
    state.error = f"{type(error).__name__}: {error}"

print(state.model_dump_json(indent=2))
