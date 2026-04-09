# Credit Memo Refinery

**From dormant archive to proprietary data moat.**

A document set and weekend hackathon specification for turning a commercial bank's credit memo backlog into a structural competitive advantage.

[![Deploy to GitHub Pages](https://github.com/jymiller/creditmemo/actions/workflows/pages.yml/badge.svg)](https://github.com/jymiller/creditmemo/actions/workflows/pages.yml)

---

## Start here

### → [jymiller.github.io/creditmemo](https://jymiller.github.io/creditmemo/)

The full document set is published as a GitHub Pages site with a hub that routes executives, engineers, and hackathon participants to the right starting point. **That's the recommended way to read the material.**

> **▶ Prefer to watch first?** [Walkthrough on Loom](https://www.loom.com/share/8e1d2384a0e642e8896f36a2a60927d9) — a tour of the document set and the business case behind it.

---

## What's in this repo

| Document | Read time | Audience |
|---|---|---|
| **[One-Page Brief](https://jymiller.github.io/creditmemo/one-page-brief.html)** — problem, pattern, before/after, key decisions | 3 min | Executive |
| **[Strategic Brief](https://jymiller.github.io/creditmemo/credit-memo-extraction-explainer.html)** — full business case as a four-stage supply chain | 12 min | Mixed |
| **[Demo Requirements](https://jymiller.github.io/creditmemo/demo-requirements.html)** — hackathon contract + reference implementation | 15 min | Engineering |

### Markdown sources

Developer-friendly versions that render natively on GitHub:

- [`one-page-brief.md`](one-page-brief.md)
- [`demo-requirements.md`](demo-requirements.md)

### Sample input

- [`Sample-Enhanced-Memo.pdf`](Sample-Enhanced-Memo.pdf) — 22-page sample credit memorandum used as the input for the weekend hackathon demo.

---

## For hackathon participants

Start with [`demo-requirements.md`](demo-requirements.md).

- **The Contract** (§§1–9) is locked. Every implementation must satisfy it, regardless of language, framework, or architecture. The output JSON schema, the arithmetic verification checks, the scope, and the deliverables all live here.
- **Reference Implementation** (§§10–16) is guidance only. Tech stack, timeline, team roles, and the specialist-team architecture from the strategic brief are all suggestions you can freely substitute.
- Two formats are supported: **Unified Team** (one shared codebase, split into roles) or **Bake-off** (2–3 independent pairs targeting the same contract with different stacks). Pick at Saturday morning kickoff after the group has read The Contract together.

---

## Repository layout

```
.
├── index.html                             Landing page (GitHub Pages entry)
├── credit-memo-extraction-explainer.html  Strategic brief (frozen)
├── demo-requirements.html                 Hackathon requirements (rendered)
├── demo-requirements.md                   Hackathon requirements (source)
├── one-page-brief.html                    Executive brief (rendered)
├── one-page-brief.md                      Executive brief (source)
├── Sample-Enhanced-Memo.pdf               Sample input for the demo
├── README.md                              This file
└── .github/workflows/pages.yml            GitHub Pages deployment workflow
```
