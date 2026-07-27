"""PostgreSQL에 사용자 장기 선호를 저장·조회·삭제합니다."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "10_python-agent-backend"))

from app.repositories.postgres_store import PostgresStore  # noqa: E402


load_dotenv(ROOT / ".env")
store = PostgresStore(os.environ["DATABASE_URL"])
created = store.add_memory("student-01", "transportation", "대중교통")
print("저장:", created)
print("조회:", store.list_memories("student-01"))
print("삭제:", store.delete_memory("student-01", created["id"]))
