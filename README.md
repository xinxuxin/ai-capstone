# AI Impact Research

AI Impact Research is the Larridin x CMU AI Capstone repository for testing whether AI adoption signals predict future public-company performance.

The project builds a reproducible decision intelligence system around four Larridin AI Transformation Tracker signals:

- `ai_adoption_score`
- `ai_fluency_score`
- `ai_impact_score`
- `ai_hiring_score`

The research pipeline combines those signals with public financial and market data to study forward returns, revenue growth, margin expansion, revenue per employee, and hiring or headcount indicators when available.

```text
Larridin signals + public company data
        -> normalized datasets
        -> company-quarter analytical panel
        -> IC, regression, backtest, robustness analysis
        -> Streamlit dashboard + ticker-level report
```

## Setup

Use Python 3.11 or newer. `uv` is recommended for local development, but plain `pip` also works.

```bash
uv sync --all-extras
```

Pip alternative:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Create local configuration from the example file:

```bash
cp .env.example .env
```

Real credentials are optional for the current sample workflow and are not required for tests.

Makefile commands use the active `python` by default. If you do not activate the venv, pass it explicitly:

```bash
make PYTHON=.venv/bin/python test
```

## Test Commands

```bash
make test
make lint
python -m compileall src
pytest tests
ruff check src tests
```

## Sample Workflow

The committed sample data is synthetic and intended for smoke tests only.

```bash
make sample-panel
make sample-analysis
make robustness
make dashboard
```

The sample workflow writes local outputs under ignored folders such as `data/processed/` and `reports/tables/`.

## Data Policy

- Do not commit real API keys, tokens, database credentials, or private sponsor data.
- Do not commit proprietary raw data.
- Keep raw, interim, processed, and external datasets in ignored `data/` folders or managed storage.
- Sample data committed to the repo must be clearly marked synthetic.
- Every model feature must preserve an observation date or `available_at` timestamp.
- Do not invent real research results. Label exploratory and hypothetical outputs clearly.

## Configuration

Default local configuration lives in [configs/base.yaml](configs/base.yaml). Environment variables and values in `.env` can override local settings.

Useful local variables:

- `PROJECT_ENV`
- `AI_IMPACT_CONFIG`
- `AI_IMPACT_SAMPLES_DIR`
- `AI_IMPACT_PROCESSED_DIR`
- `AI_IMPACT_REPORTS_DIR`
- `AI_IMPACT_DEFAULT_SIGNAL`
- `AI_IMPACT_DEFAULT_RETURN_COLUMN`
- `AI_IMPACT_LOG_LEVEL`
- `DATABASE_URL`
- `LARRIDIN_API_BASE_URL`
- `LARRIDIN_API_KEY`
- `SEC_USER_AGENT`

## Repo Structure

```text
.
├── configs/                 # YAML configuration
├── data/                    # sample data plus ignored local data folders
├── docs/                    # architecture, methodology, and reproducibility docs
├── infra/                   # SQL schema and deployment notes
├── reports/                 # report templates and ignored generated outputs
├── scripts/                 # command-line entry points
├── src/ai_impact_research/  # Python package
└── tests/                   # pytest suite
```

## Development Notes

- Keep changes small and reviewable.
- Keep Streamlit pages thin; put reusable logic in package modules.
- Prefer deterministic tests using synthetic fixtures.
- Avoid heavyweight orchestration frameworks until the research workflow needs them.
