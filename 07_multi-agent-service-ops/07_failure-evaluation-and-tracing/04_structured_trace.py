from shared.travel_observability import TraceEvent


events = [
    TraceEvent(task_id="travel-001", trace_id="trace-001", step=1, actor="supervisor", action="route", status="completed", duration_ms=42),
    TraceEvent(task_id="travel-001", trace_id="trace-001", step=2, actor="weather_agent", action="get_weather", status="completed", duration_ms=180),
    TraceEvent(task_id="travel-001", trace_id="trace-001", step=3, actor="place_agent", action="search_places", status="failed", duration_ms=3000, error_type="TimeoutError"),
    TraceEvent(task_id="travel-001", trace_id="trace-001", step=4, actor="orchestrator", action="replan", status="completed", details={"kept_results": ["weather_agent"]}),
]

for event in events:
    print(event.model_dump_json())

failed = [event for event in events if event.status == "failed"]
print("\n실패 지점:", [(event.actor, event.action, event.error_type) for event in failed])
