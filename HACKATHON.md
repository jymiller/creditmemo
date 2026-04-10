# Credit Memo Refinery — Hackathon Guide

**A weekend of building, breaking, and learning together.**

---

## The spirit

This is not a test. There is no wrong answer. There is no "behind."

A hackathon is experiential learning under a deadline — and the deadline exists to create energy, not anxiety. Mistakes are not failures; they are data. A table extraction that silently drops a negative sign is not a bug to be ashamed of — it is the exact insight that justifies building a proofreader. The Wall of Fails (see below) exists to celebrate these moments.

Think of it like design thinking: diverge, try, break, learn, converge. The pressure is the fun part.

**Three ground rules:**

1. **Your AI is your teammate.** Claude Code, Cursor, Copilot, ChatGPT — whatever you use, use it shamelessly. Your agent pair programmer is not cheating; it's the whole point of the architecture we're building. The question is not "can you write Python?" — it's "can you and your AI build something that passes the proofreader?"

2. **Every skill has a role.** You do not need to be an engineer to contribute. You need to be curious. Engineers write code. Domain experts read the credit memo and explain what matters. Storytellers craft the demo narrative. Quality advocates run the validator and interpret the results. Designers make the output beautiful. The best teams mix all of these.

3. **Ship something by 5pm Sunday.** It does not need to be perfect. It needs to exist. Bronze tier (3 checks passing) is a legitimate win. Gold tier (all 9) is a flex. Both get celebrated.

---

## Who this is for

You belong here if any of these are true:

- You write code in any language
- You've ever read a financial statement
- You've ever been frustrated by data locked in a PDF
- You're curious about how AI agents work
- You like building things under pressure
- You want to learn something new this weekend
- Someone invited you and you said "sure, why not"

**You do not need:** prior experience with PDF extraction, credit memos, Python, LLMs, or agent architectures. You need a laptop and an internet connection.

---

## Team formation

**Mix skills deliberately.** A team of four engineers will build faster but demo worse than a team with an engineer, a domain expert, a storyteller, and a quality advocate. The best hackathon teams look like a startup, not a dev shop.

### Suggested roles (not required, just helpful)

| Role | What you do | Best fit for |
|---|---|---|
| **Builder** | Write the extraction code, wire the agents, debug the pipeline | Engineers, data scientists |
| **Domain interpreter** | Read the credit memo, explain what the numbers mean, spot extraction errors that code can't | Finance people, analysts, anyone who's seen a loan file |
| **Quality advocate** | Run `validate.py` early and often, interpret the results, tell the builder what's wrong | Anyone comfortable with a terminal and reading error output |
| **Demo storyteller** | Own the 5-minute walkthrough, craft the narrative, make the audience care | PMs, designers, anyone who's ever presented |

A two-person team can combine roles. A solo participant can do all four with an AI teammate. There's no minimum team size.

### How to form teams

**If you're the organizer:** At Saturday morning kickoff, ask everyone to introduce themselves with one sentence: name, skill, and one thing they're curious about. Then let people self-organize into teams of 2-4, optimizing for skill diversity over friendship. Shuffle if any team is all-engineers or all-non-technical.

**If you're remote:** Pick a team in the Discord/chat channel. Or go solo with your AI — a solo builder with Claude Code can absolutely hit Bronze by Sunday.

---

## The challenge

**One PDF goes in. Verified structured data comes out.**

Your team processes `Sample-Enhanced-Memo.pdf` — a 22-page credit memo for a $514,500 multifamily real estate loan — and produces a JSON file matching the contract schema. A proofreader (the validator) checks the math. Every field traces back to the page it came from.

The full technical contract is in [demo-requirements.md](demo-requirements.md) (sections 1-9). The TL;DR:

