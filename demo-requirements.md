# Credit Memo Demo — Requirements

**Version:** 2.1 (two-phase structure)
**Scope:** Weekend hackathon (Phase 1) + extended sprint (Phase 2)
**Phase:** This document primarily covers **Phase 1 — Crack the PDF** (single credit memo extraction and verification). Phase 2 preview is at the end.
**Input:** `Sample-Enhanced-Memo.pdf` (22 pages, 1.1 MB)
**Companion to:** [Strategic Brief](credit-memo-extraction-explainer.html) — frozen as the source of high-level requirements

---

## How to read this document

This document has two zones.

**The Contract** is locked. Every implementation must satisfy everything in it, regardless of language, framework, or architectural decomposition. Anything the audience sees at the demo lives here — the input, the output schema, the arithmetic checks, the deliverables.

**Reference Implementation** is guidance only. It exists to help teams get started, but any layer — language, libraries, agent framework, even the specialist-team architecture itself — can be substituted for an equivalent that hits The Contract. If in doubt, the proofreader checks in §8 are the ultimate arbiter of whether an implementation satisfies the requirements.

---

## Pick a format

This demo can run in two modes. Decide on Saturday morning at kickoff, after the group has read The Contract together.

### Unified team
*One codebase · One demo*

- **Structure:** one shared repo, split into roles (extraction, agent, validator, UX/demo)
- **Output:** one integrated demo at the end
- **Best for:** smaller groups (2–4 people), teams that haven't worked together before, tight coordination
- **Strength:** fastest path to a single polished story
- **Risk:** a bug in one layer breaks the whole demo

### Bake-off
*Multiple stacks · Same contract*

- **Structure:** 2–3 independent pairs, each picking their own stack, architecture, and approach
- **Output:** each pair demos for 5 minutes, followed by a comparative retrospective
- **Best for:** larger groups (5–8 people), mixed skill backgrounds, learning-focused hackathons
- **Strength:** direct comparison — which stack was fastest, which caught the hardest edge cases, which recovery path was cleverest
- **Risk:** more scaffolding up front; if one pair's implementation breaks, the others still work

*The rest of this document works for either mode.*

---

# THE CONTRACT — Zone 1 of 2 (LOCKED)

*Everything in this zone must be satisfied by every implementation, regardless of technology choice, architecture, or format. The audience sees all of this at the demo.*

---

## 1. Purpose [LOCKED]

Prove the refinery works. One sample credit memo goes in; verified structured data comes out. Every field traces back to a page in the source PDF. Every number reconciles against the proofreader's arithmetic checks. Nothing silently wrong.

This is the credibility anchor for Stage 2 of the supply chain in the strategic brief. Stages 1, 3, and 4 are acknowledged and out of scope.

## 2. Supply chain position [LOCKED]

The demo scopes to **Stage 2 (Refinery)** of the four-stage supply chain:

```
[Archive] → [Refinery] → [Data Estate] → [Factory]
             ~~~~~~~~
             WEEKEND
```

Stages 1, 3, and 4 are acknowledged but out of scope. See the strategic brief diagram for full context.

## 3. The sample document [LOCKED]

22-page MBFS Credit Memorandum for a $514,500 multifamily real estate refinance in Philadelphia. Contains the full mixed-content profile the refinery needs to handle.

| Field | Value |
|---|---|
| File | `Sample-Enhanced-Memo.pdf` (22 pages, 1.1 MB) |
| Borrower | Real estate holding company |
| Loan | $514,500 @ 4.75% fixed, 5yr / 30yr amort |
| Collateral | Multifamily 5+ unit, est. value $735,000, 70% LTV |
| Guarantors | Two, each 50% ownership; credit 734 and 775 |
| Risk rating | 4-Pass (scored 3.55) |
| Borrower DSCR | 0.82x (2021), 1.02x pro-forma |
| Global DSCR | 1.59x (2021), 1.60x pro-forma |
| Gross rents | $53,400/yr ($4,450/mo across six units) |

## 4. Scope [LOCKED]

### In scope
- Processing one PDF end-to-end
- Content-aware page routing
- Header field extraction
- Three financial tables
- Narrative sections (strengths, weaknesses, analyst notes, loan purpose)
- Arithmetic verification with a reported result per check
- At least one observable recovered error
- Structured JSON output matching the §7 schema
- Source-page provenance for every populated field
- A five-minute demo walkthrough

