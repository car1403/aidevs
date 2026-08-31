from typing import Literal

from pydantic import BaseModel, Field


AgentId = Literal["weather_agent", "place_agent", "budget_agent", "itinerary_agent"]


class TravelPlanDraft(BaseModel):
    destination: str
    days: int = Field(ge=1, le=30)
    summary: str
    recommendations: list[str] = Field(min_length=1, max_length=8)
    cautions: list[str] = Field(default_factory=list, max_length=8)


class SpecialistResult(BaseModel):
    agent_id: AgentId
    goal: str
    summary: str
    recommendations: list[str] = Field(min_length=1, max_length=6)
    missing_information: list[str] = Field(default_factory=list, max_length=5)
    completed: bool


class RouteDecision(BaseModel):
    selected_agents: list[AgentId] = Field(min_length=1, max_length=4)
    reason: str
    missing_information: list[str] = Field(default_factory=list, max_length=5)


SPECIALIST_GOALS: dict[AgentId, str] = {
    "weather_agent": "날씨 관점에서 필요한 준비와 확인 항목을 정리한다.",
    "place_agent": "사용자 조건에 맞는 장소 탐색 기준과 후보를 정리한다.",
    "budget_agent": "여행 예산 항목과 계산에 필요한 정보를 정리한다.",
    "itinerary_agent": "검증된 정보를 날짜별 일정 초안으로 구성한다.",
}
