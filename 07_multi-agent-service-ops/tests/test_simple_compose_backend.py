import importlib.util
from pathlib import Path

from fastapi.testclient import TestClient


APP_FILE = (
    Path(__file__).parents[1]
    / "13_observability-docker-and-security"
    / "01_simple-compose"
    / "backend"
    / "app.py"
)
spec = importlib.util.spec_from_file_location("simple_compose_backend", APP_FILE)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
client = TestClient(module.app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "backend"


def test_message_round_trip() -> None:
    response = client.post(
        "/api/message",
        json={"name": "홍길동", "message": "이사 준비를 시작합니다."},
    )
    assert response.status_code == 200
    assert "홍길동" in response.json()["reply"]

