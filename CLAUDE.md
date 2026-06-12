# CLAUDE.md

> Working brain for the Larridin × CMU capstone project. Shared context between Ian and Claude Code. This file evolves as we learn more — defaults here are starting points, not commitments. When something stops making sense, we update the file together.

---

## How We Work Together

A few working preferences worth knowing up front:

- **Discuss before moving phases.** When the current phase feels close to done, let's pause and talk through the next phase before diving in. Quick alignment beats course-correcting later.
- **Confirm before destructive actions on shared resources.** Especially for Supabase: deleting data, dropping tables, or changing schema. Read operations and inserting new data are fine without confirmation; anything that destroys or alters existing state, let's confirm first.
- **Flag surprises early.** If something in the data, methodology, or literature doesn't match what this file says, bring it up — defaults here are starting points, not rules.
- **Honest reporting over good-looking results.** This is a research study, not a marketing exercise. Negative, weak, or mixed findings are valid outcomes and should be reported as such.
- **Watch for look-ahead bias in everything we backtest.** Any time we use historical scores or features, double-check that the values were actually knowable at that point in time. This is the most common way studies like this go wrong.
- **Cost-aware LLM use.** When running LLM extraction at scale, default to a cheaper model (Haiku) for the first pass and reserve the stronger model (Sonnet or above) for hard cases or final-pass verification. Cache aggressively.
- **When blocked on Larridin's side, escalate to Ian.** If we hit something that needs Ameya's input (data, API keys, missing context), surface it and we'll figure out the right ask together rather than guessing.

---

## What This Project Is

We're testing whether Larridin's AI adoption signals — quantitative scores measuring how publicly traded companies are adopting AI — can predict those companies' future financial performance.

Framed in research terms: this is an **alternative-data factor research study**. AI adoption is the candidate signal; corporate financial performance (stock returns, revenue growth, margin expansion, revenue per employee) is the outcome being predicted. Methodologically, the core analysis is **classical quantitative finance / econometrics**, not machine learning — methods like rank correlation, portfolio sorts, and cross-sectional regression. The AI/LLM work lives upstream (signal extraction from public documents) and optionally downstream (an agentic workflow that explains findings).

**Primary deliverable: a research paper** (LaTeX). Dashboard and agentic workflow come later, after the analysis is solid.

### What Larridin Does (brief context)

Larridin is an early-stage SF startup building independent measurement infrastructure for enterprise AI adoption. They score public companies on AI adoption using public data. Their broader business is separate from this project — what matters for us is that they have a proprietary scoring framework, and we're testing whether those scores have predictive power.

### Research Posture

The honest framing of this study is **exploratory**, not confirmatory. Signals may have strong predictive power, weak power, or none — possibly varying by company size, industry, or outcome type. All results, including null or weak ones, are valid findings worth reporting.

A genuinely interesting paper here probably looks less like "we proved the signals work" and more like "we tested the signals rigorously and here's what we found, including what doesn't work and why." This posture also shapes methodology: we resist temptations to flex specifications until results look good.

---

## Repository

Our teammate has already built a **relatively mature scaffolding** — not an empty skeleton. As of 2026-06-08 the full pipeline exists in code (built largely via Codex; see `AGENTS.md` and `docs/01_PHASED_CODING_PROMPTS.md`, the build prompt-pack). What's missing is **real data, real results, and the paper** — every committed dataset today is synthetic sample data for smoke tests.

Before making structural changes, review the existing repo and reuse what's there rather than rebuilding. Suggested order:

1. **Read this file first** for project context and direction.
2. **Then explore the repo** — `README.md`, the `docs/` folder, and the `src/ai_impact_research/` package.
3. **Flag conflicts or improvements** before changing anything. If existing structure conflicts with this file, talk to Ian — we decide together which to adjust.

### What's in the repo

