# Interim Findings

Phase 9 adds reproducible baseline quantitative analysis for the synthetic/sample analytical panel.

Generated tables are written by `scripts/run_baseline_analysis.py` to:

- `data/processed/analysis/`
- `reports/tables/`

Baseline methods:

- Cross-sectional Spearman IC by quarter.
- Pooled OLS regression with available controls plus sector and quarter fixed effects.
- Equal-weight quintile backtest and Q5-Q1 long-short summary.

Interpretation guardrails:

- These outputs are associational research diagnostics.
- They do not establish causality.
- They are not investment advice.
- Synthetic sample results must not be represented as real sponsor findings.

Open review items:

- Confirm sponsor-approved benchmark or sector return field for excess return analysis.
- Confirm minimum sample thresholds for regression and quintile construction on real data.
- Decide whether robust or clustered standard errors should replace baseline OLS standard errors.
