from __future__ import annotations

import pandas as pd
import plotly.express as px


def score_distribution_figure(panel: pd.DataFrame, score_col: str):
    return px.histogram(panel, x=score_col, nbins=5, title=f"Distribution of {score_col}")


def signal_vs_outcome_figure(panel: pd.DataFrame, signal: str, outcome: str):
    return px.scatter(panel, x=signal, y=outcome, color="sector", hover_data=["ticker"])
