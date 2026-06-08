CREATE TABLE IF NOT EXISTS companies (
    company_id TEXT PRIMARY KEY,
    ticker TEXT NOT NULL,
    name TEXT NOT NULL,
    sector TEXT,
    industry TEXT,
    cik TEXT,
    exchange TEXT,
    market_cap NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS company_identifiers (
    company_id TEXT REFERENCES companies(company_id),
    identifier_type TEXT NOT NULL,
    identifier_value TEXT NOT NULL,
    valid_from DATE,
    valid_to DATE,
    source_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    PRIMARY KEY (company_id, identifier_type, identifier_value)
);

CREATE TABLE IF NOT EXISTS larridin_scores (
    score_id BIGSERIAL PRIMARY KEY,
    company_id TEXT REFERENCES companies(company_id),
    ticker TEXT NOT NULL,
    snapshot_date DATE NOT NULL,
    score_quarter TEXT NOT NULL,
    ai_adoption_score INTEGER CHECK (ai_adoption_score BETWEEN 1 AND 5),
    ai_fluency_score INTEGER CHECK (ai_fluency_score BETWEEN 1 AND 5),
    ai_impact_score INTEGER CHECK (ai_impact_score BETWEEN 1 AND 5),
    ai_hiring_score INTEGER CHECK (ai_hiring_score BETWEEN 1 AND 5),
    source_name TEXT,
    source_url TEXT,
    available_at TIMESTAMPTZ NOT NULL,
    raw_payload JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (company_id, snapshot_date)
);

CREATE TABLE IF NOT EXISTS financial_metrics (
    metric_id BIGSERIAL PRIMARY KEY,
    company_id TEXT REFERENCES companies(company_id),
    ticker TEXT NOT NULL,
    fiscal_quarter TEXT NOT NULL,
    fiscal_period_end DATE NOT NULL,
    revenue NUMERIC,
    operating_margin NUMERIC,
    employee_count NUMERIC,
    source_name TEXT,
    source_url TEXT,
    available_at TIMESTAMPTZ NOT NULL,
    raw_payload JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (company_id, fiscal_quarter, source_name)
);

CREATE TABLE IF NOT EXISTS market_prices (
    price_id BIGSERIAL PRIMARY KEY,
    company_id TEXT REFERENCES companies(company_id),
    ticker TEXT NOT NULL,
    price_date DATE NOT NULL,
    price_quarter TEXT NOT NULL,
    adjusted_close NUMERIC NOT NULL,
    volume NUMERIC,
    source_name TEXT,
    available_at TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (company_id, price_date, source_name)
);

CREATE TABLE IF NOT EXISTS source_documents (
    source_document_id TEXT PRIMARY KEY,
    company_id TEXT REFERENCES companies(company_id),
    ticker TEXT,
    source_type TEXT NOT NULL,
    source_name TEXT,
    source_url TEXT,
    source_path TEXT,
    document_date DATE,
    collected_at TIMESTAMPTZ NOT NULL,
    available_at TIMESTAMPTZ NOT NULL,
    content_hash TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS llm_extractions (
    extraction_id BIGSERIAL PRIMARY KEY,
    source_document_id TEXT REFERENCES source_documents(source_document_id),
    company_id TEXT REFERENCES companies(company_id),
    ticker TEXT,
    period TEXT,
    model_name TEXT NOT NULL,
    prompt_version TEXT NOT NULL,
    extraction_json JSONB NOT NULL,
    confidence NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS analytic_panel_snapshots (
    panel_snapshot_id TEXT PRIMARY KEY,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    input_data_versions JSONB,
    row_count INTEGER,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS model_runs (
    model_run_id TEXT PRIMARY KEY,
    panel_snapshot_id TEXT REFERENCES analytic_panel_snapshots(panel_snapshot_id),
    run_type TEXT NOT NULL,
    signal_name TEXT,
    outcome_name TEXT,
    config_json JSONB,
    git_commit_hash TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS backtest_results (
    result_id BIGSERIAL PRIMARY KEY,
    model_run_id TEXT REFERENCES model_runs(model_run_id),
    metric_name TEXT NOT NULL,
    metric_value NUMERIC,
    metric_json JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
