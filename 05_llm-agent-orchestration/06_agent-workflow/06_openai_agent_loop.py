"""OpenAI Responses API로 실제 LLM 기반 Multi-Tool Agent Loop를 실행합니다."""

import json
import sys

from openai_agent_backend import run_openai_agent


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "제주 날씨에 맞는 장소를 추천해 줘."
    result = run_openai_agent(question)
    print(json.dumps(result, ensure_ascii=False, indent=2))
