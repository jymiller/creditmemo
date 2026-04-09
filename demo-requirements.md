# Credit Memo Demo — Requirements

**Version:** 1.0
**Scope:** Weekend hackathon
**Input:** `Sample-Enhanced-Memo.pdf` (22 pages, 1.1 MB)
**Companion to:** [Strategic Brief](credit-memo-extraction-explainer.html) — frozen as the source of high-level requirements

---

## 1. Purpose

Prove the refinery works. One sample credit memo goes in; verified structured data comes out. Every field traces back to a page in the source PDF. Every number reconciles against the proofreader's arithmetic checks. Nothing silently wrong.

This is the credibility anchor for Stage 2 of the supply chain described in the strategic brief. Stages 1, 3, and 4 are acknowledged and out of scope for this demo.

---

## 2. Success criteria

The demo succeeds if at the end of Sunday we can, on a laptop:

1. Drop `Sample-Enhanced-Memo.pdf` into the system and produce a JSON document matching the schema in §7.
2. Every populated field carries a page-level source reference back to the PDF.
3. The proofreader emits a validation report; all **mandatory** checks in §8 pass.
4. At least one reconciler retry is visible in the output (first attempt wrong → fallback corrected).
5. We can walk through the five-minute demo script in §12 without hedging.

---

## 3. In scope / Out of scope

### In scope
- One PDF, processed end-to-end
- Mail sorter page routing
- Form specialist (header fields, pages 1–2)
- Spreadsheet specialist (three target tables)
- Reading specialist (narrative sections)
- Vision specialist (basic, used as a retry fallback)
- Proofreader with mandatory arithmetic checks
- Supervisor with one retry path
- Minimal UI or CLI for the demo
- Source-page provenance per field

### Out of scope
- Any Stage 3 (data estate) work
- Any Stage 4 (insight agents)
- Multiple documents or cross-memo linking
- AuthN/AuthZ, multi-user, persistence beyond local files
- Production observability, cost tracking, SLAs
- Template drift handling across memo versions
- PII handling, anonymization, compliance review
- Exhaustive field extraction — only what's needed to run §8

---

## 4. The sample document

22-page MBFS Credit Memorandum for a $514,500 multifamily real estate refinance in Philadelphia. Contains the full mixed-content profile the refinery needs to handle.

| Field | Value |
|---|---|
| Borrower | Real estate holding company |
| Loan | $514,500 @ 4.75% fixed, 5yr / 30yr amort |
| Collateral | Multifamily 5+ unit, est. value $735,000, 70% LTV |
| Guarantors | Two, each 50% ownership; credit 734 and 775 |
| Risk rating | 4-Pass (scored 3.55) |
| Borrower DSCR | 0.82x (2021), 1.02x pro-forma |
| Global DSCR | 1.59x (2021), 1.60x pro-forma |
| Gross rents | $53,400/yr ($4,450/mo across six units) |

---

## 5. Architecture

Seven roles, per the strategic brief:

| Role | Agent name | Responsibility |
|---|---|---|
| Mail Sorter | Orchestrator | Classifies and routes each page |
| Form Specialist | Key-value agent | Labeled fields, header tables |
| Spreadsheet Specialist | Table agent | Ruled financial tables |
| Reading Specialist | Narrative agent | Paragraphs, lists, analyst notes |
| Visual Specialist | Vision agent | Charts, infographics, retry path |
| Proofreader | Validator agent | Arithmetic + cross-page checks |
| Supervisor | Reconciler agent | Retry / fallback routing |

Diagram lives in the strategic brief (`credit-memo-extraction-explainer.html#technical`).

---

## 6. Functional requirements

### F1 — Page routing (Mail Sorter)

Classify each of the 22 pages into one or more of: `form`, `table`, `narrative`, `visual`, `skip`. Expected routing for the sample:

- **Form:** 1, 2, 19, 21
- **Table:** 4, 5, 6, 7, 12, 17, 20
- **Narrative:** 2, 3, 8, 9, 18, 19
- **Visual:** 10, 11, 13–16
- **Skip:** 22

