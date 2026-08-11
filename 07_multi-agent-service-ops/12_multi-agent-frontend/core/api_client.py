"""과정의 11_multi-agent-backend API를 호출합니다.

Backend를 Port 8100으로 먼저 실행합니다. 다른 주소는 MULTI_AGENT_API_URL로 지정하며,
Mini 프로젝트 Backend는 API·Queue 계약이 다르므로 연결하지 않습니다.
"""

import os

import httpx


BASE_URL = os.getenv("MULTI_AGENT_API_URL", "http://127.0.0.1:8100")


def request(method: str, path: str, **kwargs):
    try:
        response = httpx.request(method, f"{BASE_URL}{path}", timeout=15, **kwargs)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as exc:
        try:
            detail = exc.response.json().get("detail", exc.response.text)
        except ValueError:
            detail = exc.response.text
        raise RuntimeError(detail) from exc
    except httpx.RequestError as exc:
        raise RuntimeError(f"Backend 연결 실패: {exc}") from exc


def create_task(payload: dict) -> dict:
    return request("POST", "/api/tasks", json=payload)


def get_task(task_id: str) -> dict:
    return request("GET", f"/api/tasks/{task_id}")


def list_tasks() -> list[dict]:
    return request("GET", "/api/tasks")


def get_history(task_id: str) -> dict:
    return request("GET", f"/api/tasks/{task_id}/history")


def health() -> dict:
    return request("GET", "/health")


def action(task_id: str, name: str) -> dict:
    return request("POST", f"/api/tasks/{task_id}/{name}")


def submit_input(task_id: str, values: dict) -> dict:
    return request(
        "POST",
        f"/api/tasks/{task_id}/input",
        json={"values": values},
    )
