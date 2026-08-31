"""Tool 수가 아니라 독립 Goal·Context·권한·평가 기준으로 Agent 분리를 판단합니다."""


criteria = {
    "single_ai_agent": [
        "사용자 Goal이 하나다",
        "같은 Context와 Tool 권한을 사용한다",
        "하나의 완료·평가 기준으로 충분하다",
    ],
    "multi_ai_agent": [
        "독립적인 전문 Goal이 있다",
        "Context 또는 Tool 권한을 격리해야 한다",
        "Agent별 완료·평가 기준이 다르다",
        "결과를 병렬로 만들거나 Handoff해야 한다",
    ],
}

print("판단 기준:", criteria)
print("여행 서비스 결정: Weather·Place·Budget는 독립 결과와 평가 기준이 있어 분리를 검토합니다.")
print("주의: Agent가 여러 개 존재해도 선택·전달·종료를 연결하지 않으면 Orchestration은 아닙니다.")
