"""앞선 개념을 결합한 실제 OpenAI 기반 AI Agent Loop의 실행 진입점입니다.

이 장은 고정 Workflow, 조건 분기, State 기반 반복, Tool Result routing, LLM의 Tool
선택을 차례로 학습했습니다. 이번 파일은 이 요소들을 결합한 최종 필수 예제로,
OpenAI 모델이 목표와 Tool Result를 보고 다음 행동 또는 최종 답변을 결정합니다.

실행 흐름
---------
사용자 질문 → LLM 판단 → Tool Call → backend의 검증과 Tool 실행 → Tool Result 전달
→ LLM 재판단 → 추가 Tool Call 또는 최종 답변

이번 파일 자체는 명령행 질문을 읽고 ``run_openai_agent``를 호출하여 결과를 출력하는
얇은 진입점입니다. Agent의 지침, Tool Schema, OpenAI 호출, 반복, State, 오류 처리와
종료 조건의 실제 구현은 ``openai_agent_backend.py``에 있습니다. 따라서 두 파일을
합쳐서 이 장의 LLM 기반 Tool-using AI Agent 구현으로 이해합니다.
"""

import json
import sys

from openai_agent_backend import run_openai_agent


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "제주 날씨에 맞는 장소를 추천해 줘."
    result = run_openai_agent(question)
    print(json.dumps(result, ensure_ascii=False, indent=2))
