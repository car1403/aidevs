from shared.travel_observability import TraceEvent


MAX_ATTEMPTS = 3
trace: list[TraceEvent] = []


def unstable_weather_service(attempt: int) -> dict[str, str]:
    # Retry 흐름을 재현하기 위한 의도적 실패이며 성공 결과를 외부 API처럼 위장하지 않습니다.
    if attempt < 3:
        raise TimeoutError("날씨 서비스 Timeout")
    return {"summary": "셋째 시도에서 응답 수신"}


for attempt in range(1, MAX_ATTEMPTS + 1):
    try:
        result = unstable_weather_service(attempt)
        trace.append(
            TraceEvent(
                task_id="travel-001",
                trace_id="trace-001",
                step=attempt,
                actor="weather_agent",
                action="get_weather",
                status="completed",
                attempt=attempt,
            )
        )
        print(result)
        break
    except TimeoutError as error:
        trace.append(
            TraceEvent(
                task_id="travel-001",
                trace_id="trace-001",
                step=attempt,
                actor="weather_agent",
                action="get_weather",
                status="failed",
                attempt=attempt,
                error_type=type(error).__name__,
            )
        )
else:
    raise RuntimeError("최대 시도 횟수 안에 복구하지 못했습니다.")

for event in trace:
    print(event.model_dump_json())
