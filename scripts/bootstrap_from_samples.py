from __future__ import annotations

import pandas as pd

from ai_impact_research.config import load_settings
from ai_impact_research.io_utils import write_csv
from ai_impact_research.processing.panel_builder import build_analytic_panel


def main() -> None:
    settings = load_settings()
    samples = settings.samples_dir
    companies = pd.read_csv(samples / "companies.csv")
    scores = pd.read_csv(samples / "larridin_scores.csv")
    prices = pd.read_csv(samples / "market_prices.csv")
    financials = pd.read_csv(samples / "fundamentals.csv")
    panel = build_analytic_panel(companies, scores, prices, financials)
    output = write_csv(panel, settings.processed_dir / "analytic_panel.csv")
    print(f"Wrote {len(panel):,} panel rows to {output}")


if __name__ == "__main__":
    main()
