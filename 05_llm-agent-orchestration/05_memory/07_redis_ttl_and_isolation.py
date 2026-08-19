"""Redis Session의 사용자 격리, TTL 조회, Sliding TTL 연장을 확인합니다."""

import httpx
from _memory_backend import print_help, request

if __name__ == "__main__":
    try:
        for user, city in (("user-a", "부산"), ("user-b", "제주")):
            request("POST", "/api/memory/sessions", {
                "user_id": user, "session_id": "trip", "state": {"city": city},
            })
        # session_id가 같아도 user_id가 다르면 서로 다른 Redis Key를 조회합니다.
        print("A:", request("GET", "/api/memory/sessions/trip?user_id=user-a"))
        print("B:", request("GET", "/api/memory/sessions/trip?user_id=user-b"))
        print("TTL 연장:", request("GET", "/api/memory/sessions/trip?user_id=user-a&refresh_ttl=true"))
    except httpx.HTTPError as error:
        print_help(error)
