import asyncio
import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).parents[1]
SERVICE_ROOT = ROOT / "08_multi-ai-agent-service"
FINAL_ROOT = ROOT / "09_integrated-travel-multi-ai-agent"
sys.path.insert(0, str(SERVICE_ROOT))
sys.path.insert(0, str(FINAL_ROOT))

from app.models import TaskRecord  # noqa: E402
import integrated_orchestrator as integrated  # noqa: E402
from shared.travel_contracts import SpecialistResult  # noqa: E402


def load_mcp_server():
    spec = importlib.util.spec_from_file_location("travel_mcp_server", FINAL_ROOT / "mcp_server.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


class FakeHttpClient:
    def __init__(self, *args, **kwargs):
        pass

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        return None

    async def get(self, url, params):
        if "geocoding" in url:
            return FakeResponse(
                {"results": [{"name": "부산", "country": "대한민국", "latitude": 35.18, "longitude": 129.07, "timezone": "Asia/Seoul"}]}
            )
        return FakeResponse(
            {"daily": {"time": ["2026-09-01"], "temperature_2m_max": [27], "temperature_2m_min": [21], "precipitation_probability_max": [30]}}
        )


def specialist(agent_id: str) -> SpecialistResult:
    return SpecialistResult(
        agent_id=agent_id,
        goal="여행 작업",
        summary=f"{agent_id} 완료, 알레르기와 대중교통, 예산 60만원 반영",
        recommendations=["추천"],
        completed=True,
    )


def test_mcp_weather_tool_uses_geocoding_and_forecast(monkeypatch) -> None:
    module = load_mcp_server()
    monkeypatch.setattr(module.httpx, "AsyncClient", FakeHttpClient)
    output = asyncio.run(module.get_weather("부산", 3))
    assert output["source"] == "Open-Meteo"
    assert output["location"]["name"] == "부산"
    assert output["daily"]["temperature_2m_max"] == [27]


def test_integrated_orchestrator_connects_mcp_handoff_and_evaluation(monkeypatch) -> None:
    async def fake_tool(name, arguments):
        assert name == "get_weather"
        return {"source": "Open-Meteo", "daily": {"time": ["2026-09-01"]}}

    monkeypatch.setattr(integrated, "call_travel_tool", fake_tool)
    monkeypatch.setattr(
        integrated,
        "extract_intent",
        lambda task: integrated.TripIntent(
            destination="부산",
            days=3,
            constraints=["알레르기", "대중교통", "60만원"],
        ),
    )
    monkeypatch.setattr(
        integrated,
        "run_specialist",
        lambda task, agent_id, extra_context=None: specialist(agent_id),
    )
    monkeypatch.setattr(
        integrated,
        "run_structured",
        lambda provider, prompt, schema: specialist("itinerary_agent"),
    )
    task = TaskRecord(
        user_id="user-1",
        request="부산 2박 3일, 해산물 알레르기, 대중교통, 예산 60만원 여행",
    )

    result = asyncio.run(integrated.run_integrated(task))

    assert result.status == "waiting_approval"
    assert result.result["mcp"]["source"] == "Open-Meteo"
    assert len(result.result["handoffs"]) == 3
    assert result.result["evaluation"]["passed"] is True
    assert any(item["action"] == "mcp:get_weather" for item in result.trace)
