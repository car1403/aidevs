from shared.contracts import TaskRecord, TaskStatus
from shared.orchestrator import run_moving_orchestration


def test_moving_orchestration_completes() -> None:
    task = TaskRecord(
        user_id="demo-user",
        message="짐 목록과 이사 비용을 계산해 주세요.",
    )
    result = run_moving_orchestration(task)
    assert result.status == TaskStatus.COMPLETED
    assert "packing_agent" in result.completed_agents
    assert "budget_agent" in result.completed_agents
    assert any(item["event_type"] == "agent_handoff" for item in result.trace)


def test_moving_orchestration_stops_at_limit() -> None:
    task = TaskRecord(user_id="demo-user", message="이사 비용을 계산해 주세요.")
    result = run_moving_orchestration(task, max_steps=1)
    assert result.status == TaskStatus.FAILED
    assert "최대 Orchestration" in (result.error or "")


def test_vague_request_waits_for_input() -> None:
    task = TaskRecord(user_id="demo-user", message="이사를 도와주세요.")
    result = run_moving_orchestration(task)
    assert result.status == TaskStatus.WAITING_INPUT
    assert result.result["route"]["missing_information"]