```text
src/ai_impact_research/   # Python package — the whole pipeline lives here
  ingestion/              # larridin · market_data · financials · job_postings importers (CSV now; API stubs for later)
  processing/             # panel_builder (company-quarter panel), identifiers, sampling
  analysis/               # ic · backtest · regressions · robustness · plots
  llm/                    # extract · schemas · eval + versioned prompts/
  dashboard/              # Streamlit app + 5 pages (Overview · Company Explorer · Signal Analysis · Backtest · Methodology)
  agent/                  # deterministic ticker-level report generator
  db/                     # connection · schema · models
scripts/                  # CLI entry points: bootstrap → build_panel → run_baseline_analysis → robustness → report
tests/                    # ~22 pytest files (schema contract, panel timing, IC, backtest, …)
docs/                     # charter, architecture, data sources/dictionary, methodology, LLM rubric, dashboard spec, responsible-AI
infra/                    # db_schema.sql (Postgres) + deployment notes
configs/                  # base.yaml
data/samples/             # SYNTHETIC sample CSVs only (e.g. synthetic_larridin_sample) — no real data yet
reports/                  # interim findings, sample report, final_paper_outline.qmd
```

Key implication: the work ahead is **less "build the pipeline" and more "feed it real data, run the analysis, write the paper."** When a task sounds like building a component, first check whether it already exists under `src/ai_impact_research/`.

### Working posture given this repo

The scaffolding runs well ahead of the research, so for now (agreed 2026-06-08):

- **The product layer is frozen.** Don't touch the dashboard or the report agent (Phases 9–10) until there's a finding robust enough to present. Building presentation on synthetic or preliminary data manufactures false confidence — exactly what an exploratory study should avoid.
- **Schema, panel, and analysis modules are a draft, not a contract.** Validate them against the first slice of real data and be ready to change column names, outcome definitions, even the panel grain. Never bend the analysis to fit the pre-built structure — that's the "flex specifications until results look good" trap.
- **When real data lands, validate before running the machine.** Order: point-in-time check → coverage / missingness / distribution sanity → is there any signal at all → only then IC / regression / backtest. Resist the temptation of a one-click backtest on day one.

### Known inconsistencies (audited 2026-06-08)

- ✅ **Resolved** — two docs shared the `05_` prefix; the LLM rubric is now `08_LLM_SIGNAL_RUBRIC.md` (dashboard reference updated to match).
- ✅ **Resolved** — `docs/01_PHASED_CODING_PROMPTS.md` had stale cross-references; it now carries a header marking it a historical build prompt-pack and points to README/CLAUDE.md for current structure.
- ⏳ **Open, deferred on purpose** — the panel's outcome columns drift across **four files in two conventions**: `panel_builder.py` + `docs/04_DATA_DICTIONARY.md` use `future_revenue_growth_qoq` / `composite_ai_score` / `snapshot_date`+`prediction_date`, while `infra/db_schema.sql` + `configs/base.yaml` use `revenue_growth` / `operating_margin_delta` / `revenue_per_employee_growth` / `headcount_growth` / `ai_composite_score` / `panel_date`. `panel_builder.py` is the runtime truth. Real bug, but per the "schema is a draft" posture we unify it while wiring up real-data analysis, not now — just **don't assume any single file is canonical**.
- ⏳ **Open** — the local working copy is not yet a git repo, though `.github/workflows/ci.yml` exists. `git init` + remote needed for CI/collaboration; do when Ian's ready.
- ℹ️ **By design** — phase numbering differs across this file, `docs/01`, and the code (which references phases 9/11/14). **This file's phases are the source of truth for us;** the doc/code numbers just reflect the Codex build order.

---

## Project Structure: Two Tracks

The work splits into two parallel tracks based on what we can do at any given moment:

**Track A — Self-driven work** (things we can build now with public data and our own tooling)

**Track B — Larridin-dependent work** (things that require their data, scores, or Supabase access)

We push Track A as far as possible while waiting on Track B unblocks. When stuck on Track B, escalate to Ian rather than guess.

