def run_with_retry(action, *, max_retries: int = 1):
    errors = []
    for attempt in range(1, max_retries + 2):
        try:
            return {"status": "completed", "attempt": attempt, "result": action()}
        except TimeoutError as exc:
            errors.append(str(exc))
    return {"status": "failed_after_retry", "errors": errors}


if __name__ == "__main__":
    attempts = {"count": 0}

    def unstable():
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise TimeoutError("교육용 timeout")
        return {"quote": 650_000}

    print(run_with_retry(unstable))

