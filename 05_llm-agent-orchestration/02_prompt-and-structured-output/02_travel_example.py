"""여행 요청의 구조화 결과를 검증하는 예제."""

from datetime import date
from typing import Literal
from pydantic import BaseModel, Field, model_validator


class TravelRequest(BaseModel):
    destination: str = Field(min_length=1)
    start_date: date
    nights: int = Field(ge=1, le=30)
    adults: int = Field(ge=1, le=20)
    budget: int = Field(gt=0)
    transportation: Literal["public", "car", "flight", "unknown"] = "unknown"
    missing_fields: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def start_date_must_be_valid(self) -> "TravelRequest":
        if self.start_date.year < 2026:
            raise ValueError("교육 예제에서는 2026년 이후 날짜를 사용하세요.")
        return self


MOCK_LLM_OUTPUT = {
    "destination": "부산",
    "start_date": "2026-08-10",
    "nights": 2,
    "adults": 2,
    "budget": 500000,
    "transportation": "public",
    "missing_fields": [],
}


if __name__ == "__main__":
    request = TravelRequest.model_validate(MOCK_LLM_OUTPUT)
    print(request.model_dump_json(indent=2))
