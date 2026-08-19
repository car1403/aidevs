# 02 Assignment · 병원 예약 요청 Schema

병원 예약 요청을 위한 Prompt, Pydantic Schema와 검증 프로그램을 작성하세요.

Prompt 요구사항:

- Role, Instruction, Context, Constraint를 분리합니다.
- 사용자 입력은 명확한 구분자 안에 넣습니다.
- Zero-shot Prompt와 가상 예시 2개를 포함한 Few-shot Prompt를 각각 작성합니다.
- 두 Prompt의 결과 차이를 기록합니다.

필수 필드:

- 환자 식별용 별칭
- 희망 날짜
- 진료과
- 증상 요약
- 초진 여부
- 연락 방법

제출물:

1. Zero-shot·Few-shot Prompt
2. 실제 또는 Mock 호출 결과 비교
3. Pydantic 모델
4. 정상 입력 1개
5. 누락 입력 1개
6. 잘못된 타입 또는 범위 입력 1개
7. ValidationError를 사용자가 이해할 문장으로 바꾸는 함수

실제 주민등록번호, 전화번호, 병력처럼 민감한 의료정보는 교육 예제에 사용하지
않습니다. 가상의 값만 사용하고, LLM 출력은 의료 진단으로 사용하지 않습니다.
