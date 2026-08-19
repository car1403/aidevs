"""같은 고객 문의를 Zero-shot과 Few-shot Prompt로 실제 호출해 비교합니다."""

# 방식	예시 제공	의미
# Zero-shot	0개	지시문만 보고 작업 수행
# One-shot	1개	예시 하나를 참고하여 수행
# Few-shot	여러 개	여러 예시의 규칙과 패턴을 참고하여 수행

import httpx

from _llm_backend import generate_text, print_connection_help, print_result


MESSAGE = "배송 조회 화면에서 계속 오류가 발생하고 주문 상태를 볼 수 없습니다."
ZERO_SHOT = "고객 문의를 billing, technical, account, other 중 하나로 분류하세요."
FEW_SHOT = """고객 문의를 billing, technical, account, other 중 하나로 분류하세요.

예시:
- 결제가 두 번 됐어요. → billing
- 비밀번호를 잊었어요. → account
- 화면에서 서버 오류가 발생해요. → technical

분류값과 한 문장 근거만 답하세요."""


if __name__ == "__main__":
    try:
        print_result("Zero-shot", generate_text(ZERO_SHOT, MESSAGE))
        print_result("Few-shot", generate_text(FEW_SHOT, MESSAGE))
    except httpx.HTTPError as error:
        print_connection_help(error)
