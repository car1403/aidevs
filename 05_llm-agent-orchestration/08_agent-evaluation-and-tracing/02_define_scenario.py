"""입력 문장보다 기대 상태와 행동을 평가 Scenario로 정의합니다."""

import json

from evaluation import load_suite


scenarios, _ = load_suite()
print(json.dumps(scenarios[0], ensure_ascii=False, indent=2))