Acceptance: per-page label JSON written to `routing.json`.

### F2 — Header extraction (Form Specialist)

Extract from pages 1–2 into the schema:

- [ ] Memo date, credit union, RM, analyst, borrower name
- [ ] Loan amount, rate, rate type, term, amortization
- [ ] Collateral type, address, estimated value, LTV, purchase price, lien position
- [ ] NAICS code, MBFS risk rating, aggregate relationship
- [ ] Borrower DSCR, global DSCR (both actual and pro-forma)
- [ ] Guarantors: name, credit score, ownership %
- [ ] Sources & Uses rows with amounts

### F3 — Financial table extraction (Spreadsheet Specialist)

Extract three target tables. Scope is deliberately narrow — we're proving the mechanism, not being exhaustive.

- [ ] **Guarantor 1 Net Worth** (page 4) — assets, liabilities, adjustments, stated & adjusted net worth
- [ ] **Guarantor 1 Personal Cash Flow** (page 5) — 2018/2019/2020/Projected columns, income/deductions/debt service/DSCR rows
- [ ] **Global Cash Flow** (page 12) — borrower + two guarantors + totals across 2019/2020/2021/Projected

### F4 — Narrative extraction (Reading Specialist)

Extract from pages 3, 8, 9, 18, 19:

- [ ] Borrower background paragraph
- [ ] Operating statement narrative
- [ ] Strengths list
- [ ] Weaknesses list
- [ ] Analyst notes / CU recommendations
- [ ] Loan purpose statement

### F5 — Proofreader (Validator)

Implement each check from §8 as a pure function taking the extracted `CreditMemo` and returning a `ValidationCheck`. Run all checks after extraction completes.

### F6 — Supervisor / Reconciler

At minimum one retry path: if the Spreadsheet Specialist's first method fails a proofreader check, retry the affected page with a fallback (camelot stream or Vision Specialist rendering). Log which path produced the final value.

### F7 — Output

Emit two artifacts:

1. `sample-output.json` — full `CreditMemo` structured output
2. `sample-validation.html` — human-readable validation report with per-field provenance

---

## 7. Output schema

