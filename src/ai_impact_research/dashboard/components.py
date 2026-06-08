from __future__ import annotations

import pandas as pd
import streamlit as st

from ai_impact_research.config import load_settings


@st.cache_data
def load_panel() -> pd.DataFrame:
    settings = load_settings()
    processed_panel = settings.processed_dir / "analytic_panel.csv"
    sample_panel = settings.samples_dir / "larridin_scores.csv"
    if processed_panel.exists():
        return pd.read_csv(processed_panel)
    st.warning(
        "Processed panel not found. Run `make sample-panel` first. Showing an empty dashboard shell."
    )
    if sample_panel.exists():
        return pd.DataFrame()
    raise FileNotFoundError("No panel or sample data found.")


def show_research_caveat() -> None:
    st.caption(
        "Research use only. Hypothetical backtests are not investment advice. "
        "All findings require data-quality and timing checks."
    )
