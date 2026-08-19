"""Node 오류가 Graph 바깥으로 전달될 때 Provider 설정과 실패 원인을 확인합니다."""

import httpx
from _graph_backend import post, print_help

if __name__ == "__main__":
    try:
        # 준비되지 않은 Provider 호출은 조용히 성공 처리하지 않고 HTTP 오류로 드러냅니다.
        print(post("/api/learning/graph/llm-node", {"message": "테스트", "provider": "openai"}))
    except httpx.HTTPStatusError as error:
        print("예상한 Provider 오류:", error.response.status_code, error.response.text)
        print("Fallback은 LLM_FALLBACK_ENABLED 정책을 명시적으로 켠 경우에만 사용합니다.")
    except httpx.HTTPError as error:
        print_help(error)
