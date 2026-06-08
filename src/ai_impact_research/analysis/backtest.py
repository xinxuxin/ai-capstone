from __future__ import annotations

import pandas as pd


def assign_quantiles(
    df: pd.DataFrame,
    signal: str,
    period_col: str = "score_quarter",
    quantiles: int = 5,
    label_col: str = "signal_quantile",
) -> pd.DataFrame:
    out = df.copy()
    out[label_col] = pd.NA
    for _period, idx in out.groupby(period_col).groups.items():
        values = out.loc[idx, signal]
        valid_idx = values.dropna().index
        if len(valid_idx) < quantiles:
            continue
        try:
            out.loc[valid_idx, label_col] = pd.qcut(
                out.loc[valid_idx, signal],
                q=quantiles,
                labels=False,
                duplicates="drop",
            ) + 1
        except ValueError:
            # Too many ties. Use rank first to make the assignment deterministic.
            ranks = out.loc[valid_idx, signal].rank(method="first")
            out.loc[valid_idx, label_col] = pd.qcut(ranks, q=quantiles, labels=False) + 1
    return out


def quintile_returns(
    panel: pd.DataFrame,
    signal: str,
    return_col: str = "fwd_return_1q",
    period_col: str = "score_quarter",
    quantiles: int = 5,
) -> pd.DataFrame:
    assigned = assign_quantiles(panel, signal, period_col, quantiles)
    valid = assigned.dropna(subset=["signal_quantile", return_col]).copy()
    if valid.empty:
        return pd.DataFrame(columns=[period_col, "signal_quantile", "mean_return", "n"])
    grouped = (
        valid.groupby([period_col, "signal_quantile"], observed=True)[return_col]
        .agg(mean_return="mean", n="count")
        .reset_index()
    )
    return grouped


def long_short_returns(
    quintile_result: pd.DataFrame,
    period_col: str = "score_quarter",
    low_quantile: int = 1,
    high_quantile: int = 5,
) -> pd.DataFrame:
    if quintile_result.empty:
        return pd.DataFrame(columns=[period_col, "long_return", "short_return", "long_short_return"])
    q = quintile_result.copy()
    q["signal_quantile"] = q["signal_quantile"].astype(int)
    wide = q.pivot(index=period_col, columns="signal_quantile", values="mean_return")
    if low_quantile not in wide.columns or high_quantile not in wide.columns:
        return pd.DataFrame(columns=[period_col, "long_return", "short_return", "long_short_return"])
    out = pd.DataFrame(
        {
            period_col: wide.index.astype(str),
            "long_return": wide[high_quantile].values,
            "short_return": wide[low_quantile].values,
            "long_short_return": (wide[high_quantile] - wide[low_quantile]).values,
        }
    )
    out["cumulative_long_short"] = (1 + out["long_short_return"].fillna(0)).cumprod() - 1
    return out.reset_index(drop=True)
