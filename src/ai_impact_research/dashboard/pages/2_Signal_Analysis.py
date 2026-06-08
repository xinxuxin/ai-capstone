from __future__ import annotations

import streamlit as st

from ai_impact_research.analysis.ic import compute_ic_by_period, summarize_ic
from ai_impact_research.analysis.plots import signal_vs_outcome_figure
from ai_impact_research.dashboard.components import load_panel, show_research_caveat

st.title("Signal Analysis")
show_research_caveat()
panel = load_panel()
if panel.empty:
    st.info("Run `make sample-panel` first.")
    st.stop()

signal = st.selectbox("Signal", [c for c in panel.columns if c.startswith("ai_") and c.endswith("score")])
outcome = st.selectbox("Outcome", ["fwd_return_1q", "revenue_growth_qoq", "operating_margin_delta_qoq"])
st.plotly_chart(signal_vs_outcome_figure(panel.dropna(subset=[signal, outcome]), signal, outcome), use_container_width=True)
ic = compute_ic_by_period(panel, signal, outcome)
st.dataframe(ic)
st.json(summarize_ic(ic))