### Out of scope (Phase 1)
- Any Stage 3 (data estate) work
- Any Stage 4 (insight agents)
- AuthN/AuthZ, multi-user, persistence beyond local files
- Production observability, cost tracking, SLAs
- Template drift across memo versions
- PII handling, anonymization, compliance review
- Exhaustive field extraction — only what's needed to run §8

### Phase 2 scope (see §17 for details)
- Multiple documents and cross-document linking (PFS, Rent Roll, Appraisal, scanned docs)
- Cross-document verification and reconciliation
- Origination vs. servicing timeline dimension

## 5. Success criteria [LOCKED]

At the end of Sunday, the demo must produce the following observable outcomes, regardless of how the system is built:

1. Running the system on `Sample-Enhanced-Memo.pdf` produces a JSON document matching the schema in §7.
2. Every populated field carries a source-page reference back to the PDF.
3. All mandatory checks in §8 pass, and the validation report is visible in the demo surface.
4. At least one recovered error is visible in the output — a case where an initial extraction attempt produced an incorrect value, the incorrect value was detected, and a corrected value was produced.
5. A reviewer can point at any field in the output and be shown the specific page of the source PDF it came from.
6. A five-minute walkthrough maps each demo step back to the strategic brief's four-stage supply chain.

## 6. Functional outcomes [LOCKED]

What must be true of the system when the demo runs, **regardless of how the system is built**. An implementation that uses a single LLM pass, a specialist-team architecture, a state machine, or any other pattern is acceptable as long as every outcome below is observable in the final output.

### FO1 — Content-aware routing

Every page of the source PDF must be classified by content type (at minimum: `form`, `table`, `narrative`, `visual`, `skip`), and the classification must influence how that page is extracted. An implementation that processes every page with one tool and ignores content type does not satisfy this outcome.

### FO2 — Header field extraction

The following fields must appear in the output with correct values drawn from pages 1–2. Each field must carry a source-page reference.

- Memo date, credit union, relationship manager, analyst, borrower name
- Loan amount, rate, rate type, term, amortization
- Collateral type, address, estimated value, LTV, purchase price, lien position
- NAICS code, risk rating, aggregate relationship
- Borrower DSCR and global DSCR (both actual and pro-forma)
- Guarantors: name, credit score, ownership percentage
- Sources & Uses rows with amounts

### FO3 — Financial table extraction

Three tables must be extracted into structured form (column → value) with correct numeric values and source-page references:

- **Guarantor 1 Net Worth** (page 4)
- **Guarantor 1 Personal Cash Flow** (page 5) — must include the 2018, 2019, 2020, and Projected columns
- **Global Cash Flow** (page 12) — must include the Borrower, Guarantor 1, Guarantor 2, and Total rows across 2019, 2020, 2021, and Projected columns

### FO4 — Narrative extraction

The following narrative elements must be extracted from the appropriate pages with source-page references:

- Borrower background paragraph
- Operating statement narrative (rent history, expenses)
- Strengths list (as discrete items)
- Weaknesses list (as discrete items)
- Analyst notes / CU recommendations
- Stated loan purpose

### FO5 — Arithmetic verification

All mandatory checks from §8 must be executed against the extracted data and reported in the output, with expected value, observed value, and pass/fail status. Implementations may add additional checks beyond §8 but must not remove any.

### FO6 — Observable error recovery

The demo must include at least one observable case where an initial extraction attempt produced an incorrect value, the incorrect value was detected, and a corrected value was produced. The recovery must be visible in the final output — a reviewer should be able to see that the system tried one approach, the result failed a check or was flagged, and a different approach succeeded. **How** the detection and correction happen is an implementation choice.

### FO7 — Structured output with provenance

The final output must match the schema in §7. Every populated field must carry a reference back to the source page and the method/agent/tool that produced it. A reviewer must be able to ask "where did this value come from?" for any field and receive a specific page answer.

## 7. Output schema [LOCKED]

The schema below is expressed in Python/Pydantic. Teams using other languages must produce JSON that is **shape-compatible** — same field names, same structure, same nesting. The schema is deliberately flat and minimal.

