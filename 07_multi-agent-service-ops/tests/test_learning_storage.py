import json

from shared.learning_storage import PostgresLearningHistory, RedisLearningStore


class FakeRedis:
    def __init__(self) -> None:
        self.values = {}
        self.expirations = {}

    def ping(self) -> bool:
        return True

    def set(self, key: str, value: str, ex: int) -> None:
        self.values[key] = value
        self.expirations[key] = ex

    def get(self, key: str) -> str | None:
        return self.values.get(key)


class FakeCursor:
    def __init__(self) -> None:
        self.query = ""
        self.params = ()

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return None

    def execute(self, query: str, params: tuple) -> None:
        self.query = query
        self.params = params


class FakeConnection:
    def __init__(self, cursor: FakeCursor) -> None:
        self._cursor = cursor

    def __enter__(self):
        return self

    def __exit__(self, *_):
        return None

    def cursor(self) -> FakeCursor:
        return self._cursor


def test_redis_state_round_trip_keeps_ttl() -> None:
    client = FakeRedis()
    store = RedisLearningStore(client=client)

    store.save("run-01", "04_workflow", {"status": "running"})
    loaded = store.load("run-01", "04_workflow")

    assert loaded["state"]["status"] == "running"
    assert client.expirations[store.key("run-01", "04_workflow")] == store.ttl


def test_postgres_history_uses_upsert_and_json() -> None:
    cursor = FakeCursor()
    history = PostgresLearningHistory(connect=lambda _: FakeConnection(cursor))

    output = history.save(
        "run-02",
        "06_langgraph",
        "completed",
        {"agents": ["packing_agent"]},
        {"trace": [{"step": 1}]},
    )

    assert "ON CONFLICT (run_id, unit) DO UPDATE" in cursor.query
    assert json.loads(cursor.params[3])["agents"] == ["packing_agent"]
    assert output["stored_in"] == "postgresql"


def test_postgres_event_is_append_only_audit_record() -> None:
    cursor = FakeCursor()
    history = PostgresLearningHistory(connect=lambda _: FakeConnection(cursor))

    output = history.append_event(
        "run-03",
        "08_approval",
        "human_decision",
        "student-01",
        {"decision": "approve"},
        event_id="event-fixed",
    )

    assert "INSERT INTO learning_events" in cursor.query
    assert "DO UPDATE" not in cursor.query
    assert cursor.params[0] == "event-fixed"
    assert json.loads(cursor.params[5])["decision"] == "approve"
    assert output["event_type"] == "human_decision"
