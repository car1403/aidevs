"""여행 선호 중 필요한 정보만 선택해 사용하는 예제."""

from dataclasses import dataclass, asdict


SENSITIVE_KEYS = {"card_number", "password", "passport_number"}


@dataclass
class Preference:
    key: str
    value: str


class TravelMemory:
    def __init__(self) -> None:
        self._users: dict[str, dict[str, str]] = {}

    def save(self, user_id: str, key: str, value: str) -> None:
        if key in SENSITIVE_KEYS:
            raise ValueError("민감정보는 Memory에 저장할 수 없습니다.")
        self._users.setdefault(user_id, {})[key] = value

    def relevant(self, user_id: str, keys: list[str]) -> list[dict]:
        user_memory = self._users.get(user_id, {})
        return [
            asdict(Preference(key, user_memory[key]))
            for key in keys
            if key in user_memory
        ]

    def update(self, user_id: str, key: str, value: str) -> bool:
        if key not in self._users.get(user_id, {}):
            return False
        self.save(user_id, key, value)
        return True

    def delete(self, user_id: str, key: str) -> bool:
        if key not in self._users.get(user_id, {}):
            return False
        del self._users[user_id][key]
        return True


if __name__ == "__main__":
    memory = TravelMemory()
    memory.save("demo-user", "transportation", "대중교통")
    memory.save("demo-user", "food_restriction", "해산물 알레르기")
    memory.save("demo-user", "hotel_preference", "조용한 호텔")
    print(memory.relevant("demo-user", ["transportation", "hotel_preference"]))