```python
from pydantic import BaseModel, Field
from typing import Literal

class SourceRef(BaseModel):
    page: int
    agent: str          # e.g. "form", "table", "narrative", "visual", or custom
    method: str         # e.g. "pdfplumber-lattice", "claude-vision", "regex"
    confidence: float = 1.0

class Field_(BaseModel):
    value: str | float | int | None
    source: SourceRef

class Guarantor(BaseModel):
    name: Field_
    credit_score: Field_
    ownership_pct: Field_
    stated_net_worth: Field_ | None = None

class LoanTerms(BaseModel):
    amount: Field_
    rate: Field_
    rate_type: Field_
    term_years: Field_
    amortization_years: Field_

class Collateral(BaseModel):
    asset_type: Field_
    address: Field_
    estimated_value: Field_
    ltv_pct: Field_
    lien_position: Field_

class FinancialTable(BaseModel):
    name: str
    rows: list[dict]    # column name -> value
    source: SourceRef

class ValidationCheck(BaseModel):
    name: str
    formula: str
    expected: float | str
    observed: float | str
    status: Literal["pass", "fail", "warning"]
    source_pages: list[int]

class CreditMemo(BaseModel):
    document_id: str
    memo_date: Field_
    borrower_name: Field_
    loan: LoanTerms
    collateral: Collateral
    guarantors: list[Guarantor]
    sources: list[dict] = Field(default_factory=list)
    uses: list[dict] = Field(default_factory=list)
    tables: list[FinancialTable] = Field(default_factory=list)
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    analyst_notes: str | None = None
    validation: list[ValidationCheck]
```

## 8. Proofreader checks [LOCKED]

Mandatory arithmetic checks against the sample document. Expected values are the ground truth — if an implementation produces something different, either the extraction is wrong or the check is wrong. Either way, the demo does not ship until both agree.

Tolerance: ±1 unit for integer dollar totals, ±0.01 for ratios.

| # | Check | Formula | Expected |
|---|---|---|---|
| C1 | Sources = Uses | `sum(sources.amount) == sum(uses.amount)` | `$514,500 == $514,500` |
| C2 | G1 stated net worth | `total_assets − total_liabilities` | `$4,760,177 − $1,070,737 = $3,689,440` |
| C3 | G1 adjusted net worth | `assets − liabilities − adjustments` | `$4,760,177 − $1,070,737 − $425,000 = $3,264,440` |
| C4 | G2 stated net worth | `total_assets − total_liabilities` | `$1,546,440 − $656,140 = $890,300` |
| C5 | Ownership sum | `sum(guarantor.ownership_pct) == 100` | `50 + 50 = 100` |
| C6 | G1 DSCR 2020 | `gross_cash_flow / total_debt` | `$111,831 / $33,120 ≈ 3.38` |
| C7 | Global DSCR 2019 | `total_combined_cash / total_combined_debt_service` | `$189,500 / $66,050 ≈ 2.87` |
| C8 | Rent roll sum | `sum(unit_rents) * 12` | `($800+$650+$650+$800+$750+$800) × 12 = $53,400` |
| C9 | Cross-page rents | narrative (p8) == transactional table (p17) | `$53,400` on both |

## 9. Deliverables [LOCKED]

Every implementation — whether in unified-team or bake-off mode — delivers the following by end of weekend:

- [ ] Git repository with a one-command bootstrap (`make demo`, `npm run demo`, or equivalent)
- [ ] `README.md` with setup, run instructions, and how to regenerate the sample output
- [ ] A short statement of which stack, framework, and architecture the implementation used and why
- [ ] Generated `sample-output.json` committed alongside the source PDF, matching the §7 schema
- [ ] Generated validation report showing all §8 checks with expected, observed, and status
- [ ] A demo surface (CLI, UI, or static HTML) capable of running the five-minute walkthrough
- [ ] A five-minute recorded demo video (insurance policy against demo-day failures)
- [ ] A one-page retrospective: what worked, what didn't, what to build next

---

# REFERENCE IMPLEMENTATION — Zone 2 of 2 (GUIDANCE ONLY)

*Everything in this zone is guidance. It exists to help teams get started, reduce decision fatigue on Saturday morning, and provide a known-good reference point. Any section can be ignored, replaced, or adapted — as long as The Contract above is satisfied.*

---

## 10. Reference architecture [REFERENCE]

The strategic brief describes a specialist-team pattern. It is the recommended starting point, not a requirement.

| Role | Responsibility |
|---|---|
| Mail Sorter (Orchestrator) | Classifies each page and routes it to the right specialist |
| Form Specialist | Labeled fields, header tables, key-value extraction from pages 1–2 |
| Spreadsheet Specialist | Ruled financial tables; typically has multiple methods with fallback |
| Reading Specialist | Paragraphs, lists, analyst commentary |
| Visual Specialist | Charts, infographics, photos; also serves as a retry path |
| **Proofreader** | **Quality gate.** Runs the §8 arithmetic checks against the extracted data |
| Supervisor (Reconciler) | Handles flagged errors, decides on retry paths |

