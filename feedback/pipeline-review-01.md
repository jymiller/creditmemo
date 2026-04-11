# Pipeline Review #1

**Hackathon Feedback** | Reviewed against [demo-requirements.md](../demo-requirements.md) sections 1-9

> **Scope note:** This review covers the **Phase 1 (Crack the PDF)** pipeline architecture — single credit memo, nine math checks, Bronze/Silver/Gold tiers. See the Phase 2 implications section at the end for how this architecture extends into the multi-document Loan File phase.

---

## Verdict: This design maps cleanly to the contract. One refinement recommended.

---

## The submitted architecture

```
Ingest PDF → Classify Pages → Route Pages → Run Proofreader
                                (subprocess)        |
                                               Validation Gate
                                              /              \
                                         (fail)            (pass)
                                            |                 |
                                  Supervisor Remediate    Emit Output
                                    (subprocess)
```

Six stages, each with READY and DEFAULT FALLBACK states. Route Pages and Supervisor Remediate are marked as subprocesses using what appears to be a workflow orchestration tool (the `studio.credit-memo-*` references and `samples.alpha` service account suggest Prefect, Dagster, Temporal, or a custom engine).

## Contract mapping

| Pipeline stage | Contract outcome | Status |
|---|---|---|
| Ingest PDF | -- | Scaffolding (no FO) |
| Classify Pages | FO1 — Content-aware routing | Covered |
| Route Pages (subprocess) | FO2 Header, FO3 Tables, FO4 Narrative | Covered (extraction bundle) |
| Run Proofreader | FO5 — Arithmetic verification | Covered |
| Validation Gate + Supervisor | FO6 — Observable error recovery | Covered |
| Emit Output | FO7 — Structured output with provenance | Covered |

Every functional outcome from the contract is accounted for.

## What's strong

1. **The validation gate as a decision diamond.** Making the pass/fail branch an explicit first-class architectural element — not buried inside the proofreader — is a mature design choice. Failed memos route to remediation; passing memos route to output. The error recovery loop (FO6) is baked into the flow as a concept, not an afterthought.

2. **SUBPROCESS tags on Route Pages and Supervisor.** Using a workflow orchestration tool rather than ad-hoc scripts is a different and completely valid architectural choice compared to the reference implementation's agent-based approach. The contract doesn't prescribe architecture — it prescribes outcomes.

3. **"Extraction bundle" abstraction.** Route Pages launches a content-specific extraction bundle rather than hard-coding individual specialist agents. The routing layer doesn't know or care how each content type is extracted — it just dispatches to the right bundle. Clean separation of concerns.

## One recommended refinement

> **The re-validation loop.** The current diagram shows Supervisor Remediate, but it's not clear where the remediated output goes after re-extraction. If it flows directly to Emit Output without being re-checked, a bad retry could slip through unchecked.

**Recommendation:** Route the Supervisor's output back to **Run Proofreader** so re-extracted values get validated before reaching Emit Output. Add a max-retry cap (2-3 attempts) so it doesn't loop forever. If checks still fail after retries, emit the output anyway with failing checks marked as `"status": "fail"` in the validation report — that's still a demoable and honest result.

The corrected flow:

```
Ingest PDF
  → Classify Pages
    → Route Pages (extraction bundle)
      → Run Proofreader
        → Validation Gate
          → PASS → Emit Output
          → FAIL → Supervisor Remediate
                     → Run Proofreader (again, max 2-3 retries)
                       → still failing? → Emit Output with failures marked
```

## Tracking toward tier

The architecture is structurally complete — every FO is covered. The question is which checks are actually passing inside the extraction bundle. Run the validator to see where you stand:

```bash
cd starter-kit
python3 validate.py ../your-output.json
```

The validator prints a tier summary (Bronze/Silver/Gold) and shows exactly which checks are passing or failing.

## Summary

Solid pipeline design. Six stages map directly to seven functional outcomes. The validation gate is the right architectural choice. The one fix — looping remediated output back through the proofreader — is a refinement, not a redesign. If the extraction bundle is producing numbers, this team is tracking for Silver or Gold by Sunday.

---

## Phase 2 implications

Phase 2 (The Loan File) introduces multiple document types — Personal Financial Statements, Rent Rolls, Appraisals, and scanned documents — with cross-document verification and an origination-vs.-servicing timeline. The current six-stage pipeline remains the core processing spine, but several extensions will be needed.

First, a **document classification stage** will need to sit upstream of the current Ingest step. Where Phase 1 assumes a single credit memo PDF, Phase 2 must identify each document type in a loan file and route it to the appropriate specialized extractor. The existing "Route Pages" subprocess concept scales naturally here — it already dispatches to content-specific extraction bundles — but the routing taxonomy expands from page-level content types to document-level types.

Second, **cross-document verification** introduces a new validation layer that doesn't exist in Phase 1. The current Validation Gate checks arithmetic within a single document; Phase 2 adds checks that compare values across documents (e.g., does the NOI on the Rent Roll match the NOI referenced in the Credit Memo?). This likely means a second validation pass after individual documents are processed, operating on the combined extracted data.

Third, **OCR handling for scanned documents** adds confidence and quality considerations to the extraction pipeline. Scanned pages may produce lower-confidence text, which the proofreader and validation gate will need to account for — distinguishing between a genuine arithmetic error and an OCR misread requires different remediation strategies.

---

*Reviewed against the [Demo Requirements Contract](../demo-requirements.md) (sections 1-9) | [Credit Memo Refinery Hackathon](https://jymiller.github.io/creditmemo/)*
