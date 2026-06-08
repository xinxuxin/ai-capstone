# Backtesting Methodology

## Main hypotheses

- H1: Higher AI adoption scores are positively associated with future excess returns.
- H2: AI hiring scores lead future revenue per employee growth.
- H3: AI impact scores are more strongly associated with margin expansion than raw AI mention intensity.

## Feature timing

Only use features that are available at or before the prediction date. Every record should carry `available_at`.

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

## Caveats

- Correlation is not causation.
- Short history may make Sharpe ratios unstable.
- Disclosure intensity may bias AI scores toward large-cap or technology companies.
- Hypothetical backtests are not investment advice.
