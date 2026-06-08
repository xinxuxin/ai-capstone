from __future__ import annotations

import argparse

from ai_impact_research.ingestion.financials import load_financials_csv
from ai_impact_research.io_utils import write_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize financial metrics export.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="data/interim/financials_normalized.csv")
    args = parser.parse_args()
    df = load_financials_csv(args.input)
    write_csv(df, args.output)
    print(f"Wrote {len(df):,} normalized financial rows to {args.output}")


if __name__ == "__main__":
    main()
