from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import json

import pandas as pd

from ai_impact_research.analysis.backtest import long_short_returns, quintile_returns
from ai_impact_research.analysis.ic import compute_ic_by_period, summarize_ic
from ai_impact_research.io_utils import write_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Run baseline IC and quintile backtest.")
    parser.add_argument("--panel", default="data/processed/analytic_panel.csv")
    parser.add_argument("--signal", default="ai_composite_score")
    parser.add_argument("--outcome", default="fwd_return_1q")
    parser.add_argument("--output-dir", default="reports/tables")
    args = parser.parse_args()

    panel = pd.read_csv(args.panel)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    ic = compute_ic_by_period(panel, args.signal, args.outcome)
    q = quintile_returns(panel, args.signal, args.outcome)
    ls = long_short_returns(q)

    write_csv(ic, output_dir / "ic_by_period.csv")
    write_csv(q, output_dir / "quintile_returns.csv")
    write_csv(ls, output_dir / "long_short_returns.csv")

    metadata = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "panel": args.panel,
        "signal": args.signal,
        "outcome": args.outcome,
        "ic_summary": summarize_ic(ic),
        "caveat": "Hypothetical research analysis only; not investment advice.",
    }
    (output_dir / "analysis_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
