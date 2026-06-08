from __future__ import annotations

import json

from ai_impact_research.llm.schemas import AISignalExtraction


def validate_extraction_json(payload: str | dict) -> AISignalExtraction:
    if isinstance(payload, str):
        data = json.loads(payload)
    else:
        data = payload
    return AISignalExtraction.model_validate(data)


def extract_ai_signals_offline_stub(
    text: str,
    company: str,
    period: str,
    source_document_id: str,
    source_type: str,
) -> AISignalExtraction:
    """Deterministic stub for tests and local development.

    Replace this with an adapter around your LLM provider. Keep schema validation here.
    """
    evidence_text = text.strip().split(".")[0][:250] or "No meaningful text provided"
    payload = {
        "company": company,
        "ticker": None,
        "period": period,
        "source_document_id": source_document_id,
        "source_type": source_type,
        "evidence_items": [
            {
                "claim_type": "ai_mention",
                "business_function": None,
                "evidence_text": evidence_text,
                "confidence": 0.5,
            }
        ],
        "signal_scores": {
            "ai_strategy_specificity": 2,
            "ai_operational_maturity": 2,
            "ai_capex_commitment": 1,
            "ai_workforce_training": 1,
        },
        "model_name": "offline_stub",
        "prompt_version": "v0",
        "overall_confidence": 0.5,
    }
    return validate_extraction_json(payload)
