"""평가 실행 결과를 PostgreSQL에 저장하고 최근 회귀 여부를 확인합니다.

필요 환경 변수:
    DATABASE_URL=postgresql://agent_user:agent_password@127.0.0.1:5433/agent_db
선택 환경 변수:
    MINI_AGENT_API_URL=http://localhost:8000
"""

import json
import os
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

import psycopg
from psycopg.types.json import Jsonb


DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://agent_user:agent_password@127.0.0.1:5433/agent_db",
)
API_URL = os.getenv("MINI_AGENT_API_URL", "http://localhost:8000")


def run_evaluation(api_url: str) -> dict:
    """Mini Agent의 기본 평가 시나리오 전체를 실행합니다."""
    request = Request(
        f"{api_url.rstrip('/')}/api/evaluations/run",
        data=b'{"scenarios": []}',
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))["data"]


def prepare_table(connection: psycopg.Connection) -> None:
    """요약 열과 상세 JSONB를 함께 보관하는 평가 테이블을 준비합니다."""
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS evaluation_runs (
            id BIGSERIAL PRIMARY KEY,
            created_at TIMESTAMPTZ NOT NULL,
            provider TEXT NOT NULL,
            passed INTEGER NOT NULL,
            failed INTEGER NOT NULL,
            total INTEGER NOT NULL,
            pass_rate DOUBLE PRECISION NOT NULL,
            result JSONB NOT NULL
        )
        """
    )


def save_run(connection: psycopg.Connection, result: dict, provider: str) -> int:
    """집계 조회용 요약과 실패 분석용 전체 결과를 한 실행으로 저장합니다."""
    summary = result["summary"]
    row = connection.execute(
        """
        INSERT INTO evaluation_runs
            (created_at, provider, passed, failed, total, pass_rate, result)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """,
        (
            datetime.now(timezone.utc),
            provider,
            summary["passed"],
            summary["failed"],
            summary["total"],
            summary["pass_rate"],
            Jsonb(result),
        ),
    ).fetchone()
    return int(row[0])


def recent_runs(connection: psycopg.Connection, limit: int = 5) -> list[dict]:
    """최근 실행을 조회하여 직전 통과율보다 낮아졌는지 비교할 수 있게 합니다."""
    rows = connection.execute(
        """
        SELECT id, created_at, provider, passed, failed, total, pass_rate
        FROM evaluation_runs ORDER BY id DESC LIMIT %s
        """,
        (limit,),
    ).fetchall()
    columns = ["id", "created_at", "provider", "passed", "failed", "total", "pass_rate"]
    return [dict(zip(columns, row)) for row in rows]


def main() -> None:
    try:
        evaluation = run_evaluation(API_URL)
        with psycopg.connect(DATABASE_URL) as connection:
            prepare_table(connection)
            run_id = save_run(connection, evaluation, os.getenv("LLM_PROVIDER", "mock"))
            history = recent_runs(connection)
    except (HTTPError, URLError, TimeoutError, psycopg.Error) as error:
        raise SystemExit(f"평가 API 또는 PostgreSQL 연결 실패: {error}") from error

    regression = len(history) > 1 and history[0]["pass_rate"] < history[1]["pass_rate"]
    print(json.dumps({"saved_run_id": run_id, "regression": regression, "history": history}, ensure_ascii=False, default=str, indent=2))


if __name__ == "__main__":
    main()
