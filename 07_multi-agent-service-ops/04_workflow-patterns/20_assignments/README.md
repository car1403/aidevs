# 04 Assignment

가족 모임의 장소·음식 조사를 병렬 실행하고, 두 결과가 끝난 뒤 일정 Agent가
실행되는 Workflow를 작성하세요.

장소 조사 실패와 음식 조사 실패를 각각 재현하고, 성공 결과를 보존할지 전체를
실패시킬지 정책을 한 문장으로 작성합니다.

Workflow의 `completed`, `failed`, `join` 결과를 실제 Redis에 저장하고 같은 실행 ID로
다시 읽으세요. 제출물에는 Redis Key 이름과 TTL을 포함합니다.

