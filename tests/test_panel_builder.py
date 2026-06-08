import pandas as pd

from ai_impact_research.processing.panel_builder import build_analytic_panel


def test_build_analytic_panel_forward_return() -> None:
    companies = pd.DataFrame(
        {"company_id": ["C1"], "ticker": ["AAA"], "name": ["AAA Corp"], "sector": ["Tech"], "industry": ["Software"], "market_cap": [100.0]}
    )
    scores = pd.DataFrame(
        {
            "company_id": ["C1"],
            "ticker": ["AAA"],
            "company_name": ["AAA Corp"],
            "snapshot_date": ["2025-03-31"],
            "ai_adoption_score": [4],
            "ai_fluency_score": [3],
            "ai_impact_score": [3],
            "ai_hiring_score": [4],
            "source_name": ["synthetic_larridin_sample"],
            "available_at": ["2025-04-02"],
        }
    )
    prices = pd.DataFrame(
        {
            "company_id": ["C1", "C1"],
            "ticker": ["AAA", "AAA"],
            "price_date": ["2025-03-31", "2025-06-30"],
            "adjusted_close": [100.0, 110.0],
        }
    )
    financials = pd.DataFrame(
        {
            "company_id": ["C1", "C1"],
            "ticker": ["AAA", "AAA"],
            "fiscal_quarter": ["2025Q1", "2025Q2"],
            "fiscal_period_end": ["2025-03-31", "2025-06-30"],
            "available_at": ["2025-04-25", "2025-07-25"],
            "revenue": [1000.0, 1050.0],
            "operating_margin": [0.20, 0.22],
            "employee_count": [100.0, 101.0],
        }
    )
    panel = build_analytic_panel(companies, scores, prices, financials)
    assert len(panel) == 1
    assert round(panel.loc[0, "fwd_return_1q"], 4) == 0.1000
    assert round(panel.loc[0, "revenue_growth_qoq"], 4) == 0.0500
    assert round(panel.loc[0, "operating_margin_delta_qoq"], 4) == 0.0200
