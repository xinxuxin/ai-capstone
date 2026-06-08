from __future__ import annotations

import pandas as pd

from ai_impact_research.analysis.robustness import missingness_summary


def test_missingness_summary_without_group_col() -> None:
    df = pd.DataFrame({"ticker": ["AAA", "BBB"], "value": [1.0, None]})

    summary = missingness_summary(df)

    assert set(summary.columns) == {"field", "missing_rate"}
    assert summary.loc[summary["field"].eq("value"), "missing_rate"].iloc[0] == 0.5
