from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field, model_validator

SourceType = Literal["sec_filing", "earnings_transcript", "job_posting", "news", "company_page"]


class EvidenceItem(BaseModel):
    claim_type: str = Field(..., description="Type of AI adoption claim")
    business_function: str | None = Field(None, description="Function affected, e.g. finance, HR, support")
    evidence_text: str = Field(..., min_length=5, description="Short quote or evidence paraphrase")
    confidence: float = Field(..., ge=0, le=1)


class SignalScores(BaseModel):
    ai_strategy_specificity: int = Field(..., ge=1, le=5)
    ai_operational_maturity: int = Field(..., ge=1, le=5)
    ai_capex_commitment: int = Field(..., ge=1, le=5)
    ai_workforce_training: int = Field(..., ge=1, le=5)


class AISignalExtraction(BaseModel):
    company: str
    ticker: str | None = None
    period: str
    source_document_id: str
    source_type: SourceType
    evidence_items: list[EvidenceItem]
    signal_scores: SignalScores
    model_name: str
    prompt_version: str
    overall_confidence: float = Field(..., ge=0, le=1)

    @model_validator(mode="after")
    def require_evidence(self) -> AISignalExtraction:
        if not self.evidence_items:
            raise ValueError("At least one evidence item is required for an AI signal extraction.")
        return self