```python
from pydantic import BaseModel, Field
from typing import Literal

class SourceRef(BaseModel):
    page: int
    agent: Literal["form", "table", "narrative", "visual"]
    method: str  # e.g. "pdfplumber-lattice", "claude-vision"
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
    rows: list[dict]  # column name -> value
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

---

## 8. Proofreader checks

Mandatory arithmetic checks against the sample document. Expected values are the ground truth — if the extraction produces something else, either the extraction is wrong or the check is wrong. Either way, the demo doesn't ship until both agree.

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

Tolerance: ±1 unit for integer dollar totals, ±0.01 for ratios.

---

## 9. Tech stack

| Layer | Choice | Rationale |
|---|---|---|
| Language | Python 3.11+ | Best ecosystem for PDF + LLM |
| LLM | Claude (Opus 4.6 or Sonnet 4.6) | Strong on tables, vision, structured output |
| Agent framework | Claude Agent SDK | Matches the brief's architecture |
| PDF text/tables | `pdfplumber` | First choice for ruled tables |
| PDF rendering | `pymupdf` (fitz) | Fast rasterization for vision fallback |
| Table fallback | `camelot-py` | Second choice when pdfplumber fails |
| Schema | `pydantic` v2 | Structured output + JSON |
| UI | Streamlit **or** FastAPI + minimal HTML | Streamlit for speed; FastAPI if team prefers |
| Scaffold | `uv` or `poetry` | Fast dep install Saturday morning |

---

## 10. Weekend timeline

### Saturday — Build

| Time | Activity |
|---|---|
| 09:00 | Kickoff. Review sample PDF together. Divide tasks. Agree on schema and §8 checks before any code. |
| 10:00 | Project scaffold. Repo, deps, Claude API keys, Pydantic schemas, end-to-end "hello world" returning an empty `CreditMemo`. |
| 11:00 | Mail Sorter v1. Single LLM call returning page → label map. |
| 12:00 | Lunch. |
| 13:00 | Form Specialist. Header extraction from pages 1–2 with structured output. |
| 15:00 | Spreadsheet Specialist v1. pdfplumber lattice on the three target tables. |
| 16:30 | Reading Specialist. Strengths/weaknesses/analyst notes. |
| 17:30 | First integration pass. Run end-to-end, inspect JSON, note breakage. |
| 18:30 | Dinner. |

### Sunday — Verify & Polish

| Time | Activity |
|---|---|
| 09:00 | Proofreader. Implement each §8 check as a pure function. At least one should fail on first run — fix upstream. |
| 11:00 | Supervisor / Reconciler. One retry path: pdfplumber lattice → camelot stream → vision. |
| 12:00 | Lunch. |
| 13:00 | Demo surface. Streamlit or static HTML with source page, extracted JSON, validation report, provenance column. |
| 15:00 | End-to-end dry run. All mandatory checks pass. At least one reconciler retry visible. |
| 16:00 | Demo rehearsal. Record the walkthrough twice. |
| 17:00 | Live demo + retrospective. |

---

## 11. Team structure

Assumes 3–4 people. If smaller, fold Validator into UX.

- **Extraction lead** — Spreadsheet Specialist + Vision Specialist. Knows `pdfplumber` well.
- **Agent lead** — Mail Sorter, Form Specialist, Reading Specialist. Claude Agent SDK wiring.
- **Validator lead** — Proofreader + Supervisor + provenance tracking. Quality gate.
- **UX/demo lead** — Schema, UI surface, integration runner, demo script.

---

## 12. Demo script (5 minutes)

1. **(30s) The pitch.** "This is Stage 2 of the supply chain from the strategic brief — the refinery that turns a PDF into trustworthy structured data."
2. **(45s) The input.** Show the sample PDF. Flip through form pages, spreadsheets, narrative, infographic, photos. "One document, every content type."
3. **(1m) The run.** Drop the file in. Show Mail Sorter routing, specialists working, JSON output appearing.
4. **(90s) The proofreader.** Open the validation report. Walk through three checks: Sources = Uses, G1 net worth, global DSCR. Show one check that initially failed and how the reconciler recovered. **Money moment.**
5. **(30s) Provenance.** Click any field, show the source page.
6. **(45s) Bigger picture.** Return to the brief's supply chain diagram. "We just proved Stage 2. Stages 3 and 4 are the business case." Close.

---

## 13. Stretch goals

- Cross-page consistency check (gross rents narrative vs. transactional table)
- Vision Specialist actually parsing page 10 (IBISWorld infographic)
- Side-by-side PDF viewer with extracted fields highlighted on source pages
- Second retry path using a different LLM model
- CSV export of the financial tables
- Load a second hand-modified memo to show template robustness

---

## 14. Risks and mitigations

| Risk | Likelihood | Mitigation |
|---|---|---|
| Over-scoping field extraction | High | Extract only what §8 needs. Everything else is stretch. |
| Merged-header drift on page 5 Projected column | High | Expected — this is the demo punchline. Reconciler is the recovery. |
| Vision specialist eats the weekend on page 10 | Medium | Stretch only. Mail Sorter labels it `skip` for the core demo. |
| LLM rate limits / API key issues | Medium | Verify access Friday night. Cache LLM responses during dev. |
| Proofreader passes trivially (same bad source) | Medium | Require cross-agent checks where possible. |
| Integration breaks 10 min before demo | Always | Record the demo video Sunday morning as backup. |

---

## 15. Deliverables

- [ ] Git repository with one-command bootstrap (`make demo`)
- [ ] `README.md` with setup, run, regenerate instructions
- [ ] Source code for all seven agent roles
- [ ] Pydantic schemas matching §7
- [ ] Proofreader checks as testable pure functions
- [ ] `sample-output.json` committed next to the source PDF
- [ ] `sample-validation.html` committed
- [ ] Five-minute recorded demo video (backup)
- [ ] One-page retrospective: what worked, what didn't, what to build next

---

*Requirements v1.0 · Companion to the Strategic Brief · Hackathon scope*
