"""Safe Order Agent의 저장된 실행 결과 하나를 PASS 또는 FAIL로 평가합니다."""

import json

from evaluation import evaluate, load_suite


scenarios, fixtures = load_suite()
scenario = scenarios[0]
actual = fixtures[scenario["name"]]
print(json.dumps(evaluate(scenario, actual), ensure_ascii=False, indent=2))
