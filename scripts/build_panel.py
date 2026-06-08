from __future__ import annotations

import argparse
import pandas as pd

from ai_impact_research.io_utils import write_csv
from ai_impact_research.processing.panel_builder import build_analytic_panel


def main() -> None:
    parser = argparse.ArgumentParser(description="Build analytical panel from CSV inputs.")
    parser.add_argument("--companies", required=True)
    parser.add_argument("--scores", required=True)
    parser.add_argument("--prices", required=True)
    parser.add_argument("--financials", required=True)
    parser.add_argument("--output", default="data/processed/analytic_panel.csv")
    args = parser.parse_args()

    panel = build_analytic_panel(
        pd.read_csv(args.companies),
        pd.read_csv(args.scores),
        pd.read_csv(args.prices),
        pd.read_csv(args.financials),
    )
    output = write_csv(panel, args.output)
    print(f"Wrote {len(panel):,} rows to {output}")


if __name__ == "__main__":
    main()
