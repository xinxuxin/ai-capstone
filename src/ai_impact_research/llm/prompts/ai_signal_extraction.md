# AI Signal Extraction Prompt

You are extracting AI adoption evidence from a public company source document.

Return only valid JSON matching the provided schema.

## Rules

1. Extract evidence before assigning scores.
2. Do not infer beyond the document.
3. Use a 1–5 scale only.
4. Every score must be supported by at least one evidence item.
5. If the evidence is vague, assign a lower score and lower confidence.
6. Store the source document id, model name, and prompt version.

## Score scale

1 = no meaningful evidence
2 = vague or exploratory language
3 = pilot or limited deployment
4 = production deployment in one or more functions
5 = enterprise-wide transformation with measurable impact
