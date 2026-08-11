from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from types import ModuleType

from shared.contracts import TaskStatus


ROOT = Path(__file__).parents[1]


def load_example(relative_path: str, module_name: str) -> ModuleType:
    spec = spec_from_file_location(module_name, ROOT / relative_path)
    assert spec and spec.loader
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_parallel_failure_preserves_success() -> None:
    example = load_example("04_workflow-patterns/03_partial_failure.py", "partial_failure")
    result = example.run_jobs(
        {
            "address_agent": example.address_agent,
            "cleaning_agent": example.unavailable_cleaning_agent,
        }
    )
    assert "address_agent" in result["completed"]
    assert result["failed"]["cleaning_agent"]["error_type"] == "TimeoutError"


def test_completed_state_cannot_restart() -> None:
    example = load_example("05_agent-orchestration/04_state_transitions.py", "state_transitions")
    try:
        example.transition(TaskStatus.COMPLETED, TaskStatus.RUNNING)
    except ValueError:
        return
    raise AssertionError("완료된 Task가 running으로 다시 전이되었습니다.")


def test_supervisor_worker_graph_stops_at_limit() -> None:
    example = load_example(
        "06_langgraph-multi-agent/03_supervisor_worker_graph.py",
        "supervisor_worker_graph",
    )
    initial = {
        "context": {"box_count": 10},
        "remaining_agents": ["packing_agent", "budget_agent"],
        "current_agent": "",
        "results": {},
        "step_count": 0,
        "max_steps": 1,
        "status": "queued",
    }
    result = example.graph.invoke(initial, config={"recursion_limit": 8})
    assert result["status"] == "failed"
    assert result["remaining_agents"] == ["budget_agent"]
