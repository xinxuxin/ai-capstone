# Data Sources

## Larridin scores

Purpose: Core AI adoption signals.

MVP ingestion mode: CSV export only. Use `scripts/ingest_larridin.py`; do not call private APIs in tests or local smoke workflows.

Expected CSV fields:

- `company_id` or `ticker`
- `company_name`, if available
- `snapshot_date`
- `available_at`
- `ai_adoption_score`
- `ai_fluency_score`
- `ai_impact_score`
- `ai_hiring_score`
- `source_name`
- `source_url` or `source_reference`, if available

Ingestion rules:

- Tickers are normalized to uppercase.
- Score values must be whole numbers from 1 to 5.
- `snapshot_date` and `available_at` must parse as dates.
- Extra CSV columns are preserved in `metadata_json` in the normalized output.
- `available_at` is required. If a source export lacks it, the CLI allows `--available-at YYYY-MM-DD`; this is an explicit timing assumption and must be documented in downstream analysis.
- Normalized outputs should be written to `data/processed/larridin_scores_normalized.csv` or `.parquet`.

Future API mode:

- `LarridinAPIClient` is a stub until sponsor endpoint shape, authentication, pagination, and rate limits are confirmed.
- Do not hardcode private endpoint assumptions.
- Do not add network calls to tests.

## Financial metrics

Purpose: Operational outcomes and controls.

Candidate fields:

- revenue
- gross margin
- operating margin
- net income
- employee count
- revenue per employee

## Market data

Purpose: Forward return outcomes and hypothetical portfolio backtest.

Candidate fields:

- adjusted close
- volume
- market cap
- benchmark return
- sector benchmark return

## Unstructured sources

Purpose: LLM enrichment.

Sources:

- 10-K / 10-Q filings
- earnings call transcripts
- job postings
- news articles
- company AI initiative pages

## Data quality notes

- Job posting pages are not standardized.
- Large companies may have tens of thousands of openings; use defensible sampling.
- Companies disclose AI adoption differently, which creates disclosure bias.
- Always preserve `source_name`, `source_url`, `source_path`, `snapshot_date`, and `available_at`.
