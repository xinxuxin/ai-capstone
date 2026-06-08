from __future__ import annotations

from ai_impact_research.llm.extract import extract_ai_signals_offline_stub


SAMPLE_TEXT = "The company is piloting generative AI in customer support and software engineering workflows."


def main() -> None:
    extraction = extract_ai_signals_offline_stub(
        text=SAMPLE_TEXT,
        company="Sample Corp",
        period="2025Q4",
        source_document_id="sample_doc_001",
        source_type="earnings_transcript",
    )
    print(extraction.model_dump_json(indent=2))


if __name__ == "__main__":
    main()
