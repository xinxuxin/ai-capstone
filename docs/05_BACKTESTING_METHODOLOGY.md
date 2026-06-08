# Backtesting Methodology

## Main hypotheses

- H1: Higher AI adoption scores are positively associated with future excess returns.
- H2: AI hiring scores lead future revenue per employee growth.
- H3: AI impact scores are more strongly associated with margin expansion than raw AI mention intensity.

## Feature timing

Only use features that are available at or before the prediction date. Every record should carry `available_at`.

The analytical panel uses these timing conventions:

- Panel grain is one row per `company_id` per `score_quarter`.
- `prediction_date` defaults to the Larridin score `available_at` date unless an explicit prediction date is supplied for a research experiment.
- `score_available_at` must be at or before `prediction_date`.
- Market outcomes start from the first price date after `prediction_date`; the one-quarter outcome ends at the next available price date.
- `prior_return_1q` uses only prices at or before `prediction_date`.
- Financial controls use only fundamentals with `available_at <= prediction_date`.
- Future fundamental outcomes use fiscal periods ending after `prediction_date`.
- Strict mode excludes rows with timing violations.
- Permissive mode preserves rows and sets `timing_warning` / `timing_violation` for audit.

## Core metrics

- Spearman information coefficient (IC)
- Mean IC and IC hit rate
- Regression coefficient, p-value, and confidence interval
- Quintile portfolio return
- Q5-Q1 long-short return
- Sharpe ratio, if sufficient time-series observations exist

## Basic regression

```text
future_outcome_i,t+1 = beta_0
  + beta_1 * ai_signal_i,t
  + beta_2 * log_market_cap_i,t
  + beta_3 * prior_return_i,t
  + sector fixed effects
  + quarter fixed effects
  + error_i,t
```

## Quintile portfolio construction

For each rebalance period:

- Use the analytical panel after strict timing filtering.
- Rank companies by the selected AI signal within the period.
- Form quintiles only when there are enough names for meaningful buckets.
- Compute equal-weight average forward returns by quintile.
- Report Q5-Q1 long-short return when both edge quintiles are populated.
- Use `fwd_excess_return_1q` only as a benchmark-relative diagnostic unless a sponsor-approved benchmark field is available.

Rows with missing signal, missing outcome, or `timing_violation = true` should be excluded from strict IC, regression, and backtest runs.

## Caveats

- Correlation is not causation.
- Short history may make Sharpe ratios unstable.
- Disclosure intensity may bias AI scores toward large-cap or technology companies.
- Hypothetical backtests are not investment advice.
