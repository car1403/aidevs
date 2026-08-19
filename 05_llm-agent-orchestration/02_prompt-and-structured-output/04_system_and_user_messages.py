"""모든 지시를 User에 넣는 방식과 System·User 역할 분리를 비교합니다."""

import httpx

from _llm_backend import generate_text, print_connection_help, print_result


MEETING = "민수는 금요일까지 API를 완성하기로 했다. 배포일은 다음 회의에서 정한다."
USER_ONLY = f"회의 기록 담당자로서 결정 사항과 할 일을 구분하세요. 회의 내용: {MEETING}"
SYSTEM_PROMPT = """당신은 프로젝트 회의 기록 담당자입니다.
결정 사항과 담당자별 할 일을 분리하고, 확정되지 않은 내용은 결정 사항에서 제외하세요."""


if __name__ == "__main__":
    try:
        print_result(
            "모든 내용을 User Message에 작성",
            generate_text("사용자 요청에 답하세요.", USER_ONLY),
        )
        print_result(
            "System과 User 역할 분리",
            generate_text(SYSTEM_PROMPT, MEETING),
        )
    except httpx.HTTPError as error:
        print_connection_help(error)
