def route_company_question(message: str) -> str:
    if "휴가" in message or "근태" in message:
        return "hr_agent"
    if "노트북" in message or "계정" in message:
        return "it_agent"
    if "영수증" in message or "비용" in message:
        return "finance_agent"
    return "ask_user"


if __name__ == "__main__":
    for question in ["휴가 신청", "노트북 고장", "무엇을 해야 하나요?"]:
        print(question, "->", route_company_question(question))

