from __future__ import annotations

import pandas as pd


def normalize_companies(df: pd.DataFrame) -> pd.DataFrame:
    required = {"company_id", "ticker", "name"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Companies file missing required columns: {sorted(missing)}")
    out = df.copy()
    out["ticker"] = out["ticker"].astype(str).str.upper().str.strip()
    out["company_id"] = out["company_id"].astype(str).str.strip()
    return out


def attach_company_id(df: pd.DataFrame, companies: pd.DataFrame) -> pd.DataFrame:
    companies_norm = normalize_companies(companies)
    out = df.copy()
    out["ticker"] = out["ticker"].astype(str).str.upper().str.strip()
    mapped = out.merge(companies_norm[["company_id", "ticker"]], on="ticker", how="left")
    missing = mapped["company_id"].isna()
    if missing.any():
        missing_tickers = sorted(mapped.loc[missing, "ticker"].dropna().unique())
        raise ValueError(f"Unable to map tickers to company_id: {missing_tickers}")
    return mapped
