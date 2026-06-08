# AI Impact Research Starter

This repository is a starter codebase for the Larridin × CMU AI Capstone project:
**Do AI adoption signals predict company performance?**

The project should be treated as a reproducible AI × finance research system, not just a dashboard demo. The intended pipeline is:

```text
Larridin scores + public company data
        ↓
raw and normalized datasets
        ↓
company-quarter analytical panel
        ↓
IC / regression / backtest / robustness analysis
        ↓
Streamlit dashboard + ticker-level research report
```

## What is already included

- Python package skeleton under `src/ai_impact_research/`
- Sample synthetic company, score, price, and fundamentals data under `data/samples/`
- Panel builder, IC analysis, simple backtest utilities, and deterministic report generator
- Streamlit dashboard starter
- SQL schema starter under `infra/db_schema.sql`
- Phased coding prompts under `docs/01_PHASED_CODING_PROMPTS.md`
- Methodology and documentation templates under `docs/`

All sample data is synthetic and for local smoke tests only.

## Quick start

```bash
# 1. Install dependencies. uv is recommended, but pip also works.
uv sync

# or:
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# 2. Run tests
make test

# 3. Build a sample analytical panel
make sample-panel

# 4. Run baseline analysis on the sample panel
make sample-analysis

# 5. Start dashboard
make dashboard
```

## Expected first-week goal

By the end of the first week, the team should be able to:

1. Import Larridin scores or a sponsor-provided export.
2. Build a clean company universe with ticker, CIK, sector, and industry.
3. Pull or import public financial and market data.
4. Build a company-quarter analytical panel.
5. Compute the first IC and quintile backtest.
6. Show coverage, signal distributions, and preliminary results in Streamlit.

## Repository conventions

- Keep raw data out of git. Use `data/raw/`, object storage, or database tables.
- Every derived dataset should record source, snapshot date, and `available_at` timestamp.
- Never commit API keys, database URLs with credentials, or private sponsor data.
- Avoid look-ahead bias. Features must only use data observable at or before the prediction date.
- Treat backtests as research artifacts, not investment advice.

## Project structure

```text
.
├── configs/                 # YAML configs
├── data/                    # local data folders; raw/interim/processed ignored
├── docs/                    # project docs and coding prompts
├── infra/                   # SQL schema and deployment notes
├── reports/                 # research outputs, figures, tables
├── scripts/                 # runnable entry points
├── src/ai_impact_research/  # package code
└── tests/                   # unit tests
```
