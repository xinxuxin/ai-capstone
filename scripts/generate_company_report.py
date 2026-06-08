from __future__ import annotations

import argparse
import pandas as pd

from ai_impact_research.agent.company_report_agent import generate_company_report


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a ticker-level research report.")
    parser.add_argument("--panel", default="data/processed/analytic_panel.csv")
    parser.add_argument("--ticker", required=True)
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    panel = pd.read_csv(args.panel)
    report = generate_company_report(panel, args.ticker)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Wrote report to {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