**Status (2026-06-08):** Track A's code skeleton is essentially built. Track B is about to unblock — Supabase access is expected **this afternoon**. Once it lands, the immediate next step is **data collection**: point the existing ingestion pipelines at real sources and Supabase instead of synthetic samples.

---

## Phases

Logical phases, not time-bound steps. Some can overlap. The point is shared awareness of what's done and what's next — not rigid sequencing.

### Phase 1 — Setup & Orientation

**Track:** A

**Status (2026-06-08):** Largely complete. Repo reviewed, conventions understood, scaffolding mapped, open questions logged below. Remaining item is resolving point-in-time data integrity once we see the Supabase schema.

**Goal:** Have a working environment, a shared understanding of the repo, and open methodology questions clearly listed.

**In scope:**
- Get the repo running locally; confirm conventions our teammate has set up
- Read existing scaffolding; align with it where reasonable
- Confirm tooling defaults (Python, LaTeX for the paper, Anthropic API as primary LLM)
- Document any open methodology questions that affect later phases

**Discuss before exit:**
- Have we surfaced everything we don't yet know — especially around point-in-time data integrity?

---

### Phase 2 — Data Collection Pipelines

**Track:** A (mostly). Some pipelines may need refinement once we know Larridin's exact company universe — but the v1 universe is **S&P 500**, which is public and well-defined, so we can start now.

**Status (2026-06-08): this is the active phase.** The ingestion modules already exist in `src/ai_impact_research/ingestion/` (currently CSV-based, with API stubs for SEC/market/vendor sources). The work is **wiring them to real sources and Supabase**, not building from scratch. Supabase access expected this afternoon — that unblocks writing collected data to the shared DB instead of local samples.

**Goal:** Automated, reproducible pipelines that pull raw data from public sources into structured storage.

**Sources to cover:**
- **SEC EDGAR** — 10-K and 10-Q filings; structured fundamentals via the `companyfacts` API
- **Earnings call transcripts** — investigate public sources (Motley Fool, company IR pages, Seeking Alpha)
- **Hiring data** — company career pages, public job listings
- **News** — GDELT, RSS feeds, or other systematic sources
- **Financial market data** — Yahoo Finance (`yfinance`) for prices and returns

**Design notes:**
- Store everything keyed by company identifier (CIK or ticker) and date, so we can join cleanly later
- Build idempotent pipelines (re-runnable without duplication)
- For high-volume sources (e.g., a single company with thousands of job postings), design a defensible sampling strategy — don't full-scan when it explodes costs
- Storage destination is **Supabase** (see Supabase section below). Once we have access, pipelines should write directly there. In the meantime, local Parquet/CSV is fine as a staging step

**Discuss before exit:**
- Pipelines working on a small test set before scaling?
- Defensible sampling strategy for high-volume sources?

---

### Phase 3 — Signal Extraction (LLM)

**Track:** A — we can prototype on any sample of S&P 500 companies; final extraction also runs on S&P 500.

**Goal:** Convert raw unstructured text into structured AI-adoption signals.

**Signals to build (working list, will refine):**
- The 4 Larridin dimensions: AI Adoption maturity, AI Fluency, AI Impact / strategic initiatives, AI Hiring signals
- New candidate signals: AI capital expenditure, executive sentiment on AI in earnings calls, competitor benchmarking language, concreteness of AI claims (specific deployments vs. vague aspirations)

**Important context on scoring rubric:**
Larridin does not have a formal scoring rubric. Ameya's approach is to let the LLM score directly on a 1–5 scale. **This means our prompt engineering effectively IS the rubric.** When we write the extraction prompts — including descriptions of what each level (1, 2, 3, 4, 5) means, example cases, and constraints — we are defining the scoring methodology itself. This is a Phase 3 deliverable, not an external input we're waiting on.

