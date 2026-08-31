CREATE TABLE IF NOT EXISTS travel_task_runs (
    task_id TEXT PRIMARY KEY,
    trace_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    request TEXT NOT NULL,
    status TEXT NOT NULL,
    result JSONB NOT NULL DEFAULT '{}'::jsonb,
    error TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_travel_task_runs_user_created
    ON travel_task_runs (user_id, created_at DESC);

CREATE TABLE IF NOT EXISTS travel_trace_events (
    event_id BIGSERIAL PRIMARY KEY,
    task_id TEXT NOT NULL REFERENCES travel_task_runs(task_id) ON DELETE CASCADE,
    trace_id TEXT NOT NULL,
    sequence INTEGER NOT NULL,
    actor TEXT NOT NULL,
    action TEXT NOT NULL,
    status TEXT NOT NULL,
    payload JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (task_id, sequence)
);

CREATE INDEX IF NOT EXISTS idx_travel_trace_events_trace
    ON travel_trace_events (trace_id, sequence);
