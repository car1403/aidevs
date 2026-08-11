"""독립 조사를 병렬 실행한 뒤 결과가 모두 준비되면 다음 단계를 실행합니다."""

from concurrent.futures import ThreadPoolExecutor


def address_agent() -> dict:
    return {"address_tasks": ["전입 신고", "우편물 변경"]}


def cleaning_agent() -> dict:
    return {"cleaning_tasks": ["입주 청소", "폐기물 확인"]}


def summary_agent(context: dict) -> dict:
    return {
        "total_tasks": len(context["address_tasks"]) + len(context["cleaning_tasks"]),
        "ready": True,
    }


def run() -> dict:
    with ThreadPoolExecutor(max_workers=2) as executor:
        address_future = executor.submit(address_agent)
        cleaning_future = executor.submit(cleaning_agent)
        context = {**address_future.result(), **cleaning_future.result()}
    return {"parallel_results": context, "summary": summary_agent(context)}


if __name__ == "__main__":
    print(run())
