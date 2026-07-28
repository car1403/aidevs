ALLOWED_BUDGET_FIELDS = {"estimated_volume_m3", "large_items", "distance_km"}


def filter_context(context: dict) -> dict:
    return {key: value for key, value in context.items() if key in ALLOWED_BUDGET_FIELDS}


if __name__ == "__main__":
    raw = {
        "estimated_volume_m3": 12.5,
        "large_items": ["침대"],
        "distance_km": 15,
        "openai_api_key": "절대 전달하면 안 되는 값",
        "full_conversation": "불필요한 전체 대화",
    }
    print(filter_context(raw))

