import importlib.util
import sys
from pathlib import Path

from fastapi.testclient import TestClient


BACKEND_DIR = (
    Path(__file__).parents[1]
    / "00_service_ops"
    / "01_simple-compose"
    / "backend"
)
sys.path.insert(0, str(BACKEND_DIR))
spec = importlib.util.spec_from_file_location("simple_compose_backend", BACKEND_DIR / "app.py")
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
client = TestClient(module.app)


def test_backend_liveness_does_not_require_external_services() -> None:
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "backend"}


def test_note_validation_rejects_empty_values_before_storage() -> None:
    response = client.post("/api/notes", json={"name": "", "message": ""})
    assert response.status_code == 422
