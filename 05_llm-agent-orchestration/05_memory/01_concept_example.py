"""사용자별 Memory CRUD 최소 예제."""

from dataclasses import dataclass, asdict
from uuid import uuid4


@dataclass
class Memory:
    id: str
    user_id: str
    key: str
    value: str


class MemoryStore:
    def __init__(self) -> None:
        self._items: dict[str, Memory] = {}

    def add(self, user_id: str, key: str, value: str) -> Memory:
        item = Memory(str(uuid4()), user_id, key, value)
        self._items[item.id] = item
        return item

    def list_for_user(self, user_id: str) -> list[dict]:
        return [asdict(item) for item in self._items.values() if item.user_id == user_id]

    def delete(self, user_id: str, memory_id: str) -> bool:
        item = self._items.get(memory_id)
        if item is None or item.user_id != user_id:
            return False
        del self._items[memory_id]
        return True


if __name__ == "__main__":
    store = MemoryStore()
    memory = store.add("user-a", "favorite_food", "한식")
    store.add("user-b", "favorite_food", "양식")
    print("user-a:", store.list_for_user("user-a"))
    print("다른 사용자의 삭제 차단:", store.delete("user-b", memory.id))
