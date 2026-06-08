from __future__ import annotations

import pandas as pd

from ai_impact_research.agent.tools import latest_company_snapshot, peer_rank


def _fmt(value, digits: int = 3) -> str:
    if pd.isna(value):
        return "unavailable"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def generate_company_report(panel: pd.DataFrame, ticker: str) -> str:
    latest = latest_company_snapshot(panel, ticker)
    rank = peer_rank(panel, ticker)
    name = latest.get("name", ticker.upper())

    return f"""# {name} ({ticker.upper()}) AI Impact Research Brief

## Company snapshot

- Sector: {_fmt(latest.get('sector'))}
- Industry: {_fmt(latest.get('industry'))}
- Latest signal quarter: {_fmt(latest.get('score_quarter'))}

## AI maturity summary

- AI Adoption: {_fmt(latest.get('ai_adoption_score'))}
- AI Fluency: {_fmt(latest.get('ai_fluency_score'))}
- AI Impact / Initiatives: {_fmt(latest.get('ai_impact_score'))}
- AI Hiring: {_fmt(latest.get('ai_hiring_score'))}
- Composite AI score: {_fmt(latest.get('ai_composite_score'))}

## Financial performance context

- Forward 1Q return from latest signal quarter: {_fmt(latest.get('fwd_return_1q'))}
- Revenue growth QoQ: {_fmt(latest.get('revenue_growth_qoq'))}
- Operating margin delta QoQ: {_fmt(latest.get('operating_margin_delta_qoq'))}
- Revenue per employee at t: {_fmt(latest.get('revenue_per_employee_t'))}

## Peer comparison

In {_fmt(rank.get('sector'))} for {_fmt(rank.get('quarter'))}, this company ranks {rank.get('rank')} out of {rank.get('num_peers')} peers by {rank.get('score_col')}.

## Methodology caveats

This brief is generated from the analytical panel. Missing fields are reported as unavailable. The output is a research summary, not investment advice. Historical relationships and hypothetical backtests should not be interpreted as causal proof or trading recommendations.
"""
