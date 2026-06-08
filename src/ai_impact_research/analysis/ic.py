from __future__ import annotations

import pandas as pd
from scipy.stats import spearmanr


def spearman_ic(df: pd.DataFrame, signal: str, outcome: str) -> float:
    valid = df[[signal, outcome]].dropna()
    if len(valid) < 3:
        raise ValueError(f"Need at least 3 valid observations for IC; got {len(valid)}")
    return float(spearmanr(valid[signal], valid[outcome]).statistic)


def compute_ic_by_period(
    panel: pd.DataFrame,
    signal: str,
    outcome: str,
    period_col: str = "score_quarter",
) -> pd.DataFrame:
    rows: list[dict] = []
    for period, group in panel.groupby(period_col):
        valid = group[[signal, outcome]].dropna()
        if len(valid) < 3:
            rows.append({"period": period, "ic": None, "n": len(valid), "status": "too_few_obs"})
            continue
        result = spearmanr(valid[signal], valid[outcome])
        rows.append(
            {
                "period": period,
                "ic": float(result.statistic),
                "p_value": float(result.pvalue),
                "n": len(valid),
                "status": "ok",
            }
        )
    return pd.DataFrame(rows)


def summarize_ic(ic_by_period: pd.DataFrame) -> dict[str, float | int | None]:
    valid = ic_by_period[ic_by_period["status"].eq("ok") & ic_by_period["ic"].notna()]
    if valid.empty:
        return {"mean_ic": None, "hit_rate": None, "num_periods": 0}
    return {
        "mean_ic": float(valid["ic"].mean()),
        "hit_rate": float((valid["ic"] > 0).mean()),
        "num_periods": int(len(valid)),
    }
