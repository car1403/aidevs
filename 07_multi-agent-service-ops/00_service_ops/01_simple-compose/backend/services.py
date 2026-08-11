from __future__ import annotations

import json
import os
from typing import Any

import psycopg
import redis
from psycopg.rows import dict_row


class RedisSessionStore:
    """짧게 유지할 현재 대화와 통계를 Redis에 저장합니다."""

    def __init__(self, url: str | None = None, ttl_seconds: int = 1800) -> None:
        self.client = redis.from_url(
            url or os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
            decode_responses=True,
        )
        self.ttl_seconds = ttl_seconds

    def ping(self) -> bool:
        return bool(self.client.ping())

    def record_request(self, text: str) -> int:
        count = int(self.client.incr("service_ops:request_count"))
        self.client.set("service_ops:recent_request", text, ex=self.ttl_seconds)
        return count

    def stats(self) -> dict[str, Any]:
        return {
            "request_count": int(self.client.get("service_ops:request_count") or 0),
            "recent_request": self.client.get("service_ops:recent_request"),
        }

    def load_session(self, session_id: str) -> list[dict[str, str]]:
        key = f"service_ops:session:{session_id}"
        return [json.loads(item) for item in self.client.lrange(key, 0, -1)]

    def append_session(self, session_id: str, messages: list[dict[str, str]]) -> None:
        key = f"service_ops:session:{session_id}"
        if messages:
            self.client.rpush(key, *[json.dumps(item, ensure_ascii=False) for item in messages])
        self.client.ltrim(key, -12, -1)
        self.client.expire(key, self.ttl_seconds)

    def clear_session(self, session_id: str) -> None:
        self.client.delete(f"service_ops:session:{session_id}")


class PostgresRepository:
    """사라지면 안 되는 메모와 전체 Chat 이력을 PostgreSQL에 저장합니다."""

    def __init__(self, url: str | None = None) -> None:
        self.url = url or os.getenv(
            "DATABASE_URL",
            "postgresql://service_ops:service_ops@127.0.0.1:5432/service_ops",
        )

    def ping(self) -> bool:
        with psycopg.connect(self.url) as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                return cursor.fetchone() == (1,)

    def add_note(self, name: str, message: str) -> dict[str, Any]:
        with psycopg.connect(self.url, row_factory=dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO notes (name, message)
                    VALUES (%s, %s)
                    RETURNING id, name, message, created_at
                    """,
                    (name, message),
                )
                return dict(cursor.fetchone())

    def list_notes(self, limit: int = 50) -> list[dict[str, Any]]:
        with psycopg.connect(self.url, row_factory=dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, name, message, created_at
                    FROM notes ORDER BY id DESC LIMIT %s
                    """,
                    (limit,),
                )
                return [dict(row) for row in cursor.fetchall()]

    def add_chat_message(self, session_id: str, role: str, content: str) -> dict[str, Any]:
        with psycopg.connect(self.url, row_factory=dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO chat_messages (session_id, role, content)
                    VALUES (%s, %s, %s)
                    RETURNING id, session_id, role, content, created_at
                    """,
                    (session_id, role, content),
                )
                return dict(cursor.fetchone())

    def list_chat(self, session_id: str, limit: int = 100) -> list[dict[str, Any]]:
        with psycopg.connect(self.url, row_factory=dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, session_id, role, content, created_at
                    FROM chat_messages
                    WHERE session_id = %s
                    ORDER BY id ASC LIMIT %s
                    """,
                    (session_id, limit),
                )
                return [dict(row) for row in cursor.fetchall()]


class GeminiChatService:
    """Backend에서 Gemini API를 호출합니다. API Key는 코드에 저장하지 않습니다."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", "")
        self.model = model or os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

    @property
    def configured(self) -> bool:
        return bool(self.api_key)

    def reply(self, message: str, recent_messages: list[dict[str, str]]) -> str:
        if not self.configured:
            raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다.")

        from google import genai

        history_text = "\n".join(
            f"{item['role']}: {item['content']}" for item in recent_messages[-6:]
        )
        prompt = f"""
당신은 초보자용 이사 준비 도우미입니다.
실제 예약이나 결제를 수행하지 말고, 짧고 안전한 준비 조언만 제공하세요.

최근 대화:
{history_text or '(첫 대화)'}

사용자 질문: {message}
""".strip()
        response = genai.Client(api_key=self.api_key).models.generate_content(
            model=self.model,
            contents=prompt,
        )
        if not response.text:
            raise RuntimeError("Gemini가 텍스트 응답을 반환하지 않았습니다.")
        return response.text
