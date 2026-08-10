"""Redis TTL로 자동 만료되는 Agent 대화 상태 예제입니다."""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "09_python-agent-backend"))

from app.repositories.redis_session import RedisSessionStore  # noqa: E402


load_dotenv(ROOT / ".env")
store = RedisSessionStore(
    os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0"),
    int(os.getenv("REDIS_TTL_SECONDS", "1800")),
)
store.set(
    "travel-demo",
    {"current_node": "collect_information", "destination": "부산"},
)
print(store.get("travel-demo"))
print("TTL이 지나면 이 상태는 자동으로 삭제됩니다.")
