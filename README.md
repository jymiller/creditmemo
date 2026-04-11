# Credit Memo Hackathon

**Can you teach an AI to read a credit memo?**

A 22-page PDF. Nine math checks hidden inside it. Your AI teammate. Whatever tools you want. Go.

[![Deploy to GitHub Pages](https://github.com/jymiller/creditmemo/actions/workflows/pages.yml/badge.svg)](https://github.com/jymiller/creditmemo/actions/workflows/pages.yml)

---

## The Challenge

### → [jymiller.github.io/creditmemo](https://jymiller.github.io/creditmemo/)

We give you one real credit memo — a $514,500 multifamily loan in Philadelphia. It has form fields, financial tables, analyst commentary, infographics, and property photos. Every content type that makes PDF extraction hard.

Your job: extract structured data from it, verify the math, and show where every number came from. Use any language, any framework, any AI. The only thing that matters is whether your output passes the scorecard.

| Tier | What it means |
|---|---|
| **Bronze** (3 of 9 checks) | "I can extract numbers and the math adds up" |
| **Silver** (6 of 9 checks) | "I can extract tables and cross-reference across pages" |
| **Gold** (all 9 checks) | "Every check passes. Full scorecard satisfied." |

**[Join the Discord](https://discord.gg/PCMcgK2P)** to find a team, get help, and share your best extraction failures.

---

## Quick start

```bash
git clone https://github.com/jymiller/creditmemo.git
cd creditmemo/starter-kit
bash setup-check.sh                       # verify your environment
python3 validate.py sample-output.json    # see what Gold looks like
python3 quickstart.py                     # extract your first field
```

Then build your own solution and run `python3 validate.py your-output.json` to check your score anytime.

---

## What's in the repo

### The challenge

| File | What it is |
|---|---|
| [`HACKATHON.md`](HACKATHON.md) | Event guide — spirit, teams, schedule, tiers, awards |
| [`demo-requirements.md`](demo-requirements.md) | The scorecard, output schema, and full spec for teams who want every detail |
| [`Sample-Enhanced-Memo.pdf`](Sample-Enhanced-Memo.pdf) | The 22-page input document |

### Starter kit

| File | What it does |
|---|---|
| [`starter-kit/sample-output.json`](starter-kit/sample-output.json) | Reference output showing the target shape — look at this first |
| [`starter-kit/validate.py`](starter-kit/validate.py) | Runs the 9 checks against your output, prints your tier |
| [`starter-kit/quickstart.py`](starter-kit/quickstart.py) | Extracts your first field from the PDF in 5 minutes |
| [`starter-kit/schemas.py`](starter-kit/schemas.py) | Importable Pydantic schema (Python teams) |
| [`starter-kit/setup-check.sh`](starter-kit/setup-check.sh) | Verifies your environment is ready |
| [`starter-kit/.env.example`](starter-kit/.env.example) | Environment variable template |

### The deeper story (optional)

If you want to understand why a bank would care about this problem:

| Document | Read time |
|---|---|
| [One-Page Brief](https://jymiller.github.io/creditmemo/one-page-brief.html) | 3 min |
| [Strategic Brief](https://jymiller.github.io/creditmemo/credit-memo-extraction-explainer.html) | 12 min |
| [Full Spec](https://jymiller.github.io/creditmemo/demo-requirements.html) | 15 min |

> **Prefer video?** [Walkthrough on Loom](https://www.loom.com/share/8e1d2384a0e642e8896f36a2a60927d9)

---

## How to participate

1. **Read [`HACKATHON.md`](HACKATHON.md)** for the spirit, schedule, and team formation
2. **Clone the repo** and run `setup-check.sh`
3. **Look at `sample-output.json`** to see the shape of what you're building
4. **Build your solution** — any language, any framework, any approach
5. **Run `validate.py` early and often** — it's a tool for building, not a final exam
6. **Demo at 5pm Sunday PT** — 5 minutes, show what you built and what you learned

Bronze is a win. Gold is a flex. Both get celebrated. The best hackathon outcome is not the code — it's the team that built it and the things they learned.

---

## Repository layout

```
.
├── index.html                             Landing page (GitHub Pages)
├── HACKATHON.md                           Event guide
├── demo-requirements.md / .html           Scorecard and full spec
├── one-page-brief.md / .html              Executive brief
├── credit-memo-extraction-explainer.html  Strategic brief
├── Sample-Enhanced-Memo.pdf               The input document
├── hackathon-design-notes.md              Meta-analysis of hackathon design
├── starter-kit/                           Validator, quickstart, schemas, sample output
├── feedback/                              Submission reviews
└── .github/workflows/pages.yml            GitHub Pages deployment
```
