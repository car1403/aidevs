"""병렬 Worker 하나가 실패해도 성공 결과와 오류를 함께 보존합니다."""

from concurrent.futures import ThreadPoolExecutor, as_completed
from collections.abc import Callable


def address_agent() -> dict:
    return {"agent_name": "address_agent", "checklist": ["전입 신고", "우편물 변경"]}


def unavailable_cleaning_agent() -> dict:
    raise TimeoutError("교육용 Cleaning Agent timeout")


def run_jobs(jobs: dict[str, Callable[[], dict]]) -> dict:
    completed: dict[str, dict] = {}
    failed: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=len(jobs)) as executor:
        futures = {executor.submit(fn): name for name, fn in jobs.items()}
        for future in as_completed(futures):
            name = futures[future]
            try:
                completed[name] = future.result()
            except Exception as exc:
                failed[name] = {"error_type": type(exc).__name__, "error": str(exc)}
    return {"completed": completed, "failed": failed, "partial_success": bool(completed and failed)}


if __name__ == "__main__":
    print(run_jobs({"address_agent": address_agent, "cleaning_agent": unavailable_cleaning_agent}))
