import pytest

from ai_impact_research.llm.extract import validate_extraction_json


def test_llm_schema_requires_evidence() -> None:
    payload = {
        "company": "Sample Corp",
        "period": "2025Q1",
        "source_document_id": "doc1",
        "source_type": "news",
        "evidence_items": [],
        "signal_scores": {
            "ai_strategy_specificity": 2,
            "ai_operational_maturity": 2,
            "ai_capex_commitment": 1,
            "ai_workforce_training": 1,
        },
        "model_name": "test",
        "prompt_version": "v0",
        "overall_confidence": 0.5,
    }
    with pytest.raises(ValueError):
        validate_extraction_json(payload)
