import pandas as pd
import pytest

from ai_impact_research.analysis.ic import compute_ic_by_period, spearman_ic, summarize_ic


def test_spearman_ic_positive() -> None:
    df = pd.DataFrame({"signal": [1, 2, 3, 4, 5], "outcome": [0.1, 0.2, 0.3, 0.4, 0.5]})
    assert spearman_ic(df, "signal", "outcome") == pytest.approx(1.0)


def test_compute_ic_by_period() -> None:
    df = pd.DataFrame(
        {
            "score_quarter": ["2025Q1"] * 5,
            "signal": [1, 2, 3, 4, 5],
            "outcome": [0.1, 0.2, 0.3, 0.4, 0.5],
        }
    )
    ic = compute_ic_by_period(df, "signal", "outcome")
    summary = summarize_ic(ic)
    assert summary["num_periods"] == 1
    assert summary["hit_rate"] == 1.0
