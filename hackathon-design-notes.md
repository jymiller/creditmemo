# Hackathon Design Notes — Meta-Analysis

**What it takes to design a hackathon around a real business problem, what we built for the short term, and what we'd build to make it repeatable.**

---

## The anatomy of a business-problem hackathon

Most hackathons are open-ended: "build anything in 48 hours." A business-problem hackathon is different in four ways:

1. **Constrained input.** Participants work on a specific artifact (a credit memo PDF), not a blank canvas. The constraint focuses creativity — teams compete on approach, not on idea selection.

2. **Verifiable output.** The contract defines 9 arithmetic checks with specific expected values. A team's output either passes the proofreader or it doesn't. This eliminates subjective judging for the technical tier and frees the awards to celebrate softer qualities (storytelling, creativity, agent usage).

3. **Real data, real stakes.** The sample PDF is a (redacted) production-format document. Participants experience real-world extraction challenges — merged table headers, negative numbers in parentheses, infographics with no table structure — that would never appear in a synthetic dataset.

4. **Business narrative.** Participants don't just build a pipeline; they learn why the pipeline matters. The strategic brief frames the extraction as Stage 2 of a supply chain that ends in competitive advantage. The demo script maps technical output back to business outcomes. This connection elevates the hackathon from "cool tech exercise" to "I understand why a bank would pay for this."

---

## The specification-first approach

We wrote the full contract — schema, checks, scope, deliverables — before writing a single line of implementation code. This is unusual for a hackathon and it changes team dynamics in three ways:

1. **Alignment happens before Saturday morning.** Teams read the contract, ask questions, and agree on what success looks like before they touch a keyboard. This eliminates the "we built the wrong thing" failure mode that kills most hackathon projects.

2. **Diverse approaches become comparable.** Because every team targets the same schema and the same checks, a Python team's output is directly comparable to a TypeScript team's output. The bake-off format becomes possible.

3. **Non-engineers can contribute from minute one.** A domain expert can read the PDF alongside the contract checks and say "C2 expects net worth of $3,689,440 — here's where that number comes from on page 4." That contribution doesn't require writing code.

The risk of specification-first is over-prescription. We addressed this with the contract/reference split: lock the "what" (schema, checks, scope), free the "how" (language, framework, architecture). The reference implementation sections exist as guidance for teams that want a known-good starting point, but teams are explicitly invited to ignore them.

---

## The contract/reference split

This is the structural decision that makes the hackathon work for mixed-skill teams:

**Locked (The Contract):** What every implementation must satisfy. Schema shape, arithmetic checks, scope boundaries, deliverables. Visible at the demo. Non-negotiable.

**Free (Reference Implementation):** How to build it. Tech stack, agent architecture, timeline, team roles. Guidance only. A team that wants to use Go instead of Python, or a single-LLM-pass instead of the specialist-team pattern, is welcome to — as long as the contract is satisfied.

This split creates a healthy tension: teams are constrained enough to be comparable, but free enough to be creative. It also means "winning" is about quality and insight, not about who followed the reference implementation most faithfully.

---

## Tiered success

The biggest risk in a mixed-skill hackathon is that weaker teams feel like they failed. Tiered success addresses this:

- **Bronze (3 checks):** Sources = Uses, Ownership sums to 100%, Rent roll adds up. Any team that can extract numbers from a PDF and verify the arithmetic has achieved something meaningful.
- **Silver (6 checks):** Adds net worth reconciliation and cross-page consistency. Teams that can extract financial tables and cross-reference data across pages.
- **Gold (all 9):** Full contract. Includes DSCR ratio calculations and adjusted net worth. The stretch target for strong engineering teams.

The key insight: **Bronze is framed as a win, not as "you only got 3."** The tier system gives every team a finish line they can reach while keeping the ceiling high enough for experienced teams to push.

---

## The role of agents

AI pair programming changes hackathon dynamics fundamentally:

**What gets faster:** Scaffolding, boilerplate, library debugging, schema generation, test writing. A team with Claude Code can generate a working pdfplumber extraction loop in minutes instead of hours.

**What stays hard:** Understanding why a table extraction failed, designing the right retry path, interpreting financial data correctly, crafting a compelling demo narrative. These require human judgment that agents accelerate but don't replace.

