from __future__ import annotations

import pandas as pd
import statsmodels.formula.api as smf


def run_baseline_ols(
    panel: pd.DataFrame,
    signal: str,
    outcome: str,
    add_sector_fe: bool = True,
    add_quarter_fe: bool = True,
) -> pd.DataFrame:
    """Run a simple OLS regression and return a coefficient table.

    This is intentionally minimal. Production analysis should add controls and robust standard errors.
    """
    terms = [signal]
    if "market_cap" in panel.columns:
        panel = panel.copy()
        panel["log_market_cap"] = panel["market_cap"].where(panel["market_cap"] > 0).map(
            lambda x: None if pd.isna(x) else __import__("math").log(x)
        )
        terms.append("log_market_cap")
    if add_sector_fe and "sector" in panel.columns:
        terms.append("C(sector)")
    if add_quarter_fe and "score_quarter" in panel.columns:
        terms.append("C(score_quarter)")

    formula = f"{outcome} ~ " + " + ".join(terms)
    cols = [signal, outcome, *(["log_market_cap"] if "log_market_cap" in panel.columns else [])]
    data = panel.dropna(subset=[c for c in cols if c in panel.columns])
    if len(data) < 5:
        raise ValueError(f"Need at least 5 observations for OLS; got {len(data)}")
    model = smf.ols(formula=formula, data=data).fit()
    table = pd.DataFrame(
        {
            "term": model.params.index,
            "coef": model.params.values,
            "std_err": model.bse.values,
            "t_value": model.tvalues.values,
            "p_value": model.pvalues.values,
        }
    )
    return table
