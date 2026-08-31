from shared.contracts import AgentRequest, AgentResult


request = AgentRequest(
    user_id="demo-user",
    message="침대와 냉장고를 포함한 짐 목록을 만들어 주세요.",
)
result = AgentResult(
    agent_name="packing_agent",
    data={"box_count": 20, "large_items": ["침대", "냉장고"]},
)

if __name__ == "__main__":
    print(request.model_dump())
    print(result.model_dump())

