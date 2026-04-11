# Credit Memo Hackathon

**An informal weekend experiment. Build something, break something, learn something.**

---

> **This is a dry run.** Everything here — the schedule, the teams, the awards, the format — is illustrative. We're testing the concept, the materials, and the experience so that when we find a client and sponsors, we can run a real, sponsored hackathon that actually works. Your participation is helping us figure out what that looks like. The only real deliverable is honest feedback about what worked and what didn't.

---

## The only real deadline

**Submissions by Sunday at 5pm PT.** That's it. Everything else is flexible.

Feedback and support will be available all weekend in the [Discord](https://discord.gg/PCMcgK2P). Ask questions, share screenshots of weird extraction errors, or just hang out.

---

## The spirit

This is not a test. There is no wrong answer. There is no "behind."

Mistakes are not failures; they are data. A table extraction that silently drops a negative sign is not a bug — it's the exact kind of insight that makes this problem interesting. The Wall of Fails (see below) exists to celebrate these moments.

**Three ground rules:**

1. **Your AI is your teammate.** Claude Code, Cursor, Copilot, ChatGPT — whatever you use, use it shamelessly. The question is not "can you write Python?" — it's "can you and your AI crack the PDF?"

2. **Every skill has a role.** You do not need to be an engineer to contribute. You need to be curious. Engineers write code. Domain experts read the credit memo and explain what the numbers mean. Storytellers craft the demo. Quality advocates run the validator and tell the team what's off. The best teams mix all of these.

3. **Ship something by 5pm Sunday.** It does not need to be perfect. It needs to exist. Bronze tier (3 checks passing) is a legitimate win. Gold tier (all 9) is a flex. Both get celebrated.

---

## Who this is for

You belong here if any of these are true:

- You write code in any language
- You've ever read a financial statement
- You've ever been frustrated by data locked in a PDF
- You're curious about how AI can solve real problems
- You like building things under pressure
- You want to learn something new this weekend
- Someone invited you and you said "sure, why not"

**You do not need:** prior experience with PDF extraction, credit memos, Python, LLMs, or any specific technology. You need a laptop and an internet connection.

---

## Team formation

**Mix skills deliberately.** A team of four engineers will build faster but demo worse than a team with an engineer, a domain expert, a storyteller, and a quality advocate.

### Suggested roles (not required, just helpful)

| Role | What you do | Best fit for |
|---|---|---|
| **Builder** | Write the extraction code, wire the tools, debug the pipeline | Engineers, data scientists |
| **Domain interpreter** | Read the credit memo, explain what the numbers mean, spot extraction errors that code can't | Finance people, analysts, anyone who's seen a loan file |
| **Quality advocate** | Run `validate.py` early and often, interpret the results, tell the builder what's wrong | Anyone comfortable with a terminal and reading error output |
| **Demo storyteller** | Own the 5-minute walkthrough, craft the narrative, make the audience care | PMs, designers, anyone who's ever presented |

A two-person team can combine roles. A solo participant can do all four with an AI teammate. There's no minimum team size.

### How to form teams

**If you're the organizer:** At kickoff, ask everyone to introduce themselves with one sentence: name, skill, and one thing they're curious about. Then let people self-organize into teams of 2-4, optimizing for skill diversity over friendship.

**If you're remote:** Join the [Discord](https://discord.gg/PCMcgK2P) and say hello in `#introductions`. Or go solo with your AI — a solo builder with Claude Code can absolutely hit Bronze by Sunday.

---

## Phase 1 — Crack the PDF

**One PDF goes in. Verified structured data comes out.**

Your team processes `Sample-Enhanced-Memo.pdf` — a 22-page credit memo for a $514,500 multifamily real estate loan — and produces a JSON file matching the output schema. A validator checks the math. Every field traces back to the page it came from.

Use any language, any framework, any approach. The only thing that matters is your score.

The full scorecard is in [demo-requirements.md](demo-requirements.md) sections 5-8. The TL;DR:

- **Extract** header fields, financial tables, and narrative sections from the PDF
- **Verify** the extraction using 9 math checks (sources = uses, net worth reconciles, ratios match, etc.)
- **Show provenance** — for any extracted value, point at the source page
- **Demo it** in a 5-minute walkthrough Sunday afternoon

### Phase 1 tiers — what "done" looks like

| Tier | Checks passing | What it proves |
|---|---|---|
| **Bronze** | C1 + C5 + C8 (3 of 9) | "We can extract numbers from a PDF and the math adds up" |
| **Silver** | + C2 + C4 + C9 (6 of 9) | "We can extract tables and cross-reference across pages" |
| **Gold** | All 9 | "Every check passes. Full scorecard satisfied." |

**Bronze is a win.** Say it again: Bronze is a win. A team that hits Bronze built a working extraction pipeline with verification in a weekend. That's not trivial.

---

## Phase 2 — The Loan File

**Phase 1 proves extraction works on one document. Phase 2 proves it scales.**

A real loan file isn't one PDF — it's a folder. A single credit decision touches many document types that arrive at different times across the life of a loan. Banks have 2,000+ of these files sitting in file shares. To unlock that data, you need a pipeline that can handle all of them — not just the credit memo.

Phase 2 gives you a loan file folder containing multiple document types. Your system must classify each document, route it to the right extractor, and verify data *across* documents.

### The document types

| Document | What it contains | Why it's hard |
|---|---|---|
| **Credit Memo** | The Phase 1 PDF — loan terms, financials, analyst narrative | Form fields, tables, narrative, photos — you already know |
| **Personal Financial Statement (PFS)** | Borrower's net worth, liquidity, assets and liabilities | Dense tables, handwritten entries, inconsistent formats |
| **Rent Roll** | Unit-level income for the property — unit number, tenant, rent, vacancy | Tabular but messy — merged cells, footnotes, partial occupancy |
| **Appraisal Summary** | Property valuation, comparable sales, condition assessment | Mix of structured data and narrative opinions |
| **Scanned Documents** | Tax returns, insurance certs, environmental reports | OCR quality varies — faded ink, skewed pages, stamps over text |

### Cross-document verification checks

Phase 1 checks math *within* a single document. Phase 2 checks consistency *across* documents:

- **Net worth reconciliation** — Does the borrower's net worth on the PFS match the figure cited in the credit memo?
- **LTV validation** — Does the appraised value from the appraisal summary support the loan-to-value ratio in the loan terms?
- **Income consistency** — Do the rents on the rent roll tie to the income assumptions in the credit memo's cash flow analysis?
- **Guarantor consistency** — Is guarantor information (name, ownership %, net worth) consistent across all documents that reference it?

### The timeline dimension

Loan files grow over time. At origination, you get the initial credit memo, appraisal, and PFS. During servicing, annual reviews add updated financials, new rent rolls, and covenant compliance checks. Phase 2 includes documents from two points in time:

- **Origination** — The initial loan package
- **Servicing review (2 years later)** — Updated financials and property performance

New checks:
- How did NOI change between origination and the latest review?
- Did the borrower's net worth improve or deteriorate?
- Are there covenant violations based on the original loan terms?

### Phase 2 tiers

| Tier | What it proves |
|---|---|
| **Pipeline** | Auto-classify 3+ document types and extract structured data from each |
| **Crosscheck** | Pass cross-document verification — data reconciles between documents |
| **Platinum** | Handle scanned documents via OCR, origination vs. servicing timeline, full loan file assembled |

### Why Phase 2 matters

Phase 1 answers "can you extract one document?" Phase 2 answers "can you build a system that scales to 2,000+ loan files?" That's the difference between a demo and a product. Teams that reach Phase 2 are building the kind of flexible, multi-document pipeline that actually solves the bank's problem.

---

## Getting started (first 30 minutes)

1. **Clone the repo:**
   ```
   git clone https://github.com/jymiller/creditmemo.git
   cd creditmemo
   ```

2. **Run the setup check:**
   ```
   cd starter-kit
   bash setup-check.sh
   ```
   Fix anything that says FAIL. If you're stuck, ask in the Discord `#help` channel.

3. **Look at what success looks like:**
   ```
   cat sample-output.json | python3 -m json.tool | head -50
   ```
   This is the shape your output needs to match.

4. **Run the validator on the sample:**
   ```
   python3 validate.py sample-output.json
   ```
   You should see 9/9 PASS, GOLD tier. This is your target.

5. **Run the quickstart:**
   ```
   python3 quickstart.py
   ```
   This extracts loan terms from page 1 using Claude. You now have a working PDF-to-JSON pipeline. Extend it.

6. **Start building.** Fork `quickstart.py` or start fresh in your preferred language. Run `validate.py` anytime to check your score.

---

## Schedule (illustrative)

> **Note:** This schedule is a suggestion for future sponsored events, not a mandate. For this informal run, the only real milestone is **submissions by 5pm Sunday PT**. Work at your own pace, in your own timezone, in whatever order makes sense to you.

### Saturday — Build

| When | What | Energy |
|---|---|---|
| Morning | **Kickoff.** Intros, team formation, open the PDF together. | High |
| Mid-morning | **Warm-up challenge.** Run `quickstart.py` and modify it to extract one additional field. First team to extract the borrower's name wins bragging rights. | Fun |
| Late morning | Teams start building. Builder codes; Domain Interpreter reads the PDF; Quality Advocate runs the validator. | Focus |
| Afternoon | Deep work. Financial tables are hard — this is where the real learning happens. | Grind |
| Late afternoon | **Checkpoint demo.** Each team shows what they have in 2 minutes. No slides. Just the terminal or UI. | Energy boost |
| Evening | **Wall of Fails.** Share your most surprising extraction error. Best fail wins a prize. | Laughter |

### Sunday — Verify and Demo

| When | What | Energy |
|---|---|---|
| Morning | Resume building. Focus on getting the validator to pass more checks. | Focused |
| Midday | Polish the demo. Demo Storyteller takes over. | Creative |
| Afternoon | **Dry run.** Each team runs through the 5-minute demo script once. | Practice |
| **5pm PT** | **Submissions due.** Share your output.json and a short demo (recorded or live). | Showtime |
| After 5pm | **Retrospective.** What worked, what surprised you, what would you tell your past self from Saturday morning? | Reflection |

---

## Awards (illustrative)

> **Note:** Award categories for future sponsored events. For this informal run, we'll celebrate whatever happens — every submission gets recognized.

| Award | Criteria |
|---|---|
| **Gold Standard** | Highest tier achieved (Gold > Silver > Bronze) |
| **Most Creative Approach** | Unusual tool choice, unexpected architecture, or a left-field idea that worked |
| **Best Recovery Story** | Most impressive case of detecting and correcting a bad extraction |
| **Best Use of AI** | Most effective use of AI pair programming during the build |
| **Best Demo** | Best 5-minute narrative — clarity, energy, connection to the problem |
| **Most Surprising Insight** | Something nobody expected to learn |
| **Best Team Name** | Self-explanatory |
| **Best Fail** | Most entertaining extraction error from the Wall of Fails |

---

## Working with AI

Your AI pair programmer is a first-class teammate. Here are ways to use it well:

- **"Read this PDF page and extract the loan amount as JSON."** — Start with the simplest possible prompt and iterate.
- **"This table extraction has a merged header on page 5. What's going wrong?"** — Use your AI to debug library-specific issues.
- **"Write a function that checks if sources equal uses."** — Let it scaffold, then review.
- **"I have this JSON output. Run through the 9 checks and tell me which ones fail."** — Use it as a manual validator while building.
- **"Help me write a 5-minute demo script for what we built."** — The Demo Storyteller's best friend.

**What NOT to do:** Don't ask the AI to build the entire solution in one shot and submit it without understanding it. The point is learning, not just passing the checks. Use the AI as a collaborator, not a contractor.

---

## Feedback and support

**All weekend, in the [Discord](https://discord.gg/PCMcgK2P).**

- `#help` — stuck? Ask here.
- `#feedback` — reactions, suggestions, what's working and what isn't.
- `#wall-of-fails` — post your most entertaining extraction errors.
- `#demos` — share screenshots, videos, and links to your work.

Your feedback on this experience is genuinely valuable. We're using this informal run to design a real, sponsored hackathon for when we find a client and sponsors. Tell us what was confusing, what was fun, what was missing, and what you'd change.

---

## For future sponsored events (organizer notes)

> The sections below are reference material for running a formal, in-person or hybrid hackathon. They're included here for planning purposes and don't apply to this informal run.

### Supplies checklist

- [ ] Wifi that actually works
- [ ] Power strips at every table
- [ ] Post-its and markers (for architecture sketching)
- [ ] Timer visible to all teams (for checkpoint demos and final presentations)
- [ ] Snacks and drinks (all day — not just lunch)
- [ ] Music (background playlist, nothing with lyrics during focus blocks)
- [ ] Printed one-page challenge cards for each team
- [ ] A wall or whiteboard for the Wall of Fails
- [ ] Small prizes for each award category (stickers, gift cards, bragging rights)
- [ ] A way to record final demos (phone camera is fine)

---

## Quick links

| Resource | Link |
|---|---|
| Discord | [Join the hackathon Discord](https://discord.gg/PCMcgK2P) |
| GitHub Pages hub | [jymiller.github.io/creditmemo](https://jymiller.github.io/creditmemo/) |
| Video walkthrough | [Loom](https://www.loom.com/share/8e1d2384a0e642e8896f36a2a60927d9) |
| Scorecard and full spec | [demo-requirements.md](demo-requirements.md) |
| Strategic brief (the "why") | [credit-memo-extraction-explainer.html](https://jymiller.github.io/creditmemo/credit-memo-extraction-explainer.html) |
| Executive one-pager | [one-page-brief.html](https://jymiller.github.io/creditmemo/one-page-brief.html) |
| Starter kit | [starter-kit/](starter-kit/) |
| Sample output | [starter-kit/sample-output.json](starter-kit/sample-output.json) |
| Validator | [starter-kit/validate.py](starter-kit/validate.py) |

---

*The best hackathon outcome is not the code. It's the team that built it, the things they learned, and the stories they'll tell on Monday.*