Alternative patterns that would also satisfy The Contract include:

- A single-LLM-pass approach with a separate validation step
- A state-machine approach where each page advances through extraction and verification states
- A pipeline-per-content-type approach

Pick what matches the team's comfort and the problem.

## 11. Reference tech stack [REFERENCE]

Recommended defaults. Substitute freely. The only hard requirement is that **an LLM is used somewhere in the extraction path**, because semantic understanding of the document is the reason this approach works at all.

| Layer | Default | Reasonable alternatives |
|---|---|---|
| Language | Python 3.11+ | TypeScript/Node, Go, Rust — any language with decent PDF and LLM SDK support |
| LLM | Claude (Opus 4.6 / Sonnet 4.6) | Any frontier model with vision and structured output |
| Agent framework | Claude Agent SDK | LangGraph, homegrown orchestrator, or no framework at all |
| PDF text/tables | `pdfplumber` | `pymupdf`, `pdfminer.six`, `tabula-py`, Azure Document Intelligence, AWS Textract |
| PDF rendering | `pymupdf` (fitz) | `pdf2image`, `wand` |
| Table fallback | `camelot-py` | LLM vision on the rendered page, `tabula-py` |
| Schema | `pydantic` v2 | `zod` (TS), `attrs`, dataclasses, hand-rolled JSON schema |
| UI | Streamlit | FastAPI + minimal HTML, Next.js, CLI only |
| Scaffold | `uv` or `poetry` | `pnpm`, `cargo`, whatever's in muscle memory |

## 12. Reference timeline [REFERENCE]

A suggested schedule for a team that has not run this before. Bake-off pairs may run their own schedules in parallel.

### Saturday — Build

| Time | Activity |
|---|---|
| 09:00 | Group kickoff. Read The Contract together. Confirm every §8 check with the PDF open. **Pick format (unified or bake-off).** |
| 10:00 | Each team scaffolds its repo, verifies API keys, gets an empty `CreditMemo` round-tripping. |
| 11:00 | First extraction pass: header fields (FO2). Visible output by noon. |
| 12:00 | Lunch. |
| 13:00 | Financial tables (FO3). Hardest part — expect at least one to misbehave. |
| 15:00 | Narrative extraction (FO4). Usually quick once LLM plumbing is in place. |
| 16:30 | First integration pass. Run end-to-end, inspect JSON, note breakage. |
| 18:00 | Dinner. Celebrate that something works. |

### Sunday — Verify & Polish

| Time | Activity |
|---|---|
| 09:00 | Proofreader (FO5). Implement §8 checks as pure functions. Expect at least one to fail on first run. |
| 11:00 | Error recovery (FO6). Whatever retry path your architecture suggests. |
| 12:00 | Lunch. |
| 13:00 | Demo surface. Show source pages, extracted values, validation report, provenance. |
| 15:00 | End-to-end dry run. All §8 checks pass. Recovery observable. Record backup video. |
| 16:00 | Demo rehearsal. Run the walkthrough twice. |
| 17:00 | Live demos. In bake-off mode: each pair demos in turn, followed by comparative retrospective. |

## 13. Reference team roles [REFERENCE]

For unified-team mode. Bake-off pairs split responsibilities however they like inside each pair.

- **Extraction lead** — Owns the hardest extraction paths (typically financial tables and the vision fallback). Knows the chosen PDF library well enough to debug merged-header drift in under 15 minutes.
- **Agent lead** — Owns the orchestration, page routing, and LLM integration. Defines the interface each extraction component exposes.
- **Validator lead** — Owns the §8 checks, error recovery, and provenance tracking. Quality gate for the demo.
- **UX/demo lead** — Owns the schema, demo surface, integration runner, and the five-minute demo script. Runs the rehearsal.

## 14. Reference demo script [REFERENCE]

A suggested five-minute walkthrough. Teams may adapt the structure; the content points are what matters.

1. **(30s) The pitch.** "This is Stage 2 of the supply chain from the strategic brief — the refinery that turns a PDF into trustworthy structured data."
2. **(45s) The input.** Show the sample PDF. Flip through form pages, spreadsheets, narrative, infographic, photos. "One document, every content type."
3. **(1m) The run.** Drop the file into the demo surface. Show the routing decisions. Show the JSON output appearing.
4. **(90s) The proofreader.** Open the validation report. Walk through three checks: Sources = Uses, G1 net worth, global DSCR. Show one check that initially failed and how the system recovered. **This is the money moment.**
5. **(30s) Provenance.** Click any field in the output and show the source page it came from.
6. **(45s) The bigger picture.** Return to the brief's supply chain diagram. "We just proved Stage 2. Stages 3 and 4 are the business case." Close.

