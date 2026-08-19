"""Redis WATCH/MULTI와 version으로 Session의 덮어쓰기 충돌을 방지합니다."""

import httpx
from _memory_backend import print_help, request

if __name__ == "__main__":
    try:
        request("POST", "/api/memory/sessions", {
            "user_id": "user-a", "session_id": "atomic", "state": {"city": "부산"},
        })
        updated = request("PATCH", "/api/memory/sessions", {
            "user_id": "user-a", "session_id": "atomic",
            "changes": {"guests": 2}, "expected_version": 0,
        })
        print("정상 갱신:", updated)
        # 같은 version으로 다시 쓰면 HTTP 409가 되어 최신 상태를 덮어쓰지 않습니다.
        request("PATCH", "/api/memory/sessions", {
            "user_id": "user-a", "session_id": "atomic",
            "changes": {"guests": 4}, "expected_version": 0,
        })
    except httpx.HTTPStatusError as error:
        print("예상한 충돌:", error.response.status_code, error.response.text)
    except httpx.HTTPError as error:
        print_help(error)
