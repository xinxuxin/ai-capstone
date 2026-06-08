from __future__ import annotations

import pandas as pd


def missingness_summary(df: pd.DataFrame, group_col: str | None = None) -> pd.DataFrame:
    if group_col is None:
        return df.isna().mean().rename("missing_rate").rename_axis("field").reset_index()
    rows = []
    for group, part in df.groupby(group_col):
        miss = part.isna().mean()
        for field, rate in miss.items():
            rows.append({group_col: group, "field": field, "missing_rate": float(rate)})
    return pd.DataFrame(rows)
