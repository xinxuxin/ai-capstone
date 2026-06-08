from __future__ import annotations

import streamlit as st

from ai_impact_research.agent.company_report_agent import generate_company_report
from ai_impact_research.dashboard.components import load_panel, show_research_caveat

st.title("Report Generator")
show_research_caveat()
panel = load_panel()
if panel.empty:
    st.info("Run `make sample-panel` first.")
    st.stop()

ticker = st.selectbox("Ticker", sorted(panel["ticker"].unique()))
report = generate_company_report(panel, ticker)
st.markdown(report)
