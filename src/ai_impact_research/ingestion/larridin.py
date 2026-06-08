from __future__ import annotations

import pandas as pd

from ai_impact_research.time_utils import to_calendar_quarter

SCORE_COLUMNS = [
    "ai_adoption_score",
    "ai_fluency_score",
    "ai_impact_score",
    "ai_hiring_score",
]

REQUIRED_SCORE_COLUMNS = [
    "ticker",
    "company_name",
    "snapshot_date",
    *SCORE_COLUMNS,
]


def load_larridin_scores_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return normalize_larridin_scores(df)


def normalize_larridin_scores(df: pd.DataFrame) -> pd.DataFrame:
    missing = set(REQUIRED_SCORE_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Larridin score file is missing required columns: {sorted(missing)}")

    out = df.copy()
    out["ticker"] = out["ticker"].astype(str).str.upper().str.strip()
    out["snapshot_date"] = pd.to_datetime(out["snapshot_date"]).dt.date
    out["score_quarter"] = to_calendar_quarter(pd.Series(out["snapshot_date"]))

    if "available_at" not in out.columns:
        out["available_at"] = pd.to_datetime(out["snapshot_date"])
    else:
        out["available_at"] = pd.to_datetime(out["available_at"])

    for col in SCORE_COLUMNS:
        out[col] = pd.to_numeric(out[col], errors="raise").astype(int)
        invalid = ~out[col].between(1, 5)
        if invalid.any():
            bad_values = out.loc[invalid, ["ticker", "snapshot_date", col]].to_dict("records")
            raise ValueError(f"Invalid 1-5 score values in {col}: {bad_values}")

    if "source_name" not in out.columns:
        out["source_name"] = "larridin_export"
    if "source_url" not in out.columns:
        out["source_url"] = None

    return out
