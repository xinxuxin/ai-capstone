from __future__ import annotations

import pandas as pd

from ai_impact_research.time_utils import to_calendar_quarter

REQUIRED_MARKET_COLUMNS = ["ticker", "price_date", "adjusted_close"]


def load_market_prices_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return normalize_market_prices(df)


def normalize_market_prices(df: pd.DataFrame) -> pd.DataFrame:
    missing = set(REQUIRED_MARKET_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Market data file is missing required columns: {sorted(missing)}")

    out = df.copy()
    out["ticker"] = out["ticker"].astype(str).str.upper().str.strip()
    out["price_date"] = pd.to_datetime(out["price_date"]).dt.date
    out["price_quarter"] = to_calendar_quarter(pd.Series(out["price_date"]))
    out["adjusted_close"] = pd.to_numeric(out["adjusted_close"], errors="raise")

    if "volume" not in out.columns:
        out["volume"] = None
    if "source_name" not in out.columns:
        out["source_name"] = "market_data_export"
    if "available_at" not in out.columns:
        out["available_at"] = pd.to_datetime(out["price_date"])
    else:
        out["available_at"] = pd.to_datetime(out["available_at"])

    duplicate_mask = out.duplicated(["ticker", "price_date", "source_name"], keep=False)
    if duplicate_mask.any():
        duplicates = out.loc[duplicate_mask, ["ticker", "price_date", "source_name"]].to_dict("records")
        raise ValueError(f"Duplicate market price records detected: {duplicates}")

    return out
