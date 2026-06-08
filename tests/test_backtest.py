import pandas as pd

from ai_impact_research.analysis.backtest import long_short_returns, quintile_returns


def test_quintile_and_long_short_returns() -> None:
    panel = pd.DataFrame(
        {
            "score_quarter": ["2025Q1"] * 10,
            "signal": list(range(10)),
            "fwd_return_1q": [x / 100 for x in range(10)],
        }
    )
    q = quintile_returns(panel, "signal", "fwd_return_1q")
    ls = long_short_returns(q)
    assert not q.empty
    assert not ls.empty
    assert ls.loc[0, "long_short_return"] > 0
