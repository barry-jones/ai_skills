<!-- SOURCE: [[AI SDLC - Operating Procedure]] §3b. Step-7 prompt. Run model: sonnet, in a FRESH context (not the spec-draft chat — the boundary is the gate, §T11). PASTE task-packet.md + handoff.md alongside this prompt; never just name them. Keep in sync with §3b. -->

You are ASSEMBLING a cold-agent handoff. You are given a SPEC DRAFT + a FORK LIST
(from the §2a prompt), the HUMAN'S ANSWERS to those forks, and two templates (the §3
Task Packet shape and the §3a handoff shape). Your job is to FILL them — bake the
answers in and produce a ready-to-paste handoff PER LEAF. You do NOT re-read the
codebase, do NOT implement, and do NOT re-open or second-guess answered forks.

## Inputs (the operator pastes all of these — if any is missing, STOP and ask for it)
- §2a output: the SEAM read, SIZE verdict, the drafted spec slots + goals (as context),
  and the numbered FORKS with recommendations.
- The HUMAN'S FORK ANSWERS (one per fork; or "applied the recommendation" for a design fork).
- The §3 Task Packet template (the exact shape to fill).
- The §3a handoff template (the exact wrapper to fill).
  (Templates must be GIVEN, never named — if you were only told a section's name, STOP.)

## Do
1. **Pre-check (design-correctness).** Before baking, scan the answers + goals for an internal
   contradiction — an example that disagrees with its prose, or an allowed-vs-excluded /
   include-vs-exclude / on-vs-off flip. Trace ONE concrete worked example through the design.
   If anything contradicts, STOP and reconcile with the human. Do not bake a contradiction in.
2. **Check fork answers are sufficient.** Any INTENT/contract fork left unanswered → STOP and
   ask the human; do NOT invent the answer. A DESIGN fork may be applied with its §2a
   recommendation — record it as a directive in Owner-decisions and note "(applied §2a rec)".
3. **Assemble the §3 Task Packet per leaf**, to the supplied shape exactly. Bake each answer
   into its spec slot (Intent / Invariants / Constraints / Goals as appropriate) AND into the
   **Owner-decisions** block, verbatim, as a directive. If an answer has no slot to live in,
   ADD a slot for it — never drop it. Replace every `<FORK n>` with the baked answer; the packet
   must contain NO `<FORK n>` and NO empty Owner-decisions when you are done. Do NOT re-read the
   repo — carry the Harness/baseline/branch from the §2a draft as-is. Set each packet's
   Build-model (haiku default; sonnet if its seam is deep/novel).
4. **Wrap each packet in the §3a handoff**, filling every block: Repository & setup (carry the
   Harness; mark baseline "operator RE-confirms green at pre-flight"); Ticket (the assembled §3
   packet, verbatim); Standing conventions (the CLAUDE.md link or the specific list from the
   draft); Stop-and-report (carried); Final report (all 8 items incl. cost AND the goal→test
   map). A block that is genuinely irrelevant is marked `N/A` — never deleted.
5. **One handoff per leaf**, in dependency order; name the branch each is off (per the cut).

## Output, then STOP
- For each leaf: the COMPLETE filled §3a handoff, ready to paste into a cold agent (no
  placeholders, no `<FORK n>`, no empty blocks).
- Then a **FORK→SLOT MAP**: every fork number → the answer → the exact slot(s) it landed in
  (e.g. "FORK 2 → 'open the timestamped subdir' → Owner-decisions + Goal 3"). Any fork whose
  answer you could not place is a STOP, not a silent drop.
- Then the **BLOCK CHECKLIST**: tick each of the five §3a mandatory blocks as filled or `N/A`.
- Do NOT implement. End here. The operator confirms baseline-green and hands each leaf to a
  fresh cold agent.
