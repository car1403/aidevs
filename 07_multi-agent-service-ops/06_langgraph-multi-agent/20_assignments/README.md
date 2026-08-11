# 06 Assignment

가족 모임 준비를 장소·음식 Agent와 최종 일정 Agent로 구성한 Graph로
변환하세요. 장소와 음식 결과가 모두 있어야 최종 일정으로 이동해야 합니다.

일반 Python 버전도 함께 작성하고 입력, Agent 순서, 최종 결과가 같은지 비교합니다.
Graph 버전에만 `recursion_limit`과 명시적인 END 조건을 추가합니다.

Graph 실행 중 상태는 Redis에, 완료 결과와 Trace는 PostgreSQL에 저장하세요. 두 저장소
중 하나가 실패하면 성공으로 표시하지 말고 어느 저장소가 실패했는지 기록합니다.

