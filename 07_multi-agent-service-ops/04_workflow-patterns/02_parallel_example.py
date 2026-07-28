from concurrent.futures import ThreadPoolExecutor, as_completed

from shared.moving_agents import address_agent


def cleaning_agent(_: dict) -> dict:
    return {"agent_name": "cleaning_agent", "checklist": ["입주 청소", "폐기물 확인"]}


def run_parallel() -> dict:
    jobs = {"address_agent": address_agent, "cleaning_agent": cleaning_agent}
    completed, failed = {}, {}
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = {executor.submit(fn, {}): name for name, fn in jobs.items()}
        for future in as_completed(futures):
            name = futures[future]
            try:
                result = future.result()
                completed[name] = (
                    result.model_dump() if hasattr(result, "model_dump") else result
                )
            except Exception as exc:
                failed[name] = str(exc)
    return {"completed": completed, "failed": failed}


if __name__ == "__main__":
    print(run_parallel())

