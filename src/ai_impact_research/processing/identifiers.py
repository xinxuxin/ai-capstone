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
    existing_company_id = out["company_id"] if "company_id" in out.columns else None
    if "company_id" in out.columns:
        out = out.drop(columns=["company_id"])
    mapped = out.merge(companies_norm[["company_id", "ticker"]], on="ticker", how="left")
    if existing_company_id is not None:
        mapped["company_id"] = existing_company_id.combine_first(mapped["company_id"])
    missing = mapped["company_id"].isna()
    if missing.any():
        missing_tickers = sorted(mapped.loc[missing, "ticker"].dropna().unique())
        raise ValueError(f"Unable to map tickers to company_id: {missing_tickers}")
    return mapped