**The creative tension:** Agents make it easy to generate code without understanding it. A team that asks Claude to "build the whole thing" will have a working pipeline but won't be able to explain or debug it. The hackathon guide addresses this by encouraging agent use as collaboration ("use it shamelessly") while framing the goal as learning ("the point is learning, not just passing the checks").

**The mixed-skill advantage:** Agents level the playing field between experienced and novice programmers. A domain expert paired with Claude Code can build a working extraction pipeline — something that would have been impossible without the agent. This is the single biggest change agents bring to hackathons: the barrier to participation drops dramatically.

---

## Short-term: what we built

For the immediate hackathon, we added:

### 1. HACKATHON.md — The Event Guide
Cultural companion to the technical contract. Covers the spirit (YOLO, mistakes = inspiration, agents as teammates), team formation (mix skills deliberately), schedule with energy beats (warm-up challenge, Wall of Fails, checkpoint demos, awards), tiered success, and a supplies checklist for the organizer.

### 2. starter-kit/ — Zero to Running in 30 Minutes
Six files that eliminate the "I don't know where to start" problem:

- **`sample-output.json`** — a hand-crafted reference output showing the exact shape teams are building toward. Every field has a source reference. Teams can literally open this file and say "this is what I need to produce."
- **`validate.py`** — standalone proofreader that runs all 9 checks against any output JSON and prints a tiered pass/fail report (Bronze/Silver/Gold). No heavy dependencies. Non-engineers can run it.
- **`quickstart.py`** — 50-line script that extracts loan terms from page 1 using Claude. Proves the round trip works: PDF to LLM to structured output with provenance. Teams fork and extend.
- **`setup-check.sh`** — verifies Python, packages, API key, and sample PDF. Green/red status per check.
- **`.env.example`** — template for environment variables.
- **`schemas.py`** — the Pydantic schema from the contract as an importable Python module.

### 3. hackathon-design-notes.md (this document)
Meta-analysis of hackathon design decisions, capturing both what we built and what we'd build next.

### 4. Updated landing page and README
Added hackathon links and pointers so new visitors land in the right place.

---

## Long-term: what we'd build to make this repeatable

These are ideas, not commitments. Captured here so they don't get lost.

### Template repo generator
A CLI or web tool that takes a new problem (different document type, different industry, different contract checks) and generates a fresh hackathon repo with the same structure: landing page, contract, reference implementation, starter kit, validator. The credit memo hackathon becomes the first instance of a repeatable template.

### Automated scoring API / leaderboard
A webhook that teams push their `output.json` to. The API runs the validator and posts results to a shared leaderboard in real time. Teams can see their tier and how they compare to other teams throughout the weekend. Gamification that drives energy without requiring the organizer to manually run validators.

### Team formation web app
A simple form where participants register with their name, skill set, and curiosity area. The app suggests balanced teams (one engineer, one domain expert, one storyteller, one quality advocate per team) and creates their communication channel automatically.

### Facilitator playbook
A minute-by-minute event management guide for the organizer: what to say at kickoff, how to run the warm-up challenge, how to facilitate the Wall of Fails, how to time checkpoint demos, how to run the awards ceremony. Includes printable handouts, timer configurations, and fallback plans for common failure modes (wifi goes down, API keys don't work, a team gets stuck).

### Multi-problem library
A catalog of hackathon-ready problems beyond credit memos: insurance claims, medical records, legal contracts, real estate appraisals, regulatory filings. Each problem has its own contract, sample document, expected output, and validator. Organizers pick a problem from the catalog and fork the corresponding template repo.

### Post-hackathon showcase site
A static site (GitHub Pages) that displays each team's approach, demo video, retrospective, and tier achieved. Serves as both a portfolio for participants and a marketing artifact for future hackathons.

### Slack/Discord bot for event coordination
A bot that posts schedule reminders, runs the validator on demand (`/validate output.json`), announces checkpoint demos, and collects Wall of Fails submissions. Reduces organizer overhead during the event.

### Dockerized environment
A `docker-compose.yml` that gives every team an identical environment: Python, all PDF libraries, LLM SDKs, Jupyter, the sample PDF, and the starter kit. Eliminates "it works on my machine" and reduces Saturday morning setup to `docker compose up`.

---

*These notes capture the thinking behind the hackathon design. The short-term deliverables are implemented and in the repo. The long-term ideas are seeds for future work.*
