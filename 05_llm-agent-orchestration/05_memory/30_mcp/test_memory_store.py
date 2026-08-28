"""MCP 프로토콜 없이 사용자 범위 저장소 규칙만 빠르게 검증합니다."""

import unittest

from memory_store import ScopedMemoryStore


class ScopedMemoryStoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.store = ScopedMemoryStore("student-01")

    def test_upsert_keeps_same_id(self) -> None:
        first = self.store.save("transportation", "대중교통")
        second = self.store.save("transportation", "도보")
        self.assertEqual(first["id"], second["id"])
        self.assertEqual(self.store.list()[0]["value"], "도보")

    def test_sensitive_key_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.store.save("password", "secret")

    def test_only_relevant_memory_is_selected(self) -> None:
        self.store.save("transportation", "대중교통")
        self.store.save("food_restriction", "해산물 알레르기")
        selected = self.store.relevant("식당을 추천해줘")
        self.assertEqual([item["key"] for item in selected], ["food_restriction"])


if __name__ == "__main__":
    unittest.main()