- **Extract** header fields, financial tables, and narrative sections from the PDF
- **Verify** the extraction using 9 arithmetic checks (sources = uses, net worth reconciles, DSCRs match, etc.)
- **Show provenance** — for any extracted value, point at the source page
- **Demonstrate error recovery** — show at least one case where the first extraction attempt was wrong and the system caught and corrected it
- **Demo it** in a 5-minute walkthrough Sunday afternoon

### Tiers — what "done" looks like

| Tier | Checks passing | What it proves |
|---|---|---|
| **Bronze** | C1 + C5 + C8 (3 of 9) | "We can extract numbers from a PDF and the math adds up" |
| **Silver** | + C2 + C4 + C9 (6 of 9) | "We can extract tables and cross-reference across pages" |
| **Gold** | All 9 | "Full contract satisfied — the proofreader is happy" |

**Bronze is a win.** Say it again: Bronze is a win. A team that hits Bronze built a working extraction pipeline with arithmetic verification in a weekend. That's not trivial — that's the hard part of the whole supply chain.

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
   Fix anything that says FAIL. If you're stuck, ask your team or the organizer.

3. **Look at what success looks like:**
   ```
   cat sample-output.json | python3 -m json.tool | head -50
   ```
   This is the shape your output needs to match. Every field has a `source` showing where it came from.

4. **Run the validator on the sample:**
   ```
   python3 validate.py sample-output.json
   ```
   You should see 9/9 PASS, GOLD tier. This is your target.

5. **Run the quickstart:**
   ```
   python3 quickstart.py
   ```
   This extracts loan terms from page 1 using Claude. You now have a working PDF-to-LLM-to-JSON pipeline. Extend it.

6. **Start building.** Fork `quickstart.py` or start fresh in your preferred language. The contract is in [demo-requirements.md](demo-requirements.md) sections 5-8.

---

## Schedule

Adapt to your timezone and team energy. This is a guide, not a mandate.

### Saturday — Build

| When | What | Energy |
|---|---|---|
| 09:00 | **Kickoff.** Intros, team formation, read The Contract together. Open the PDF. | High |
| 09:30 | **Warm-up challenge.** Every team runs `quickstart.py` and modifies it to extract one additional field. First team to extract the borrower's name wins bragging rights. | Fun |
| 10:00 | Teams start building. Builder codes; Domain Interpreter reads the PDF; Quality Advocate runs the validator periodically. | Focus |
| 12:00 | Lunch. Talk about what's working and what's weird. | Recharge |
| 13:00 | Deep work continues. Financial tables are hard — this is where the real learning happens. | Grind |
| 16:00 | **Checkpoint demo.** Each team shows what they have in 2 minutes. No slides. Just the terminal or UI. Celebrate progress, not polish. | Energy boost |
| 16:30 | **Wall of Fails.** Each team shares their most surprising extraction error. Best fail wins a prize. | Laughter |
| 18:00 | Dinner. Optional: keep building, or take a break and come back Sunday. | Flexible |

### Sunday — Verify and Demo

| When | What | Energy |
|---|---|---|
| 09:00 | Resume building. Focus on getting the validator to pass. Quality Advocate drives. | Focused |
| 11:00 | **Error recovery.** Implement at least one retry/fallback path. This is the demo's money moment. | Critical |
| 12:00 | Lunch. | Recharge |
| 13:00 | Polish the demo surface (CLI, UI, or static HTML). Demo Storyteller takes over. | Creative |
| 14:00 | **Dry run.** Each team runs through the 5-minute demo script once. Time it. | Practice |
| 15:00 | Record a backup video of the demo (insurance against live-demo gremlins). | Safety net |
| 16:00 | **Final demos.** Each team presents for 5 minutes. Audience: the other teams + any invited guests. | Showtime |
| 16:45 | **Awards ceremony.** See categories below. | Celebration |
| 17:00 | **Retrospective.** What worked, what surprised you, what would you tell your past self from Saturday morning? | Reflection |

---

## Awards

Not just "best extraction." Every team has a shot at something.

