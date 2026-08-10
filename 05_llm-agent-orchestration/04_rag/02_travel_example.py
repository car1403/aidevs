"""여행 정책 검색 결과가 있을 때만 답하는 Mock RAG."""

from dataclasses import asdict, dataclass
import json
import re


@dataclass
class Policy:
    title: str
    content: str
    source: str


POLICIES = [
    Policy("숙소 취소", "체크인 3일 전까지 취소하면 전액 환불됩니다.", "hotel-refund.md"),
    Policy("당일 취소", "체크인 당일 취소는 숙박 요금의 100%가 부과됩니다.", "hotel-refund.md"),
    Policy("수하물", "국내선 위탁 수하물 기본 허용량은 교육용 예제에서 15kg입니다.", "baggage.md"),
    Policy("관광지", "바다 박물관은 매주 월요일 휴관합니다.", "attraction-hours.md"),
]


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[가-힣A-Za-z0-9]+", text.lower()))


def retrieve(question: str) -> list[dict]:
    query = tokens(question)
    results = []
    for policy in POLICIES:
        score = len(query & tokens(policy.title + " " + policy.content)) / max(len(query), 1)
        if score:
            results.append({**asdict(policy), "score": round(score, 3)})
    return sorted(results, key=lambda item: item["score"], reverse=True)[:2]


def answer(question: str) -> dict:
    documents = retrieve(question)
    if not documents:
        return {
            "answer": "등록된 정책 문서에서 근거를 찾지 못했습니다.",
            "grounded": False,
            "sources": [],
        }
    return {
        "answer": documents[0]["content"],
        "grounded": True,
        "sources": [{"source": item["source"], "score": item["score"]} for item in documents],
    }


if __name__ == "__main__":
    print(json.dumps(answer("숙소를 당일 취소하면 환불되나요?"), ensure_ascii=False, indent=2))
    print(json.dumps(answer("여권을 잃어버리면 어떻게 하나요?"), ensure_ascii=False, indent=2))
