"""HTTP MCP 예제가 사용하는 사용자 범위 Mock Memory 저장소입니다."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from uuid import uuid4


ALLOWED_KEYS = {"transportation", "food_restriction", "hotel_preference"}
SENSITIVE_KEYS = {"password", "card_number", "passport_number", "api_key", "access_token"}


@dataclass
class MemoryItem:
    id: str
    key: str
    value: str


class ScopedMemoryStore:
    """서버가 확인한 한 사용자 범위 안에서만 Memory를 관리합니다."""

    def __init__(self, user_id: str) -> None:
        self.user_id = user_id
        self._items: dict[str, MemoryItem] = {}

    def save(self, key: str, value: str) -> dict:
        if key in SENSITIVE_KEYS or key not in ALLOWED_KEYS:
            raise ValueError("저장이 허용되지 않은 Memory key입니다.")
        current = self._items.get(key)
        item = MemoryItem(id=current.id if current else str(uuid4()), key=key, value=value)
        self._items[key] = item
        return asdict(item)

    def list(self) -> list[dict]:
        return [asdict(item) for item in self._items.values()]

    def delete(self, memory_id: str) -> bool:
        key = next((key for key, item in self._items.items() if item.id == memory_id), None)
        if key is None:
            return False
        del self._items[key]
        return True

    def relevant(self, question: str) -> list[dict]:
        keys: list[str] = []
        if any(word in question for word in ("이동", "교통", "경로")):
            keys.append("transportation")
        if any(word in question for word in ("음식", "식당", "먹")):
            keys.append("food_restriction")
        if any(word in question for word in ("호텔", "숙소")):
            keys.append("hotel_preference")
        return [asdict(self._items[key]) for key in keys if key in self._items]
