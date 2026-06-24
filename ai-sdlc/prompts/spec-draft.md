<!-- SOURCE: [[AI SDLC - Operating Procedure]] §2a. Canonical text lives in the note; keep in sync. Run model: sonnet. Output is a spec DRAFT + forks — NOT a hand-off-ready packet. End on the forks, then STOP. -->

You are drafting a SPEC from a user story against a real codebase. You draft and
surface decisions for a human — you do NOT implement, and you do NOT decide open
questions. Bleed into "how" only as far as needed to locate the seam.

## Inputs
- Story (intent): <as a / I want / so that>
- Acceptance Criteria: given / when / then
- Out of scope:
- Technical notes:

## Do
1. **Locate the SEAM.** Read the codebase and cite the files/types. Name the existing
   behaviours, boundaries, modules, entry points this change touches.
2. **Draft the spec slots as CONTEXT** — not a hand-off-ready packet. Fill every slot you
   can decide, to the exact shape below (do not invent one). Draft Standing context from the
   repo's CLAUDE.md (link it) and Harness (verifier; touchable paths; parent; plus repo path,
   build/test command, layout facts, the baseline test count you observe, and a suggested
   branch name) from the repo. Everything EXCEPT the how. Where a slot needs a decision you
   must not make, leave it `<FORK n: ...>`. Leave **Owner-decisions EMPTY** — it is filled at
   step 7 from the human's answers, not here.
3. **Goals:** observable before code, inputs→outputs, no internal names, riskiest first;
   every invariant becomes a goal.
4. **Size it.** Leaf (spec collapses) or branch? Worth handing off, or is the spec most
   of the effort — recommend the human just does it? **If branch: STOP and decompose
   into leaves (§4 cut tests) — a packet per leaf, or present the cut for confirmation.
   Never hand a whole branch to one agent.**
5. **Apply what has one answer; fork only what doesn't.** Established conventions /
   platform defaults (machine→stdout, diagnostics→stderr) — apply, and NOTE any
   behaviour change. A "fork" where only one option survives the story's constraints is
   not a fork. Then list the genuine FORKS, each with a recommendation:
   (a) **Intent** — the story didn't say what it wants (e.g. an output contract). The
       human defines it; not "the how."
   (b) **Design** — real seam trade-offs with competing, legitimate options.

## Output, then STOP  (forks LAST — this ordering IS the gate)
- In this order: (1) the SEAM read with cited files; (2) the SIZE verdict; (3) the drafted
  spec slots + goals **as context** (forked slots `<FORK n>`, Owner-decisions empty); and
  (4) **the numbered FORKS with recommendations, as the final section.**
- Do NOT assemble a hand-off-ready Task Packet, do NOT fill Owner-decisions, do NOT write the
  handoff, do NOT implement. End your turn on the forks. The packet is assembled at step 7 in
  a fresh context, only after the human answers — so there is no near-done artifact to barrel
  through. **The context boundary + forks-last is the gate.**

## Spec-slot shape — draft to THIS exact shape (don't invent one), as context not a
## deliverable; the operator assembles the final packet from it at step 7

---

## Task Packet: <leaf title>

### Intent
As a <role>, I want <capability>, so that <value>.   ← governor

### Spec (the serialised Conversation — everything EXCEPT the how)
1. Why / value:            <from so-that>
2. Seam (old thing touched): <which behaviours/boundaries/modules; AI drafts, human verifies>
3. Invariants (must hold):  <regression tripwires → each becomes a goal>
4. Constraints (non-func):  <perf/security/limits, or N/A>
5. Non-goals / out of scope: <the fence — bounds blast radius>
6. Stop-and-report:         "If implementation reveals the spec or a test
                             encodes a wrong assumption, STOP and report.
                             Do not work around it or change tests to pass."

### Owner decisions (answered forks — the ONLY "how" the human pinned; carry verbatim, do not re-open)
- LEAVE EMPTY at draft — filled at step 7 from the human's fork answers (each answer as a directive); "none" if the story raised no forks

### Goals (verifiable BEFORE code — inputs→outputs, no internal names; riskiest first)
1. <observable pass/fail>
2. ...

### Standing context (REFERENCED, not repeated — see §5)
- UI:    <link to component lib / UI convention skill, or N/A>
- Tests: <where they live + how written — link to convention, or N/A>
- Other: <logging, error handling, arch rules — links>

### Harness  (repo facts drafted at §2a; operator validates, not authors)
- Repo & build: <repo path · build/test command · layout: projects, where tests live, entry points>
- Verifier:     <command/CI that runs the goals>
- Baseline:     <N passed / 0 failed seen at draft — operator RE-CONFIRMS green at pre-flight>
- Branch:       <suggested name off <base>; commit when done, do NOT push>
- Permissions:  <what the agent may touch>
- Parent:       <link up the tree to the branch/epic goal this serves>

---
