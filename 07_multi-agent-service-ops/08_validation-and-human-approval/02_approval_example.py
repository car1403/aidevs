def create_mock_quote_request(*, approved: bool, plan: dict) -> dict:
    if not approved:
        return {"status": "waiting_approval", "executed": False}
    return {
        "status": "completed",
        "executed": True,
        "draft": {"type": "교육용 견적 요청서", "plan": plan},
    }


if __name__ == "__main__":
    print(create_mock_quote_request(approved=False, plan={"budget": 700_000}))
    print(create_mock_quote_request(approved=True, plan={"budget": 700_000}))

