from shared.travel_observability import classify_failure


failures = [
    TimeoutError("날씨 서비스 응답 지연"),
    ValueError("일정 Agent에 필요한 입력 누락"),
    PermissionError("허용되지 않은 Tool"),
    RuntimeError("원인을 자동으로 복구할 수 없음"),
]

for error in failures:
    print(type(error).__name__, "->", classify_failure(error))
