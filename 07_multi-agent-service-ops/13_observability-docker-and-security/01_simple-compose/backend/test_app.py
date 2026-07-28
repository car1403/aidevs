from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "backend"}


def test_message() -> None:
    response = client.post(
        "/api/message",
        json={"name": "홍길동", "message": "이사 준비를 시작합니다."},
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
    assert "홍길동" in response.json()["reply"]

