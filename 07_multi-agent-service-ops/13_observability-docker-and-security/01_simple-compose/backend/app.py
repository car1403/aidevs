from pydantic import BaseModel, Field
from fastapi import FastAPI


app = FastAPI(title="Simple Compose Backend")


class MessageRequest(BaseModel):
    name: str = Field(min_length=1)
    message: str = Field(min_length=1)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "backend"}


@app.post("/api/message")
def receive_message(payload: MessageRequest) -> dict:
    return {
        "success": True,
        "reply": f"{payload.name}님의 요청을 접수했습니다: {payload.message}",
    }

