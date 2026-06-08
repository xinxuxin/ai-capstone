from __future__ import annotations

import streamlit as st

from ai_impact_research.analysis.backtest import long_short_returns, quintile_returns
from ai_impact_research.dashboard.components import load_panel, show_research_caveat

st.title("Backtest")
show_research_caveat()
panel = load_panel()
if panel.empty:
    st.info("Run `make sample-panel` first.")
    st.stop()

signal = st.selectbox("Signal", [c for c in panel.columns if c.startswith("ai_") and c.endswith("score")])
q = quintile_returns(panel, signal)
ls = long_short_returns(q)
st.subheader("Quintile returns")
st.dataframe(q)
st.subheader("Long-short returns")
st.dataframe(ls)
