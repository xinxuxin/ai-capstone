from __future__ import annotations

import pandas as pd

from ai_impact_research.ingestion.financials import normalize_financials
from ai_impact_research.ingestion.larridin import SCORE_COLUMNS, normalize_larridin_scores
from ai_impact_research.ingestion.market_data import normalize_market_prices
from ai_impact_research.processing.identifiers import attach_company_id, normalize_companies
from ai_impact_research.time_utils import next_quarter_label


def build_analytic_panel(
    companies: pd.DataFrame,
    larridin_scores: pd.DataFrame,
    market_prices: pd.DataFrame,
    financials: pd.DataFrame,
) -> pd.DataFrame:
    """Build a company-quarter panel with signals at t and outcomes at t+1.

    The implementation uses quarterly sample data. Production code should align on actual
    prediction dates and data availability windows.
    """
    companies = normalize_companies(companies)
    scores = attach_company_id(normalize_larridin_scores(larridin_scores), companies)
    prices = attach_company_id(normalize_market_prices(market_prices), companies)
    fins = attach_company_id(normalize_financials(financials), companies)

    base = scores.merge(
        companies[["company_id", "ticker", "name", "sector", "industry", "market_cap"]],
        on=["company_id", "ticker"],
        how="left",
    )

    # Price at score quarter and next quarter end.
    current_prices = prices[["company_id", "price_quarter", "adjusted_close"]].rename(
        columns={"price_quarter": "score_quarter", "adjusted_close": "price_t"}
    )
    next_prices = prices[["company_id", "price_quarter", "adjusted_close"]].rename(
        columns={"price_quarter": "next_quarter", "adjusted_close": "price_t_plus_1"}
    )

    base["next_quarter"] = base["score_quarter"].map(next_quarter_label)
    panel = base.merge(current_prices, on=["company_id", "score_quarter"], how="left")
    panel = panel.merge(next_prices, on=["company_id", "next_quarter"], how="left")
    panel["fwd_return_1q"] = panel["price_t_plus_1"] / panel["price_t"] - 1

    # Financials at t and t+1.
    fin_t = fins.rename(columns={"fiscal_quarter": "score_quarter"})[
        [
            "company_id",
            "score_quarter",
            "revenue",
            "operating_margin",
            "employee_count",
            "available_at",
        ]
    ].rename(
        columns={
            "revenue": "revenue_t",
            "operating_margin": "operating_margin_t",
            "employee_count": "employee_count_t",
            "available_at": "financial_available_at_t",
        }
    )
    fin_next = fins.rename(columns={"fiscal_quarter": "next_quarter"})[
        ["company_id", "next_quarter", "revenue", "operating_margin", "employee_count", "available_at"]
    ].rename(
        columns={
            "revenue": "revenue_t_plus_1",
            "operating_margin": "operating_margin_t_plus_1",
            "employee_count": "employee_count_t_plus_1",
            "available_at": "financial_available_at_t_plus_1",
        }
    )

    panel = panel.merge(fin_t, on=["company_id", "score_quarter"], how="left")
    panel = panel.merge(fin_next, on=["company_id", "next_quarter"], how="left")
    panel["revenue_growth_qoq"] = panel["revenue_t_plus_1"] / panel["revenue_t"] - 1
    panel["operating_margin_delta_qoq"] = (
        panel["operating_margin_t_plus_1"] - panel["operating_margin_t"]
    )
    panel["revenue_per_employee_t"] = panel["revenue_t"] / panel["employee_count_t"]

    # Composite score: simple average for MVP. Replace with documented weighting if sponsor provides rubric.
    panel["ai_composite_score"] = panel[SCORE_COLUMNS].mean(axis=1)

    duplicates = panel.duplicated(["company_id", "score_quarter"], keep=False)
    if duplicates.any():
        keys = panel.loc[duplicates, ["company_id", "score_quarter"]].to_dict("records")
        raise ValueError(f"Analytical panel has duplicate company-quarter rows: {keys}")

    ordered_cols = [
        "company_id",
        "ticker",
        "name",
        "sector",
        "industry",
        "score_quarter",
        "snapshot_date",
        "available_at",
        *SCORE_COLUMNS,
        "ai_composite_score",
        "market_cap",
        "price_t",
        "price_t_plus_1",
        "fwd_return_1q",
        "revenue_t",
        "revenue_t_plus_1",
        "revenue_growth_qoq",
        "operating_margin_t",
        "operating_margin_t_plus_1",
        "operating_margin_delta_qoq",
        "employee_count_t",
        "revenue_per_employee_t",
        "next_quarter",
    ]
    existing_cols = [col for col in ordered_cols if col in panel.columns]
    return panel[existing_cols].sort_values(["ticker", "score_quarter"]).reset_index(drop=True)
