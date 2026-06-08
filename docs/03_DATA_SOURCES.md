# Data Sources

## Larridin scores

Purpose: Core AI adoption signals.

Expected fields:

- company name
- ticker
- snapshot date
- AI Adoption score
- AI Fluency score
- AI Impact / Initiatives score
- AI Hiring score
- source metadata

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
