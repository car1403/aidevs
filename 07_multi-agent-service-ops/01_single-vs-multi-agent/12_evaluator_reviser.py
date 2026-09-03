"""Lab 01-12: Evaluator–Reviser 패턴의 제한된 반복을 확인합니다.

시나리오:
    Writer Agent가 안내 문장을 작성하고 Evaluator Agent가 필수 안전 문구를 검사합니다.
    기준을 통과하지 못하면 Reviser가 문장을 수정한 뒤 다시 평가합니다. 반복 횟수는
    Python이 최대 5회로 제한하며 Evaluator가 통과시키거나 한도에 도달하면 종료합니다.
    기준을 일찍 통과하면 남은 횟수를 모두 실행하지 않고 즉시 종료합니다.

학습 질문:
    생성 Agent와 평가 Agent의 기준을 분리하면 어떤 장점이 있으며, 반복은 누가
    멈춰야 할까요?

범위:
    Evaluator와 Reviser는 실제 LLM을 사용합니다. 필수 문구 최종 판정과 최대 5회
    종료는 Python이 결정적으로 보장합니다.
"""

from shared.travel_llm import run_learning_agent


REQUIRED_TEXT = "승인 전에는 결제를 실행하지 않습니다."


def evaluator_agent(draft: str) -> dict[str, object]:
    llm_result = run_learning_agent("evaluator_agent", "필수 안전 문구 누락 여부를 평가하고 이유를 설명한다.", draft)
    passed = REQUIRED_TEXT in draft
    return {"passed": passed, "feedback": "안전 문구 누락" if not passed else "통과", "agent_result": llm_result}


def reviser_agent(draft: str, feedback: str) -> str:
    llm_result = run_learning_agent("reviser_agent", "평가 의견을 반영해 안전한 문장으로 수정한다.", draft, feedback)
    if llm_result["result"] is not None:
        draft = llm_result["result"]["summary"]
    if feedback == "안전 문구 누락":
        return f"{draft} {REQUIRED_TEXT}"
    return draft


def review_loop_orchestrator_agent(initial_draft: str, max_rounds: int = 5) -> dict[str, object]:
    draft = initial_draft
    trace = []
    for round_number in range(1, max_rounds + 1):
        evaluation = evaluator_agent(draft)
        trace.append({"round": round_number, **evaluation})
        if evaluation["passed"]:
            return {"status": "completed", "draft": draft, "trace": trace}
        draft = reviser_agent(draft, evaluation["feedback"])
    return {"status": "failed", "reason": "max_rounds", "draft": draft, "trace": trace}


if __name__ == "__main__":
    result = review_loop_orchestrator_agent("여행 예약을 도와드립니다.")
    print(result)
    print("반복 완료:", result["status"] == "completed")
    print("필수 문구 포함:", REQUIRED_TEXT in result["draft"])
    print("설정된 최대 반복 횟수:", 5)
    print("통과하면 최대 반복 전에 조기 종료:", len(result["trace"]) < 5)
