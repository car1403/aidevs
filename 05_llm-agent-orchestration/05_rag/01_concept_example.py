"""외부 패키지 없는 작은 검색·근거 답변 예제."""

from dataclasses import dataclass
import re


@dataclass
class Document:
    id: str
    text: str
    source: str


DOCUMENTS = [
    Document("d1", "예약일 3일 전까지 취소하면 전액 환불됩니다.", "refund-policy.md"),
    Document("d2", "체크인은 오후 3시부터 가능하며 신분 확인이 필요합니다.", "check-in.md"),
    Document("d3", "기내 수하물은 10kg까지 허용됩니다.", "baggage.md"),
]


def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[가-힣A-Za-z0-9]+", text.lower()))


def search(query: str, limit: int = 2) -> list[tuple[Document, float]]:
    query_tokens = tokenize(query)
    scored = []
    for document in DOCUMENTS:
        document_tokens = tokenize(document.text)
        score = len(query_tokens & document_tokens) / max(len(query_tokens), 1)
        if score > 0:
            scored.append((document, score))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:limit]


if __name__ == "__main__":
    for document, score in search("취소하면 환불되나요?"):
        print(f"{document.source} | score={score:.2f} | {document.text}")
