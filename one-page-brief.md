# Credit Memo Refinery — Executive Brief

*One page. Read in three minutes.*

---

## The problem

A mid-size commercial bank has 20,000 or more credit memos sitting in file shares. Every one of them contains proprietary information — our borrowers, our collateral decisions, our analysts' judgments, our realized losses — and none of it is queryable.

Loan officers lose deals to competitors who price sharper because their comp data is better. Credit analysts re-extract the same fields from the same documents on every annual review. Portfolio managers cannot answer "which of my current borrowers look like the ones that defaulted in 2008?" without a multi-week project. Exam teams rebuild concentration and vintage reports from scratch every quarter.

A fully-loaded credit memo takes **15 to 40 analyst hours** to produce. Each annual review re-touches the same data. A regulatory exam cycle is another **40 to 200 hours** of manual extraction. Multiply by 20,000 archived memos and the dormant asset is worth **eight figures in analyst time alone** — plus an unknowable sum in deals lost to faster, better-informed competitors.

## Solution pattern

A small team of specialized agents, one orchestrator, one verifier. Not code — a pattern.

- **Orchestrator** reads each page and routes it by content type.
- **Specialists** — form, table, narrative, visual — each handle one kind of content, with multiple methods and fallbacks.
- **Proofreader** runs arithmetic checks against the extracted data: sources equal uses, assets minus liabilities equal net worth, DSCRs reconcile across pages. Nothing ships until the math holds.
- **Supervisor** handles flagged errors — retry with a different method or escalate.

**Input:** a PDF credit memo. **Output:** structured JSON with every field linked to a specific source page, plus a verification report. **Human checkpoint:** one — exception triage when the supervisor cannot reconcile automatically.

## Before and after

| Metric | Today | With the refinery |
|---|---|---|
| Time per memo | 15–40 analyst hours | Minutes, unattended |
| Cost per memo | Hundreds of dollars in analyst time | Cents in compute |
| Verifiability | "Trust the analyst" | Arithmetic reconciled, page-level provenance |
| Cross-memo query | File share search, manual linking | Structured query |
| Exam prep | 40–200 hours per cycle | Hours |
| Error tracking | None — no audit trail | Bounded by an explicit check set |

*Numbers are representative for a mid-size commercial lender. The shape of the improvement is the point.*

## Key design decisions

Three choices that are not obvious and that carry the whole architecture.

1. **The proofreader extracts nothing.** Most teams merge extraction and validation. We separate them, because an extractor cannot catch its own mistakes. A dedicated verification role — running real arithmetic against real expected values — turns raw AI output into data a risk organization will trust.

2. **Content-type routing, not a monolithic pass.** A single AI call over the whole document works, but failure modes are hidden inside a confident-looking answer. Routing each page to a specialist by content type exposes failures where they can be caught and recovered. This is the architectural choice that makes the error-recovery story credible.

3. **The contract is arithmetic, not vibes.** Every acceptance check in the demo is a specific equation with a specific expected value drawn from the real document. AI output looks trustworthy; arithmetic is the only way to prove it actually is.

## Scope — what the demo deliberately does not do

The weekend demo builds the refinery itself on one sample memo. It does not build the data warehouse, the downstream insight agents, template-drift handling across memo versions, multi-document linking, persistent storage, authentication, or compliance workflows.

This is deliberate. Proving the hardest and least-proven link — extraction with verification — is the credibility anchor for the entire business case. Overreaching would produce half-baked work on everything and a clean demo of nothing. Strategic judgment here is knowing that a narrow, trustworthy demo wins an investor conversation that a broad, hand-wavy demo loses.

---

*Companion to the [Strategic Brief](credit-memo-extraction-explainer.html) and the [Demo Requirements](demo-requirements.html).*
