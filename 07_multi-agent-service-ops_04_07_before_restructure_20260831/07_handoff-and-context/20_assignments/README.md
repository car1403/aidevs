# 07 Assignment

고객 상담 Agent가 환불 검토 Agent에 전달할 Handoff를 설계하세요. 주문 ID·사유만
전달하고 카드번호·전체 대화는 제외하세요.

정상 전달, 다른 사용자 ID, 허용되지 않은 대상 Agent, 최대 횟수 초과 테스트를 각각
작성하세요.

현재 Handoff 상태는 Redis에 저장하고 정상·차단 결과는 모두 PostgreSQL
`learning_events`에 기록하세요. 차단된 요청도 감사 목적으로 삭제하지 않습니다.

