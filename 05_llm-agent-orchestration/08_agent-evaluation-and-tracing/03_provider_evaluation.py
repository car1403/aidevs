"""동일한 Tool 시나리오를 GPT, Gemini, Ollama에 실제 실행합니다."""

import json
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv


load_dotenv()
BASE_URL = os.getenv("PYTHON_AGENT_API_URL", "http://127.0.0.1:8000")

response = httpx.post(
    f"{BASE_URL}/api/evaluations/run",
    json={
        "providers": ["openai", "gemini", "ollama"],
        "scenario_set": "tool_selection",
    },
    timeout=300,
)
response.raise_for_status()
report = response.json()["data"]
print(json.dumps(report, ensure_ascii=False, indent=2))

reports_dir = Path(__file__).parent / "reports"
reports_dir.mkdir(exist_ok=True)
(reports_dir / "tool_selection_report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