**Scoring approach (current default):**
- Use a **1–5 scale** for all signals, LLM-scored with structured prompts
- Write prompts that are **objective, comprehensive, and clearly anchored** — each level should describe distinct, observable criteria, not vague intensity gradations
- Where possible, decompose a signal into sub-components (e.g., AI Adoption = tooling + training + usage) and score each — coarse scales give LLMs more consistent output than fine-grained ones
- We may later revisit whether to extract some signals in raw numeric form (e.g., dollar amounts for AI capex) instead of 1–5 — keep that flagged as a design decision

**Pipeline design:**
- Pre-filter raw documents to relevant sections before sending to LLM (don't feed 100-page 10-Ks whole; locate AI-relevant excerpts first)
- For each extraction call, return structured JSON with: score, reasoning, source_quote (for traceability and anti-hallucination check)
- Validate outputs: confirm source quotes actually exist in source text; check score is in expected range; flag low-confidence cases for retry or human review

**Evaluation work needed:**
- Consistency tests: run the same extraction twice on the same document — how often do we get the same score?
- Cross-industry / cross-size bias checks: does the LLM extract more reliably for large-cap tech than mid-cap industrials?
- Small human-validation sample: spot-check 50–100 extractions for accuracy

**Discuss before exit:**
- Are extraction outputs stable enough across reruns to use downstream?
- Are there systematic biases worth documenting in the paper's limitations section?

---

### Phase 4 — Preliminary Analysis (on what we have)

**Track:** A — initial sanity check before Larridin's official data arrives.

**Goal:** Run a small-scale version of the eventual analysis on the signals we've extracted ourselves. Surface any obvious issues with the methodology before committing to the full study.

**What to compute:**
- Basic descriptive statistics on the signals (distribution, missingness, correlations between signals)
- A first IC calculation on this universe
- Visual inspection of signal-vs-outcome relationships

**Why this phase exists:** Low-stakes dry run. If something's broken in pipeline or methodology, we'd much rather find out now than after burning LLM tokens scoring 500 companies.

**Discuss before exit:**
- Anything surprising in the distributions?
- Does the analysis pipeline work end-to-end on a small case?

---

### Phase 5 — Integrate Larridin's Official Data

**Track:** B — depends on Ameya providing Supabase access with their scores.

**Goal:** Bring Larridin's official 4-dimension scores into our pipeline, alongside our extended signals, on the S&P 500 universe.

**Critical methodology question to resolve here with Ameya:**
- **Are Larridin's historical scores point-in-time, or do they get revised over time?** If revised, do we have access to the snapshot of scores as they existed at each historical date?
- Without point-in-time data, backtesting suffers from look-ahead bias and results aren't credible. This is the single most important data-integrity question in the project. Until resolved, treat any backtesting results as preliminary.

**Output:** A clean panel dataset, indexed by (company, quarter), with both Larridin's signals and our new signals as features, plus forward-looking financial outcomes (returns, revenue growth, margin, revenue per employee) as targets.

**Discuss before exit:**
- Dataset clean enough to run real analysis on? Any unexpected gaps?

---

### Phase 6 — Core Modeling

**Track:** B — requires the full dataset from Phase 5.

**Goal:** The core statistical analysis. Four mandatory components:

1. **Information Coefficient (IC)** — per-quarter Spearman rank correlation between signals and forward outcomes; report mean, std, t-statistic, hit rate
2. **Portfolio sorts + Sharpe** — sort companies into quintiles by signal, construct long-short portfolios (Q5 minus Q1), measure Sharpe of the spread. Report standard errors honestly — short data history limits power
3. **Cross-sectional regressions with controls** — Fama-MacBeth regressions of forward outcomes on signals, controlling for company size, industry, and prior performance. The point of controls is to test whether signals have predictive power *beyond* what's already explained by size / sector / momentum
4. **Backtesting hygiene** — out-of-sample validation, walk-forward testing, multiple-hypothesis correction (Bonferroni or FDR), sensitivity checks

**Methodology defaults:**
- Always rank-transform features cross-sectionally within each quarter before modeling — robust to outliers and scale differences
- For numeric features that span large ranges (e.g., AI capex in dollars), apply log transformation and winsorization before ranking
- Categorical signals: one-hot encode or map to ordinal scale, depending on context
- Report results across multiple forward horizons (1, 2, 4 quarters) — the timing of any predictive effect is itself informative
- Test both market outcomes (returns) and fundamentals (revenue, margin, productivity) — they answer different questions and can give different answers

**Paper drafting starts here.** As methodology settles, draft the methodology section of the paper in parallel. Same for data/sources sections. Don't wait until everything's done to start writing.

**Discuss before exit:**
- What does the headline finding look like? Ready to test robustness, or iterate on modeling first?

---

### Phase 7 — Robustness & Segmentation

**Track:** B.

**Goal:** Pressure-test headline findings; find interesting story angles through segmentation.

**Robustness work:**
- Sensitivity checks: vary quintile cutoffs, normalization choices, control sets — does the finding hold?
- Out-of-sample / walk-forward results — does the model predict on data it wasn't fit on?
- Sub-sample stability: do results hold in the first half vs. second half of the time period?

**Segmentation (where the interesting stories often live):**
- By industry: does the signal predict better in some sectors than others?
- By company size: large-cap vs. mid-cap vs. small-cap
- By AI maturity: does the signal matter more for early-stage adopters than mature ones?
- A finding like "signal X works for mid-cap industrials but not large-cap tech because tech is already priced in" is much more interesting than "signal X works on average"

**Leading-vs-lagging tests (only if data depth allows):**
- Does the signal at time t predict outcomes at t+1, t+2, t+3? Different lags can reveal mechanism (e.g., AI hiring intensity leading efficiency gains by 2–3 quarters)
- With limited time-series depth, this may need to be deferred to future work — document it as such

**Cautions:**
- Segmentation multiplies hypothesis tests. With many cells, some will look "significant" by chance alone. Apply multiple-comparisons correction; treat segmented results as exploratory
- Don't go fishing through 100+ cells and report the 7 that sparkle. Pre-register a small number of segmentation cuts that make conceptual sense

**Paper results section advances substantially during this phase.**

**Discuss before exit:**
- Are findings robust enough to commit to in the paper?
- Have we found the angle that makes this paper distinctive?

---

### Phase 8 — Paper Finalization

**Track:** B.

**Goal:** A complete, defensible research paper.

**Sections to ensure are tight:**
- Abstract — clear statement of question, method, findings
- Introduction — motivate the problem, position against existing literature
- Data — sources, coverage, limitations (especially data window and point-in-time considerations)
- Methodology — every choice justified; mathematical specifications clear
- Results — headline findings + segmentation + robustness checks
- Limitations — be specific and honest. Data window, signal coverage gaps, statistical power constraints, methodological caveats
- Conclusion — what we learned, what's still open

**Paper format:** LaTeX. Specific template TBD — revisit when we know the target venue.

---

### Phase 9 — Dashboard (later)

**Track:** B, deferred.

**Status (2026-06-08): frozen.** A 5-page Streamlit dashboard already exists in `src/ai_impact_research/dashboard/` (from the Codex scaffold), but it runs on synthetic data. Leave it untouched until there's a finding robust enough to present — see "Working posture given this repo" above.

**Goal:** A web-accessible interface for exploring the findings. Streamlit or similar.

---

### Phase 10 — Agentic Workflow (later)

**Track:** B, deferred.

**Status (2026-06-08): frozen.** A deterministic ticker-level report generator already exists in `src/ai_impact_research/agent/`. Same rule as Phase 9 — don't build on it until the research produces something worth narrating.

**Goal:** A workflow that, given a company ticker, pulls relevant signals and financial data, runs the analysis, and produces a narrative summary.

---

## Supabase

Larridin uses Supabase (cloud-hosted Postgres) as the project's shared database. Ameya is setting it up. Once we have access, all data — raw collected text, extracted signals, Larridin's official scores, financial outcomes — lives here.

**Access expected 2026-06-08 (this afternoon).** First thing once it lands: inspect the schema (especially the Larridin scores table) for point-in-time integrity before loading anything — see the schema note below.

**Connection details and schema go here once we have them.** Until wired up, local Parquet/CSV under `data/` remains acceptable staging storage.

When Supabase is available:
- Use the official Supabase Python client (`pip install supabase`)
- Connection credentials (URL + service_role key) go in a `.env` file, **never committed to git**
- Confirm `.env` is in `.gitignore` before adding credentials
- Read operations and inserts are fine without confirmation; **confirm with Ian before destructive operations** (deleting data, dropping tables, schema changes)
- **Treat `infra/db_schema.sql` as local/reference only — do not create our tables on the shared Supabase.** It's already stale (see the column-drift note above). Inspect Larridin's real schema first; theirs is authoritative; reconcile ours to it.

**Schema design considerations for point-in-time integrity:**
When the schema arrives, immediately check whether scores include an `as_of_date` (or similar) field that captures when a score was published. If scores are versioned in place without history, that's the look-ahead bias risk we keep flagging — surface this to Ian so we can raise it with Ameya.

---

## Methodological Defaults

Quick reference. Each is a starting point; happy to revisit.

| Choice | Default | Reason |
|---|---|---|
| Company universe (v1) | S&P 500 | Public, well-defined; Ameya's starting point |
| Signal scoring scale | 1–5 (LLM-scored) | Coarse scales give more consistent LLM output than fine-grained ones |
| Scoring rubric source | Our prompt engineering | Larridin has no formal rubric; prompts are the rubric |
| Cross-sectional normalization | Rank-transform within each quarter | Robust to outliers; equates scales across features |
| Numeric signals with large ranges | Log → winsorize → rank | Handles skew and outliers before ranking |
| Primary correlation metric | Spearman (rank-based) IC | Scale-independent; standard in factor research |
| Portfolio sort buckets | Quintiles (5) | Standard in factor research; balance between resolution and stability |
| Regression method | Fama-MacBeth | Standard for cross-sectional studies |
| Controls | Size, industry, prior performance | Standard set for cross-sectional equity research |
| Backtesting | Out-of-sample + walk-forward | Standard hygiene against overfitting |
| Multiple hypothesis testing | Bonferroni or FDR correction | Necessary when running many segmented tests |
| LLM provider | Anthropic Claude | Default; matches Ameya's stack |
| LLM cost discipline | Haiku for first pass; Sonnet+ for hard cases | Cost-aware extraction at scale |
| Programming language | Python (pandas, scikit-learn, statsmodels) | Standard for quant research |
| Database | Supabase (Postgres) | Larridin-provided shared infrastructure |
| Paper writing format | LaTeX | Flexible; standard for academic writing |

---

## Open Questions

Living list. We update as questions resolve.

| Question | Why it matters | Status |
|---|---|---|
| Are Larridin's historical scores point-in-time, or do they get revised? | Critical for backtesting integrity. Naive backtests have look-ahead bias if scores change retroactively. | **Resolve 2026-06-08** when Supabase access lands — inspect the schema for `as_of_date`/snapshot history first thing |
| Should new signals stay 1–5, or should numeric signals (e.g., AI capex) be extracted in raw units? | Affects information preservation in modeling. | Default 1–5 for now; revisit later |
| For new signals we build, do they feed back into Larridin's tracker, or stay internal to our study? | Affects rubric design and stakes. | Open — to clarify with Ameya |
| What's the refresh cadence of Larridin's scores during the project? | Affects how much new data accumulates while we're working. | Open — Ameya mentioned May/Jun/Jul/Sep snapshots planned |
| Is S&P 500 the v1 scope or also the final universe? | Affects pipeline design for scale. | Open — Ameya proposed S&P 500 as starting point; final scope TBD |
| What's the target venue for the paper? | Affects style, depth, structure. | TBD — revisit closer to Phase 8 |

---

## Decisions Log

Running log of methodology and design decisions, with brief rationale. Mark stale entries as superseded; when this section grows past ~30 entries, prune together with Ian.

Format: `[date | status] decision — brief reason`

- `[TBD | active]` Project v1 scope: S&P 500 companies. (Proposed by Ameya; we agreed.)
- `[TBD | active]` Default LLM scoring scale: 1–5. May revisit for numeric signals.
- `[TBD | active]` Scoring rubric: our prompt engineering itself. No external rubric exists.
- `[TBD | active]` Programming language: Python. Paper: LaTeX.
- `[TBD | active]` LLM defaults: Anthropic Claude; Haiku for first pass, Sonnet+ for hard cases.
- `[TBD | active]` Database: Supabase (Larridin-provided), once available.
- `[TBD | active]` Research framing: exploratory factor study, not confirmatory validation. Honest reporting of weak/null/mixed results is expected and acceptable.
- `[TBD | active]` Dashboard and agentic workflow deferred until after paper is solid.
- `[2026-06-08 | active]` Repo is already a mature scaffolding — the full pipeline exists in code (built via Codex). Work shifts from building the pipeline to feeding it real data, producing results, and writing the paper. Reuse existing modules; check before rebuilding.
- `[2026-06-08 | active]` Supabase access expected this afternoon. Immediate next step is real data collection through the existing ingestion pipelines; first action on access is a point-in-time schema check.
- `[2026-06-08 | active]` Product layer frozen: don't touch the dashboard (Phase 9) or report agent (Phase 10) until a robustness-surviving finding exists. Presentation built on synthetic/preliminary data manufactures false confidence.
- `[2026-06-08 | active]` Pre-built schema/panel/analysis are a draft to validate against real data, not a contract. When data lands, validate first (point-in-time → coverage/missingness → signal sanity) before running IC/regression/backtest; don't bend the analysis to fit existing code.
- `[2026-06-08 | done]` Doc hygiene: renamed `05_LLM_SIGNAL_RUBRIC.md` → `08_LLM_SIGNAL_RUBRIC.md` (resolved the duplicate `05_` prefix; updated the dashboard reference) and annotated `docs/01_PHASED_CODING_PROMPTS.md` as a historical build prompt-pack.
- `[2026-06-10 | active]` Real data located: Supabase project `mbyyempsotonpklaoxzw` (service_role REST keys in `.env`). 562 companies have Larridin `aiScores` (adoption/proficiency/impact + maturityIndex, evidence-backed) — but ALL assessed 2026-01-18/19: a single cross-section, no history. Hiring pipeline is a 7-company/1-month POC. Larridin's DB is **read-only** for us.
- `[2026-06-10 | active]` Study reframed to match data: cross-sectional — Jan-2026 scores (t0) → forward returns (1–5M horizons) + Q1-2026 fundamentals; plus our own forward monthly signal collection (Jun/Jul snapshots). Multi-quarter IC/backtest deferred until a panel accumulates.
- `[2026-06-10 | active]` Universe: Larridin's ~555 companies ∪ S&P 500 fill-in. Storage: our collected data in local files (Parquet/CSV) first; shared DB later if needed. Deadline: end of July 2026.
- `[2026-06-10 | active]` Signal extensions we build (Ameya's ask): SEC-filing/earnings-call LLM signals (their evidence is only ~3% SEC), systematic press collection, hiring scaled via Exa from 7→full universe monthly. Plus ticker/CIK mapping + financial outcomes (entirely absent from their DB).

---

## File Maintenance

This file grows with the project. Suggested update triggers:
- When entering a new phase, update its "Discuss before exit" outcomes and any new open questions
- When a default in the methodology table changes, update the row and add a corresponding Decisions Log entry
- When an open question resolves, move it to Decisions Log with the resolution
- When Decisions Log grows too long, prune together with Ian

This file is shared infrastructure — keeping it current is part of the work, not separate from it.
