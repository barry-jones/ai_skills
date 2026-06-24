<!-- SOURCE: [[AI SDLC - Operating Procedure]] §3a. The agent-facing wrapper around the §3 packet. This whole text is what the orchestrator pastes into the COLD implementation spawn (model: haiku unless the packet's Build-model overrides). SUPPLY verbatim — naming it = dropped blocks (§T11). Keep in sync with §3a. -->

You are picking up a development ticket on an existing <stack> project. Work
only from this ticket and the code in the repository. Where the ticket says
STOP AND REPORT, follow it — do not work around it. Each `##` section below is
already filled in or marked N/A by the operator who assembled this handoff
(the operator's tick-every-block step is the guard against a dropped section —
§9, §12); treat every section as present and address it.

## Repository & setup  (carried from the packet Harness — confirm, don't re-author)
- Repo / build / layout / permissions: per the packet Harness.
- Branch: create & switch to the packet's suggested <branch> off <base>; commit, do NOT push.
- Baseline green CONFIRMED now: <N> passed, 0 failed. Every existing test must still pass.
  ← the one fact the packet can't carry forward; re-run at pre-flight.
- Verifier gates (MECHANICAL — the run's pass is the gate's verdict, not your "all green"):
  the verifier may enforce changed-line coverage (Coverlet), a goal→test trait map
  (`[Trait("Goal",<id>)]` per goal), and the public-API analyzer. If a gate fails, fix the
  code or the test — these are checks, not advice (§10 ledger, §12). N/A if none are wired yet.

## Ticket: <title>
── the §3 Task Packet, verbatim: Intent · Spec · Owner decisions · Goals · Standing context · Harness.
   Carry Owner decisions VERBATIM — do not re-open or drop (Run 9 lost FORK 2 here).

## Standing conventions (match the codebase — as important as the feature)
- Comments: <e.g. XML only on public members; // on internal/private>
- Surface:  <e.g. internal-by-default; widen via InternalsVisibleTo, not public>
- Abstraction: prefer a little duplication over premature abstraction (rule of three)
- Single source of truth for any value that must stay consistent
- Tests: <framework + match the style of existing tests at <path>>
  (Be SPECIFIC and actionable — "follow existing conventions" does NOT work.)

## Your final report must include (concise, factual). It feeds the §6 Run Record —
## the `(→ §6 …)` tags say which field each line fills; fill what you can know:
1. Branch name + files changed.
2. Test result: total/passed/failed + new test names with pass/fail.
2a. GOAL→TEST MAP: list EVERY packet Goal and the NAME of the test that covers it; for a
    goal with no test write "none" and say why (e.g. UI with no automation surface, §9 —
    mark manual-QA). This is a factual map you PRODUCE, not a pass you self-judge: coverage
    is decided host-side by a mechanical check that fails the run if a reachable-surface goal
    (CLI/contract/API or a layered view-model) maps to "none" (§10 — goal→test coverage gate).
    A self-reported "all green" is not coverage. (Run 11: two leaves shipped green with 0
    tests for unit-testable goals — the prose STOP that used to live here leaked; §12.)
    (→ §6 goal→test survival, H6)
3. Key implementation choices made (and how, for the riskiest seam point).
4. Any STOP AND REPORT trigger hit, and any assumption you had to make.  (→ §6 Stop-and-report)
5. Anything in the ticket that was wrong, ambiguous, or encodes a mistaken assumption.  (→ §6 Promote)
6. Did the work turn out HEAVIER or LIGHTER than the packet implied — was the seam
   deeper/shallower than the Spec slot described? Say which, and why.  (→ §6 Actual size + Spec-weight vs reality)
7. Where the genuine FRICTION was — the part that was actually hard, not the boilerplate.  (→ §6 Where it was hard)
8. Your run COST: wall-clock always; tokens in/out only if the harness exposes them
   — if it doesn't, say "no counter" (cold agents usually can't see tokens, Run 8) and
   the host fills tokens from telemetry (`/usage`). Don't guess a number.  (→ §6 Cost)

(Operator-only §6 fields the agent can't see — Gateway, Predicted size, Human gates
fired, Verdict, Promote-decision — are filled host-side when the record is written.)
