from __future__ import annotations

import pandas as pd


def get_company_panel(panel: pd.DataFrame, ticker: str) -> pd.DataFrame:
    ticker = ticker.upper().strip()
    company = panel[panel["ticker"].str.upper().eq(ticker)].copy()
    if company.empty:
        raise ValueError(f"Ticker not found in panel: {ticker}")
    return company.sort_values("score_quarter")


def latest_company_snapshot(panel: pd.DataFrame, ticker: str) -> dict:
    company = get_company_panel(panel, ticker)
    latest = company.iloc[-1].to_dict()
    return latest


def peer_rank(panel: pd.DataFrame, ticker: str, score_col: str = "ai_composite_score") -> dict:
    company = latest_company_snapshot(panel, ticker)
    sector = company.get("sector")
    quarter = company.get("score_quarter")
    peers = panel[(panel["sector"].eq(sector)) & (panel["score_quarter"].eq(quarter))].copy()
    peers["rank_desc"] = peers[score_col].rank(ascending=False, method="min")
    target = peers[peers["ticker"].str.upper().eq(ticker.upper())].iloc[0]
    return {
        "sector": sector,
        "quarter": quarter,
        "score_col": score_col,
        "rank": int(target["rank_desc"]),
        "num_peers": int(len(peers)),
    }
