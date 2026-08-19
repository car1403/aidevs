# 03 Tool Use 실습

Lab 1~2와 6~7은 로컬 Python만 사용합니다. Lab 3~5와 8은 Mini Agent Backend와
실제 Provider가 필요합니다.

## Lab 1. Schema 오류 관찰

`01_tool_schema_validation.py`에 누락 필드, 잘못된 날짜, 추가 인자를 넣고 Pydantic
오류의 `field`, `message`, `type`을 기록합니다.

## Lab 2. 선택과 실행 분리

`02_mock_tool_selection.py`에 날씨·숙소·관광지·일반 대화 문장을 추가합니다. 선택
단계에서는 어떤 Tool 함수도 실행되지 않아야 합니다.

## Lab 3. Tool 설명 Before와 After

`03_tool_description_before_after.py`를 실제 Provider로 실행합니다. 모호한 설명과
명확한 설명에서 Tool 이름과 arguments가 어떻게 달라지는지 기록합니다.

## Lab 4. Tool Choice 모드

Tool이 필요한 질문과 필요하지 않은 질문을 `auto`, `none`, `required`로 실행합니다.
`required`가 불필요한 Tool Call을 만들 수 있는 이유를 설명하세요.

## Lab 5. 누락 정보 재질문

도시·날짜·인원이 없는 요청을 실행합니다. Backend가 임의 기본값을 만들지 않고
`missing_arguments`, `follow_up_question`을 반환하는지 확인합니다.

## Lab 6. 안전한 Tool 실행

`07_safe_tool_execution.py`에 관광지 조회 Tool을 추가하고 Allowlist, Pydantic 검증,
미등록 Tool 차단을 확인합니다.

## Lab 7. Tool Result 기반 답변

`08_tool_result_to_answer.py`의 Tool Result 값을 변경했을 때 최종 답변도 그 값에
따라 바뀌는지 확인합니다. Result에 없는 사실을 추가하면 안 됩니다.

## Lab 8. Provider 비교

`01_multi_provider_tool_calling.py`로 준비된 Provider만 비교합니다. Tool 이름,
arguments, 누락 정보, 지연 시간, 실패 격리를 표로 기록합니다.
