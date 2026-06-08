from __future__ import annotations

import argparse

from ai_impact_research.ingestion.market_data import load_market_prices_csv
from ai_impact_research.io_utils import write_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize market data export.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="data/interim/market_prices_normalized.csv")
    args = parser.parse_args()
    df = load_market_prices_csv(args.input)
    write_csv(df, args.output)
    print(f"Wrote {len(df):,} normalized market rows to {args.output}")


if __name__ == "__main__":
    main()
