"""Pydantic Structured Output 최소 예제."""

from datetime import date
from pydantic import BaseModel, Field, ValidationError


class ReservationRequest(BaseModel):
    customer_name: str = Field(min_length=1)
    reservation_date: date
    people: int = Field(ge=1, le=20)


def validate_sample(payload: dict) -> None:
    try:
        request = ReservationRequest.model_validate(payload)
        print("검증 성공:", request.model_dump(mode="json"))
    except ValidationError as error:
        print("검증 실패:")
        for item in error.errors():
            print("-", ".".join(map(str, item["loc"])), item["msg"])


if __name__ == "__main__":
    validate_sample(
        {
            "customer_name": "김여행",
            "reservation_date": "2026-08-10",
            "people": 2,
        }
    )
    validate_sample(
        {
            "customer_name": "",
            "reservation_date": "잘못된 날짜",
            "people": 0,
        }
    )
