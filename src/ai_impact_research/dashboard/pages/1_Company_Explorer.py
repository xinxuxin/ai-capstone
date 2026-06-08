from __future__ import annotations

import streamlit as st
from ai_impact_research.dashboard.components import load_panel, show_research_caveat

st.title("Company Explorer")
show_research_caveat()
panel = load_panel()
if panel.empty:
    st.info("Run `make sample-panel` first.")
    st.stop()

ticker = st.selectbox("Ticker", sorted(panel["ticker"].unique()))
st.dataframe(panel[panel["ticker"].eq(ticker)].sort_values("score_quarter"))
