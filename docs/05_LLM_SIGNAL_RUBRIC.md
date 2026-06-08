# LLM Signal Rubric

## Evidence-first extraction

The LLM should not directly invent a final score. It should first extract evidence, then map evidence to binary or categorical indicators, then aggregate to a 1–5 score.

## AI operational maturity score

| Score | Definition |
|---|---|
| 1 | No meaningful AI adoption evidence |
| 2 | Exploratory or vague AI language |
| 3 | Pilots or limited departmental use cases |
| 4 | Production use in multiple business functions |
| 5 | Enterprise-wide AI transformation with measurable business impact |

## Required output principles

- Every score must have evidence.
- Every evidence item must have source type, quote or paraphrase, business function, and confidence.
- Prompt version and model name must be stored.
- Low-confidence extractions should not be silently treated as high-quality data.
