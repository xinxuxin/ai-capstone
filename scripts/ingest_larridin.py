from __future__ import annotations

import argparse
from ai_impact_research.ingestion.larridin import load_larridin_scores_csv
from ai_impact_research.io_utils import write_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize Larridin score export.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", default="data/interim/larridin_scores_normalized.csv")
    args = parser.parse_args()
    df = load_larridin_scores_csv(args.input)
    write_csv(df, args.output)
    print(f"Wrote {len(df):,} normalized score rows to {args.output}")


if __name__ == "__main__":
    main()
