from __future__ import annotations

import json
import os

import httpx

from shared.contracts import AgentResult, RouteDecision
from shared.moving_agents import packing_agent, route_request


SYSTEM_PROMPT = """
이사 준비 요청을 다음 Agent 중 하나 이상으로 분류하세요.
- packing_agent: 짐, 포장, 가구
- budget_agent: 비용, 예산, 견적
- address_agent: 주소 변경, 전입, 우편
반드시 제공된 RouteDecision JSON Schema에 맞는 결과만 반환하세요.
"""


def _prompt(message: str) -> str:
    return f"{SYSTEM_PROMPT}\n사용자 요청: {message}"


def route_with_openai(message: str) -> RouteDecision:
    from openai import OpenAI

    response = OpenAI().responses.parse(
        model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": message},
        ],
        text_format=RouteDecision,
    )
    if response.output_parsed is None:
        raise RuntimeError("OpenAI의 구조화된 Route 결과가 없습니다.")
    return response.output_parsed


def route_with_gemini(message: str) -> RouteDecision:
    from google import genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
        model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        contents=_prompt(message),
        config={
            "response_mime_type": "application/json",
            "response_json_schema": RouteDecision.model_json_schema(),
        },
    )
    if not response.text:
        raise RuntimeError("Gemini의 Route 결과가 없습니다.")
    return RouteDecision.model_validate_json(response.text)


def route_with_ollama(message: str) -> RouteDecision:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11435")
    response = httpx.post(
        f"{base_url}/api/chat",
        json={
            "model": os.getenv("OLLAMA_MODEL", "llama3.2"),
            "messages": [{"role": "user", "content": _prompt(message)}],
            "format": RouteDecision.model_json_schema(),
            "stream": False,
        },
        timeout=60,
    )
    response.raise_for_status()
    content = response.json()["message"]["content"]
    return RouteDecision.model_validate_json(content)


def route_with_provider(provider: str, message: str) -> RouteDecision:
    routers = {
        "mock": route_request,
        "openai": route_with_openai,
        "gemini": route_with_gemini,
        "ollama": route_with_ollama,
    }
    if provider not in routers:
        raise ValueError(f"지원하지 않는 Provider: {provider}")
    return routers[provider](message)


def worker_with_provider(provider: str, message: str) -> AgentResult:
    prompt = (
        "당신은 이사 준비 Packing Agent입니다. 실제 예약이나 결제를 하지 말고 "
        f"교육용 짐 정리 결과를 작성하세요.\n요청: {message}"
    )
    if provider == "mock":
        return packing_agent({})
    if provider == "openai":
        from openai import OpenAI

        response = OpenAI().responses.parse(
            model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
            input=prompt,
            text_format=AgentResult,
        )
        if response.output_parsed is None:
            raise RuntimeError("OpenAI의 구조화된 Worker 결과가 없습니다.")
        return response.output_parsed
    if provider == "gemini":
        from google import genai

        response = genai.Client(api_key=os.environ["GEMINI_API_KEY"]).models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": AgentResult.model_json_schema(),
            },
        )
        if not response.text:
            raise RuntimeError("Gemini의 Worker 결과가 없습니다.")
        return AgentResult.model_validate_json(response.text)
    if provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11435")
        response = httpx.post(
            f"{base_url}/api/chat",
            json={
                "model": os.getenv("OLLAMA_MODEL", "llama3.2"),
                "messages": [{"role": "user", "content": prompt}],
                "format": AgentResult.model_json_schema(),
                "stream": False,
            },
            timeout=60,
        )
        response.raise_for_status()
        return AgentResult.model_validate_json(response.json()["message"]["content"])
    raise ValueError(f"지원하지 않는 Provider: {provider}")


def pretty_route(provider: str, message: str) -> str:
    return json.dumps(
        route_with_provider(provider, message).model_dump(),
        ensure_ascii=False,
        indent=2,
    )
