from __future__ import annotations

import os
from time import perf_counter
from typing import TypeVar

import httpx
from dotenv import load_dotenv
from pydantic import BaseModel


load_dotenv()
T = TypeVar("T", bound=BaseModel)
SUPPORTED_PROVIDERS = ("openai", "gemini", "ollama")


def provider_model(provider: str) -> str:
    models = {
        "openai": os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
        "gemini": os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
        "ollama": os.getenv("OLLAMA_MODEL", "llama3.2"),
    }
    if provider not in models:
        raise ValueError(f"지원하지 않는 Provider입니다: {provider}")
    return models[provider]


def run_structured(provider: str, prompt: str, schema: type[T]) -> T:
    """같은 Pydantic 계약을 실제 OpenAI·Gemini·Ollama 요청으로 변환합니다."""
    model = provider_model(provider)
    if provider == "openai":
        from openai import OpenAI

        response = OpenAI().responses.parse(model=model, input=prompt, text_format=schema)
        if response.output_parsed is None:
            raise RuntimeError("OpenAI가 구조화된 결과를 반환하지 않았습니다.")
        return response.output_parsed
    if provider == "gemini":
        from google import genai

        response = genai.Client(api_key=os.environ["GEMINI_API_KEY"]).models.generate_content(
            model=model,
            contents=prompt,
            config={
                "response_mime_type": "application/json",
                "response_json_schema": schema.model_json_schema(),
            },
        )
        if not response.text:
            raise RuntimeError("Gemini가 구조화된 결과를 반환하지 않았습니다.")
        return schema.model_validate_json(response.text)
    if provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11435").rstrip("/")
        response = httpx.post(
            f"{base_url}/api/chat",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "format": schema.model_json_schema(),
                "stream": False,
            },
            timeout=90,
        )
        response.raise_for_status()
        return schema.model_validate_json(response.json()["message"]["content"])
    raise ValueError(f"지원하지 않는 Provider입니다: {provider}")


def run_with_metadata(provider: str, prompt: str, schema: type[T]) -> dict:
    started = perf_counter()
    try:
        result = run_structured(provider, prompt, schema)
        return {
            "provider_requested": provider,
            "provider_used": provider,
            "model": provider_model(provider),
            "fallback_used": False,
            "latency_ms": round((perf_counter() - started) * 1000, 2),
            "result": result.model_dump(),
            "error": None,
        }
    except Exception as error:
        return {
            "provider_requested": provider,
            "provider_used": None,
            "model": provider_model(provider),
            "fallback_used": False,
            "latency_ms": round((perf_counter() - started) * 1000, 2),
            "result": None,
            "error": f"{type(error).__name__}: {error}",
        }