| Award | Criteria |
|---|---|
| **Gold Standard** | Highest tier achieved (Gold > Silver > Bronze, tiebreak: most checks passing) |
| **Most Creative Approach** | Unusual architecture, unexpected tool choice, or a left-field idea that worked |
| **Best Recovery Story** | Most impressive error-detection-and-correction path — the demo punchline |
| **Best Use of Agents** | Most effective use of AI pair programming during the build process |
| **Best Demo Storytelling** | Best 5-minute narrative — clarity, energy, connection to the business case |
| **Most Surprising Insight** | Something nobody expected to learn — about the data, the tools, or the problem |
| **Best Team Name** | Self-explanatory |
| **Best Fail** | Most entertaining or instructive extraction error from the Wall of Fails |

---

## Working with agents

Your AI pair programmer is a first-class teammate. Here are ways to use it well:

- **"Read this PDF page and extract the loan amount as JSON."** — Start with the simplest possible prompt and iterate.
- **"This pdfplumber table extraction has a merged header on page 5. What's going wrong?"** — Use your agent to debug library-specific issues.
- **"Write a function that checks if sources equal uses."** — Let the agent scaffold the proofreader checks, then review.
- **"I have this JSON output. Run through the 9 checks in demo-requirements.md section 8 and tell me which ones fail."** — Use it as a manual validator while building.
- **"Help me write a 5-minute demo script that maps our extraction to the four-stage supply chain."** — The Demo Storyteller's best friend.

**What NOT to do:** Don't ask the agent to build the entire solution in one shot and submit it without understanding it. The point is learning, not just passing the checks. Use the agent as a collaborator, not a contractor.

---

## Capturing feedback

We want to hear about your experience — what worked, what was confusing, what was fun, what you'd change.

- **During the event:** Drop notes, screenshots, and reactions in the GitHub Discussions tab on the repo (`github.com/jymiller/creditmemo/discussions`). There's a "Hackathon Feedback" discussion thread pinned for this purpose.
- **After the event:** Each team submits a one-page retrospective as part of the deliverables (see the contract in demo-requirements.md section 9).
- **Informally:** Text, Slack, email — whatever's natural. The organizer will capture the highlights.

---

## Supplies checklist (for the organizer)

- [ ] Wifi that actually works
- [ ] Power strips at every table
- [ ] Post-its and markers (for architecture sketching)
- [ ] Timer visible to all teams (for checkpoint demos and final presentations)
- [ ] Snacks and drinks (all day — not just lunch)
- [ ] Music (background playlist, nothing with lyrics during focus blocks)
- [ ] Printed copies of the contract (demo-requirements.md sections 1-9) for each team — sometimes paper is faster than scrolling
- [ ] A wall or whiteboard for the Wall of Fails
- [ ] Small prizes for each award category (stickers, gift cards, bragging rights)
- [ ] A way to record final demos (phone camera is fine)

---

## Quick links

| Resource | Link |
|---|---|
| GitHub Pages hub | [jymiller.github.io/creditmemo](https://jymiller.github.io/creditmemo/) |
| Video walkthrough | [Loom](https://www.loom.com/share/8e1d2384a0e642e8896f36a2a60927d9) |
| Technical contract | [demo-requirements.md](demo-requirements.md) (sections 1-9) |
| Reference implementation | [demo-requirements.md](demo-requirements.md) (sections 10-16) |
| Strategic brief (the "why") | [credit-memo-extraction-explainer.html](https://jymiller.github.io/creditmemo/credit-memo-extraction-explainer.html) |
| Executive one-pager | [one-page-brief.html](https://jymiller.github.io/creditmemo/one-page-brief.html) |
| Starter kit | [starter-kit/](starter-kit/) |
| Sample output | [starter-kit/sample-output.json](starter-kit/sample-output.json) |
| Validator | [starter-kit/validate.py](starter-kit/validate.py) |

---

*The best hackathon outcome is not the code. It's the team that built it, the things they learned, and the stories they'll tell on Monday.*
