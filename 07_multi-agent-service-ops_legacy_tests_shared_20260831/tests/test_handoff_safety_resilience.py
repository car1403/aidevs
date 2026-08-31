from datetime import date
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load(relative_path: str):
    path = ROOT / relative_path
    spec = spec_from_file_location(path.stem, path)
    module = module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_handoff_rejects_other_user() -> None:
    module = load("07_handoff-and-context/04_handoff_guard.py")
    result = module.guard_handoff(
        {"user_id": "other", "source_agent": "packing_agent", "target_agent": "budget_agent", "hop_count": 1},
        active_user_id="student-01",
    )
    assert result["accepted"] is False


def test_validation_uses_fixed_reference_date() -> None:
    module = load("08_validation-and-human-approval/01_validation_example.py")
    errors = module.validate_plan(
        date(2026, 8, 11),
        500_000,
        700_000,
        reference_date=date(2026, 8, 11),
    )
    assert len(errors) == 2


def test_tool_requires_role_and_approval() -> None:
    module = load("08_validation-and-human-approval/04_tool_allowlist.py")
    assert module.authorize_tool("packing_agent", "create_mock_quote", approved=True)["allowed"] is False
    assert module.authorize_tool("budget_agent", "create_mock_quote", approved=False)["allowed"] is False
    assert module.authorize_tool("budget_agent", "create_mock_quote", approved=True)["allowed"] is True


def test_failed_replan_escalates_to_human() -> None:
    module = load("09_failure-retry-and-fallback/03_replan_and_escalation.py")
    result = module.recover_route(route_error=True, replan_succeeds=False)
    assert result["status"] == "waiting_human"
    assert result["trace"][-1]["action"] == "human_escalation"
