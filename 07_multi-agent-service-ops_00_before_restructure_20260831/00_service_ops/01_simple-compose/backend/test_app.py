from fastapi.testclient import TestClient

from app import app, get_database, get_gemini, get_redis_store


class FakeRedis:
    def __init__(self) -> None:
        self.count = 0
        self.recent = None
        self.sessions = {}

    def ping(self) -> bool:
        return True

    def record_request(self, text: str) -> int:
        self.count += 1
        self.recent = text
        return self.count

    def stats(self) -> dict:
        return {"request_count": self.count, "recent_request": self.recent}

    def load_session(self, session_id: str) -> list[dict]:
        return list(self.sessions.get(session_id, []))

    def append_session(self, session_id: str, messages: list[dict]) -> None:
        self.sessions.setdefault(session_id, []).extend(messages)

    def clear_session(self, session_id: str) -> None:
        self.sessions.pop(session_id, None)


class FakeDatabase:
    def __init__(self) -> None:
        self.notes = []
        self.messages = []

    def ping(self) -> bool:
        return True

    def add_note(self, name: str, message: str) -> dict:
        note = {"id": len(self.notes) + 1, "name": name, "message": message}
        self.notes.append(note)
        return note

    def list_notes(self, limit: int = 50) -> list[dict]:
        return list(reversed(self.notes))[:limit]

    def add_chat_message(self, session_id: str, role: str, content: str) -> dict:
        item = {"id": len(self.messages) + 1, "session_id": session_id, "role": role, "content": content}
        self.messages.append(item)
        return item

    def list_chat(self, session_id: str, limit: int = 100) -> list[dict]:
        return [item for item in self.messages if item["session_id"] == session_id][:limit]


class FakeGemini:
    configured = True
    model = "gemini-test"

    def reply(self, message: str, recent_messages: list[dict]) -> str:
        return f"교육용 답변: {message}"


class MissingGemini(FakeGemini):
    configured = False


class BrokenRedis(FakeRedis):
    def record_request(self, text: str) -> int:
        raise RuntimeError("redis down")


fake_redis = FakeRedis()
fake_database = FakeDatabase()
app.dependency_overrides[get_redis_store] = lambda: fake_redis
app.dependency_overrides[get_database] = lambda: fake_database
app.dependency_overrides[get_gemini] = lambda: FakeGemini()
client = TestClient(app)


def test_live_and_dependency_health() -> None:
    assert client.get("/health/live").json()["status"] == "ok"
    health = client.get("/health").json()
    assert health["status"] == "ok"
    assert health["checks"]["redis"] is True
    assert health["checks"]["database"] is True


def test_note_round_trip_and_redis_stats() -> None:
    created = client.post(
        "/api/notes",
        json={"name": "홍길동", "message": "냉장고 포장 업체 알아보기"},
    )
    assert created.status_code == 201
    assert created.json()["note"]["name"] == "홍길동"
    assert client.get("/api/notes").json()["notes"][0]["name"] == "홍길동"
    assert client.get("/api/stats").json()["request_count"] >= 1


def test_chat_saves_user_and_assistant_history() -> None:
    response = client.post(
        "/api/chat",
        json={"session_id": "session-01", "message": "상자 준비를 알려줘"},
    )
    assert response.status_code == 200
    assert response.json()["model"] == "gemini-test"
    history = client.get("/api/chat/session-01").json()["messages"]
    assert [item["role"] for item in history] == ["user", "assistant"]


def test_note_is_saved_with_visible_warning_when_redis_is_down() -> None:
    app.dependency_overrides[get_redis_store] = lambda: BrokenRedis()
    try:
        response = client.post(
            "/api/notes",
            json={"name": "김학생", "message": "상자 준비"},
        )
    finally:
        app.dependency_overrides[get_redis_store] = lambda: fake_redis
    assert response.status_code == 201
    assert "Redis" in response.json()["warning"]


def test_missing_gemini_key_is_not_mocked() -> None:
    app.dependency_overrides[get_gemini] = lambda: MissingGemini()
    try:
        response = client.post(
            "/api/chat",
            json={"session_id": "session-02", "message": "질문"},
        )
    finally:
        app.dependency_overrides[get_gemini] = lambda: FakeGemini()
    assert response.status_code == 503
    assert "GEMINI_API_KEY" in response.json()["detail"]


def test_reset_clears_redis_session_but_preserves_database_history() -> None:
    client.post(
        "/api/chat",
        json={"session_id": "session-reset", "message": "기록을 남겨줘"},
    )
    response = client.delete("/api/sessions/session-reset")
    assert response.status_code == 200
    assert response.json()["postgres_history_preserved"] is True
    assert client.get("/api/chat/session-reset").json()["messages"]