**Bake-off variant.** Each pair runs the same 5-minute script. After all pairs have demoed, the group spends 15 minutes on a comparative retrospective: which stack extracted fastest, which caught the hardest edge case (the red `($2,918)` on page 12 is a good benchmark), which recovery path was cleverest, and what each approach would cost to scale to 20,000 memos.

## 15. Stretch goals [REFERENCE]

- Cross-page consistency checks beyond §8
- Actually parsing the IBISWorld infographic on page 10 (vision-only path)
- Side-by-side PDF viewer with extracted fields highlighted on source pages
- A second retry path using a different LLM or library
- CSV export of the financial tables
- Load a second hand-modified memo to show robustness to template drift
- Cost tracking per extraction (tokens, API calls, wall time)

---

## 16. Risks and mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Over-scoping field extraction | High | Extract only what §8 needs. Everything else is stretch. |
| Merged-header drift on page 5 Projected column | High | Expected — this is the demo punchline. Recovery is what you're building. |
| Vision attempts on page 10 eat all of Sunday | Medium | Stretch only. Route to `skip` for the core demo. |
| LLM rate limits / API key issues | Medium | Verify access Friday night. Cache LLM responses during dev. |
| Proofreader passes trivially (same wrong source) | Medium | Prefer cross-agent or cross-page checks. C9 exists for this reason. |
| Bake-off: contract ambiguity → incompatible outputs | Medium (bake-off only) | Spend the first hour of Saturday walking through §7 and §8 together with the PDF open. |
| Bake-off: unequal pair sizes or skill levels | Medium (bake-off only) | Pre-balance pairs. Early-finishers help others or attempt stretch goals. |
| Integration breaks 10 min before demo | Always | Record the demo video Sunday afternoon as backup. |

---

---

## 17. Phase 2 — The Loan File (Preview)

Phase 1 proves the refinery on a single credit memo. Phase 2 extends the challenge to the full loan file — multiple document types, cross-document verification, and a time dimension.

### Document types

Phase 2 introduces a loan file containing several document types beyond the credit memo:

| Document | Description |
|---|---|
| Personal Financial Statement (PFS) | Borrower/guarantor assets, liabilities, income — must reconcile with credit memo net worth figures |
| Rent Roll | Unit-level rent schedule at a point in time — must reconcile with memo gross rents and operating statements |
| Appraisal | Third-party valuation report — must reconcile with memo collateral value, LTV, and property description |
| Scanned documents | Signed forms, tax returns, bank statements — OCR-dependent, lower structure |

### Cross-document checks

The core challenge of Phase 2 is verifying consistency across documents:

- PFS net worth vs. credit memo guarantor net worth (C2/C3/C4 values should trace to PFS line items)
- Rent roll unit rents vs. credit memo gross rents (C8/C9 values should match rent roll totals)
- Appraisal value vs. credit memo collateral value and LTV calculation
- Income figures on PFS vs. cash flow tables in credit memo
- Property address and description consistency across all documents

### Timeline dimension

Phase 2 adds an origination vs. servicing distinction:

- **Origination:** Documents as they existed at loan closing — the baseline truth
- **Servicing:** Updated documents during the life of the loan (annual reviews, renewed PFS, updated rent rolls)
- The system must track which version of a document it is processing and flag inconsistencies between origination and servicing snapshots

### Phase 2 tiers

| Tier | Name | Criteria |
|---|---|---|
| Bronze | Pipeline | Process all document types in the loan file independently; extract structured data from each |
| Silver | Crosscheck | Cross-document verification passes — values that appear in multiple documents are reconciled and discrepancies flagged |
| Gold | Platinum | Full timeline support — origination vs. servicing snapshots tracked, with drift detection across time |

### Relationship to Phase 1

Phase 1 tiers (Bronze/Silver/Gold based on checks C1-C9) remain the entry point. A team must achieve at least Phase 1 Silver (6+ checks passing) before attempting Phase 2. The Phase 1 credit memo extraction becomes one component of the larger Phase 2 loan file pipeline.

---

*Requirements v2.1 · Two-phase structure · Contract/Reference split · Companion to the Strategic Brief · Hackathon scope*
