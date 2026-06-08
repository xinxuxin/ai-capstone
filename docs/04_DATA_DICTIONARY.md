# Data Dictionary

## `companies`

| Field | Type | Description |
|---|---|---|
| company_id | string | Internal stable company identifier |
| ticker | string | Primary ticker at collection time |
| name | string | Legal or display company name |
| sector | string | Sector classification |
| industry | string | Industry classification |
| cik | string | SEC Central Index Key |
| exchange | string | Listing exchange |
| market_cap | float | Market capitalization, if available |

## `larridin_scores`

| Field | Type | Description |
|---|---|---|
| company_id | string | Internal company identifier |
| ticker | string | Ticker from source |
| snapshot_date | date | Date of Larridin score snapshot |
| score_quarter | string | Calendar quarter derived from snapshot_date |
| ai_adoption_score | int | 1–5 AI adoption maturity score |
| ai_fluency_score | int | 1–5 AI fluency score |
| ai_impact_score | int | 1–5 AI impact / initiatives score |
| ai_hiring_score | int | 1–5 AI hiring signal score |
| source_name | string | Source name |
| available_at | timestamp | Date when score was observable to the model |

## `financial_metrics`

| Field | Type | Description |
|---|---|---|
| company_id | string | Internal company identifier |
| fiscal_quarter | string | Fiscal quarter label, such as 2025Q2 |
| fiscal_period_end | date | Period end date |
| revenue | float | Revenue for the period |
| operating_margin | float | Operating margin ratio |
| employee_count | float | Employee count, if available |
| available_at | timestamp | Date when the metric became available |

## `market_prices`

| Field | Type | Description |
|---|---|---|
| company_id | string | Internal company identifier |
| price_date | date | Price observation date |
| price_quarter | string | Quarter derived from price_date |
| adjusted_close | float | Adjusted close price |
| volume | float | Trading volume |
| available_at | timestamp | Date when the price was available |

## `analytic_panel`

| Field | Type | Description |
|---|---|---|
| company_id | string | Internal company identifier |
| ticker | string | Ticker |
| score_quarter | string | Quarter when signal is measured |
| AI score columns | numeric | Signal features measured at t |
| fwd_return_1q | float | Next-quarter stock return |
| revenue_growth_qoq | float | Next-quarter revenue growth |
| operating_margin_delta_qoq | float | Next-quarter operating margin change |
| revenue_per_employee | float | Revenue divided by employees at t |
