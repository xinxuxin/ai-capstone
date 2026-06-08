from __future__ import annotations

import pandas as pd

REQUIRED_FINANCIAL_COLUMNS = [
    "ticker",
    "fiscal_quarter",
    "fiscal_period_end",
    "revenue",
    "operating_margin",
]


def load_financials_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return normalize_financials(df)


def normalize_financials(df: pd.DataFrame) -> pd.DataFrame:
    missing = set(REQUIRED_FINANCIAL_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Financial file is missing required columns: {sorted(missing)}")

    out = df.copy()
    out["ticker"] = out["ticker"].astype(str).str.upper().str.strip()
    out["fiscal_quarter"] = out["fiscal_quarter"].astype(str).str.upper().str.strip()
    out["fiscal_period_end"] = pd.to_datetime(out["fiscal_period_end"]).dt.date
    out["revenue"] = pd.to_numeric(out["revenue"], errors="raise")
    out["operating_margin"] = pd.to_numeric(out["operating_margin"], errors="raise")

    if "employee_count" not in out.columns:
        out["employee_count"] = None
    else:
        out["employee_count"] = pd.to_numeric(out["employee_count"], errors="coerce")

    if "source_name" not in out.columns:
        out["source_name"] = "financial_export"
    if "available_at" not in out.columns:
        out["available_at"] = pd.to_datetime(out["fiscal_period_end"])
    else:
        out["available_at"] = pd.to_datetime(out["available_at"])

    duplicate_mask = out.duplicated(["ticker", "fiscal_quarter", "source_name"], keep=False)
    if duplicate_mask.any():
        duplicates = out.loc[duplicate_mask, ["ticker", "fiscal_quarter", "source_name"]].to_dict("records")
        raise ValueError(f"Duplicate financial records detected: {duplicates}")

    return out
