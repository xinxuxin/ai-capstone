from ai_impact_research.db.schema import CORE_TABLES


def test_core_schema_contract_contains_required_tables() -> None:
    assert "companies" in CORE_TABLES
    assert "larridin_scores" in CORE_TABLES
    assert "financial_metrics" in CORE_TABLES
    assert "market_prices" in CORE_TABLES
    assert "available_at" in CORE_TABLES["larridin_scores"]
