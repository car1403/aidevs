# 11 Assignment

`POST /api/tasks/{task_id}/input`에 허용 Context 필드 목록과 사용자 ID 검사를
추가하고 정상·다른 상태·허용되지 않은 필드 테스트를 작성하세요.

같은 테스트를 Memory Repository와 Redis Repository에 적용할 수 있도록 저장소 계약을
분리하세요.

Task 승인·거절·취소를 PostgreSQL `task_events`에 기록하고 `/history` API를 추가하세요.
Redis의 현재 상태와 PostgreSQL의 마지막 영구 상태가 다를 때 이를 숨기지 않습니다.
