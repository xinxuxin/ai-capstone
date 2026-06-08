from __future__ import annotations

from ai_impact_research.llm.schemas import AISignalExtraction


def evidence_coverage(extractions: list[AISignalExtraction]) -> float:
    if not extractions:
        return 0.0
    with_evidence = sum(1 for extraction in extractions if extraction.evidence_items)
    return with_evidence / len(extractions)
