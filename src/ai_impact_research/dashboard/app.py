from __future__ import annotations

import streamlit as st

from ai_impact_research.analysis.ic import compute_ic_by_period, summarize_ic
from ai_impact_research.analysis.plots import score_distribution_figure, signal_vs_outcome_figure
from ai_impact_research.dashboard.components import load_panel, show_research_caveat

st.set_page_config(page_title="AI Impact Research", layout="wide")
st.title("AI Impact Research Dashboard")
show_research_caveat()

panel = load_panel()

if panel.empty:
    st.info("Run `make sample-panel` to create data/processed/analytic_panel.csv.")
    st.stop()

score_columns = [
    col
    for col in [
        "ai_adoption_score",
        "ai_fluency_score",
        "ai_impact_score",
        "ai_hiring_score",
        "ai_composite_score",
    ]
    if col in panel.columns
]
outcome_columns = [
    col
    for col in ["fwd_return_1q", "revenue_growth_qoq", "operating_margin_delta_qoq"]
    if col in panel.columns
]

col1, col2, col3 = st.columns(3)
col1.metric("Companies", panel["ticker"].nunique())
col2.metric("Quarters", panel["score_quarter"].nunique())
col3.metric("Rows", len(panel))

st.header("Coverage")
st.dataframe(panel.groupby("sector")["ticker"].nunique().rename("company_count").reset_index())

st.header("Signal distribution")
selected_score = st.selectbox("Signal", score_columns)
st.plotly_chart(score_distribution_figure(panel, selected_score), use_container_width=True)

if outcome_columns:
    st.header("Signal analysis")
    selected_outcome = st.selectbox("Outcome", outcome_columns)
    st.plotly_chart(
        signal_vs_outcome_figure(panel.dropna(subset=[selected_score, selected_outcome]), selected_score, selected_outcome),
        use_container_width=True,
    )
    try:
        ic = compute_ic_by_period(panel, selected_score, selected_outcome)
        st.subheader("IC by quarter")
        st.dataframe(ic)
        st.json(summarize_ic(ic))
    except ValueError as exc:
        st.warning(str(exc))

st.header("Company explorer")
ticker = st.selectbox("Ticker", sorted(panel["ticker"].unique()))
st.dataframe(panel[panel["ticker"].eq(ticker)].sort_values("score_quarter"))
