"""모든 Scenario를 다시 실행해 이전 안전 행동이 유지되는지 확인합니다."""

import json

from evaluation import run_suite


report = run_suite()
summary = {key: report[key] for key in ("total", "passed", "failed", "pass_rate", "safety_gate")}
print("평가 요약:", json.dumps(summary, ensure_ascii=False, indent=2))
for result in report["results"]:
    mark = "PASS" if result["passed"] else "FAIL"
    print(f"[{mark}] {result['scenario']} · {result['failed_checks']}")
