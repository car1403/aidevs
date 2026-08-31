from pprint import pprint

from shared.travel_orchestration import ExecutionPlan, PlanStep


plan = ExecutionPlan(
    goal="날씨·장소·예산을 고려한 부산 2박 3일 일정 만들기",
    steps=[
        PlanStep(step_id="research", agents=["weather_agent", "place_agent", "budget_agent"]),
        PlanStep(
            step_id="compose",
            agents=["itinerary_agent"],
            depends_on=["research"],
            join=True,
        ),
    ],
    max_steps=5,
)

pprint(plan.model_dump())
print("\nresearch의 세 Agent는 병렬, itinerary_agent는 Join 뒤에 실행합니다.")
