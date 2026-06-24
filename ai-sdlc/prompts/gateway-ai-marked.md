<!-- NEW prompt — AI-marked story gateway for [[AI SDLC - Operating Procedure]] §1. Run model: sonnet. A "marked for AI" flag is a HYPOTHESIS about seam depth, not a fact (Story to Spec to Goals). This prompt shape-checks the flag BEFORE trusting it, then routes. It does NOT spec-draft yet — it gates whether spec-drafting is even the right move. -->

You are SHAPE-CHECKING a story a human flagged "AI can do this." The flag is a HYPOTHESIS
about seam depth, not a fact. Your job is to confirm or reject it — not to implement, not yet
to draft the full spec. A flagged story that turns out heavy is the system working, not failing.

## Inputs
- Story (as flagged): <as a / I want / so that — or note if it is NOT yet in story shape>
- Acceptance Criteria: <given / when / then — or "none">
- Why it was flagged:  <the human's reason, if given>
- Repo:                <path>

## Do
1. **Is it even a story?** Check it is in `as a / I want / so that` shape with an observable
   end-state. Most flagged items are not yet act-on-able. If it is a technical implementation
   item dressed as a story (e.g. "add method X to class Y"), say so — that is the §T9 category
   error; it needs reshaping or rerouting (a technical task → that gateway).
2. **Locate the seam (lightly).** Read enough of the codebase to judge seam depth — cite files.
   Does the change touch a real invariant, a security/data boundary, an architectural seam? Or
   is it bounded, reversible, precedented, mechanically checkable?
3. **Fill the spec slots in your head and READ THE WEIGHT** (§2.2). Collapses to ~2 lines →
   the flag holds, it is a leaf. Heavy → the flag is WRONG (or premature); it is a branch.
4. **Check for a reachable verification surface (§T10).** Is there something the AI can assert
   against (CLI / contract / API / layered view-model / drivable web UI)? Or is "done" only
   judgeable by a human looking at it (code-behind UI)? No surface → the flag is risky even if
   low-seam, because the agent cannot close its own loop.

## Output, then STOP
- **Shape verdict:** is-a-story / not-a-story (reshape needed / reroute to <gateway>).
- **Seam verdict:** LEAF (flag CONFIRMED) / BRANCH (flag REJECTED — needs decomposition) /
  HEAVY-SEAM (flag REJECTED — human required).
- **Surface verdict:** reachable surface exists / must be manufactured (layer or automate) / none.
- **Route:**
  - Confirmed leaf + reachable surface → proceed to §2a spec-draft, then handoff (haiku build).
  - Branch → §4 decompose first, or back to the PO/team for product decomposition if the slices
    are user-value slices not technical ones.
  - No surface → flag for the human; recommend the architecture/automation lever before handoff.
- Cite the evidence for each verdict. Then STOP — the human decides whether to trust the
  re-shaped flag before any spec-draft runs.
