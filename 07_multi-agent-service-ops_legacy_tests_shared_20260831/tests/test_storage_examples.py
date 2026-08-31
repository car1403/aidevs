from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT = Path(__file__).parents[1]


def load_script(name: str, relative_path: str):
    spec = spec_from_file_location(name, ROOT / relative_path)
    module = module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeLiveStore:
    def __init__(self) -> None:
        self.values = {}

    def ping(self) -> bool:
        return True

    def save(self, run_id: str, unit: str, state: dict) -> dict:
        snapshot = {"run_id": run_id, "unit": unit, "state": state.copy()}
        self.values[(run_id, unit)] = snapshot
        return snapshot

    def load(self, run_id: str, unit: str) -> dict | None:
        return self.values.get((run_id, unit))


class FakeHistory:
    def save(self, run_id: str, unit: str, status: str, payload: dict, result: dict) -> dict:
        return {"run_id": run_id, "unit": unit, "status": status, "stored_in": "postgresql"}

    def append_event(
        self,
        run_id: str,
        unit: str,
        event_type: str,
        actor: str,
        payload: dict,
    ) -> dict:
        return {"run_id": run_id, "unit": unit, "event_type": event_type, "stored_in": "postgresql"}


def test_04_real_redis_example_boundary() -> None:
    module = load_script("workflow_redis", "04_workflow-patterns/05_redis_workflow_state.py")
    output = module.run(FakeLiveStore())

    assert output["redis_connected"] is True
    assert output["loaded"]["state"]["status"] == "completed"


def test_05_redis_orchestration_restores_last_state() -> None:
    module = load_script("orchestration_redis", "05_agent-orchestration/06_redis_orchestration_state.py")
    output = module.run(["packing_agent", "budget_agent"], FakeLiveStore())

    assert output["restored_state"]["state"]["completed"] == ["packing_agent", "budget_agent"]
    assert output["restored_state"]["state"]["remaining"] == []


def test_06_graph_splits_live_and_permanent_storage() -> None:
    module = load_script("graph_storage", "06_langgraph-multi-agent/05_redis_postgres_run.py")
    output = module.run(FakeLiveStore(), FakeHistory())

    assert output["redis_state"]["state"]["status"] == "completed"
    assert output["postgres_history"]["stored_in"] == "postgresql"


def test_07_handoff_splits_current_state_and_audit_event() -> None:
    module = load_script("handoff_storage", "07_handoff-and-context/05_persist_handoff.py")
    output = module.run(FakeLiveStore(), FakeHistory())

    assert output["redis_state"]["state"]["status"] == "accepted"
    assert output["postgres_event"]["event_type"] == "agent_handoff"


def test_08_approval_keeps_waiting_and_final_states_distinct() -> None:
    module = load_script("approval_storage", "08_validation-and-human-approval/05_persist_approval.py")
    output = module.run("edit", FakeLiveStore(), FakeHistory())

    assert output["pending"]["state"]["status"] == "waiting_approval"
    assert output["current"]["state"]["status"] == "needs_revision"
    assert output["postgres_event"]["event_type"] == "human_decision"


def test_09_recovery_appends_every_trace_event() -> None:
    module = load_script("recovery_storage", "09_failure-retry-and-fallback/05_persist_recovery_trace.py")
    output = module.run(FakeLiveStore(), FakeHistory())

    assert output["redis_state"]["state"]["status"] == "completed"
    assert [event["event_type"] for event in output["postgres_events"]] == ["tool_call", "retry"]
