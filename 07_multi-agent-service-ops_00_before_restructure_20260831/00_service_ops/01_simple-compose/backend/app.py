from functools import lru_cache
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

from services import GeminiChatService, PostgresRepository, RedisSessionStore


app = FastAPI(title="Gemini Service Ops Backend", version="1.0.0")


class NoteRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    message: str = Field(min_length=1, max_length=500)


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100, pattern=r"^[a-zA-Z0-9_-]+$")
    message: str = Field(min_length=1, max_length=2000)


@lru_cache
def get_redis_store() -> RedisSessionStore:
    return RedisSessionStore()


@lru_cache
def get_database() -> PostgresRepository:
    return PostgresRepository()


@lru_cache
def get_gemini() -> GeminiChatService:
    return GeminiChatService()


RedisDep = Annotated[RedisSessionStore, Depends(get_redis_store)]
DatabaseDep = Annotated[PostgresRepository, Depends(get_database)]
GeminiDep = Annotated[GeminiChatService, Depends(get_gemini)]


@app.get("/health/live")
def live() -> dict:
    """Backend Python process만 확인하는 Docker Healthcheck입니다."""
    return {"status": "ok", "service": "backend"}


@app.get("/health")
def health(redis_store: RedisDep, database: DatabaseDep, gemini: GeminiDep) -> dict:
    checks: dict[str, object] = {
        "backend": True,
        "redis": False,
        "database": False,
        "gemini_configured": gemini.configured,
        "gemini_model": gemini.model,
    }
    errors = {}
    try:
        checks["redis"] = redis_store.ping()
    except Exception as exc:
        errors["redis"] = f"{type(exc).__name__}: {exc}"
    try:
        checks["database"] = database.ping()
    except Exception as exc:
        errors["database"] = f"{type(exc).__name__}: {exc}"
    return {
        "status": "ok" if checks["redis"] and checks["database"] else "degraded",
        "checks": checks,
        "errors": errors,
    }


@app.post("/api/notes", status_code=201)
def create_note(payload: NoteRequest, redis_store: RedisDep, database: DatabaseDep) -> dict:
    try:
        note = database.add_note(payload.name, payload.message)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"PostgreSQL 연결 실패: {exc}") from exc
    warning = None
    request_count = None
    try:
        request_count = redis_store.record_request(payload.message)
    except Exception as exc:
        warning = f"메모는 저장했지만 Redis 통계 기록에 실패했습니다: {exc}"
    return {"note": note, "request_count": request_count, "warning": warning}


@app.get("/api/notes")
def get_notes(database: DatabaseDep) -> dict:
    try:
        return {"notes": database.list_notes()}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"PostgreSQL 연결 실패: {exc}") from exc


@app.get("/api/stats")
def get_stats(redis_store: RedisDep) -> dict:
    try:
        return redis_store.stats()
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Redis 연결 실패: {exc}") from exc


@app.post("/api/chat")
def chat(
    payload: ChatRequest,
    redis_store: RedisDep,
    database: DatabaseDep,
    gemini: GeminiDep,
) -> dict:
    if not gemini.configured:
        raise HTTPException(
            status_code=503,
            detail="Gemini를 사용할 수 없습니다. GEMINI_API_KEY를 확인하세요.",
        )
    try:
        recent = redis_store.load_session(payload.session_id)
        database.add_chat_message(payload.session_id, "user", payload.message)
        answer = gemini.reply(payload.message, recent)
        database.add_chat_message(payload.session_id, "assistant", answer)
        redis_store.append_session(
            payload.session_id,
            [
                {"role": "user", "content": payload.message},
                {"role": "assistant", "content": answer},
            ],
        )
        request_count = redis_store.record_request(payload.message)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Chat 처리 실패: {exc}") from exc
    return {
        "session_id": payload.session_id,
        "answer": answer,
        "model": gemini.model,
        "request_count": request_count,
    }


@app.get("/api/chat/{session_id}")
def get_chat_history(session_id: str, database: DatabaseDep) -> dict:
    try:
        return {"session_id": session_id, "messages": database.list_chat(session_id)}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"PostgreSQL 연결 실패: {exc}") from exc


@app.delete("/api/sessions/{session_id}")
def reset_current_session(session_id: str, redis_store: RedisDep) -> dict:
    try:
        redis_store.clear_session(session_id)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Redis 연결 실패: {exc}") from exc
    return {
        "session_id": session_id,
        "redis_session_cleared": True,
        "postgres_history_preserved": True,
    }
