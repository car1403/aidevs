from shared.providers import compare_providers, route_with_metadata, worker_with_metadata


def test_mock_worker_exposes_provider_metadata() -> None:
    output = worker_with_metadata("mock", "이사 짐 목록을 만들어 주세요.")

    assert output["provider_requested"] == "mock"
    assert output["provider_used"] == "mock"
    assert output["model"] == "deterministic-mock"
    assert output["fallback_used"] is False
    assert output["latency_ms"] >= 0


def test_mock_router_uses_same_metadata_shape() -> None:
    output = route_with_metadata("mock", "짐과 비용을 알려 주세요.")

    assert output["result"]["selected_agents"]
    assert output["provider_used"] == "mock"
    assert output["fallback_used"] is False


def test_compare_records_unknown_provider_error() -> None:
    output = compare_providers("worker", ["mock", "unknown"], "짐을 정리해 주세요.")

    assert output[0]["provider_used"] == "mock"
    assert "error" in output[1]
