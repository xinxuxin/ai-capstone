import pandas as pd
import pytest

from ai_impact_research.ingestion.larridin import normalize_larridin_scores


def _valid_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "ticker": ["msft"],
            "company_name": ["Microsoft Corporation"],
            "snapshot_date": ["2025-03-31"],
            "ai_adoption_score": [5],
            "ai_fluency_score": [5],
            "ai_impact_score": [5],
            "ai_hiring_score": [4],
        }
    )


def test_normalize_larridin_scores() -> None:
    out = normalize_larridin_scores(_valid_df())
    assert out.loc[0, "ticker"] == "MSFT"
    assert out.loc[0, "score_quarter"] == "2025Q1"
    assert "available_at" in out.columns


def test_invalid_score_raises() -> None:
    df = _valid_df()
    df.loc[0, "ai_hiring_score"] = 6
    with pytest.raises(ValueError):
        normalize_larridin_scores(df)
