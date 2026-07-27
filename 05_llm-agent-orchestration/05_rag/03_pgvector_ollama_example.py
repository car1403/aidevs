"""Docker Ollama embedding을 PostgreSQL/pgvector에 저장하고 검색합니다."""

import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "10_python-agent-backend"))

from app.repositories.vector_store import PgVectorStore  # noqa: E402


load_dotenv(ROOT / ".env")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://agent_user:agent_password@127.0.0.1:5433/agent_db",
)


def embed(text: str) -> list[float]:
    response = httpx.post(
        f"{OLLAMA_BASE_URL}/api/embed",
        json={"model": OLLAMA_MODEL, "input": text},
        timeout=60,
    )
    response.raise_for_status()
    return response.json()["embeddings"][0]


store = PgVectorStore(DATABASE_URL)
documents = [
    ("숙소 취소", "체크인 3일 전까지 취소하면 전액 환불됩니다."),
    ("교통 안내", "부산역에서 해운대까지 지하철을 이용할 수 있습니다."),
]
for title, content in documents:
    store.add(
        collection="travel_documents",
        title=title,
        content=content,
        source="교육용 여행 정책",
        embedding=embed(content),
        embedding_provider="ollama",
        embedding_model=OLLAMA_MODEL,
    )

results = store.search(
    collection="travel_documents",
    embedding=embed("숙소를 취소하면 환불되나요?"),
    embedding_provider="ollama",
    embedding_model=OLLAMA_MODEL,
)
for item in results:
    print(f"{item['score']:.3f} | {item['title']} | {item['content']}")
