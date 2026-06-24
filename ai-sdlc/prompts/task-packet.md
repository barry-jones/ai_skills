<!-- SOURCE: [[AI SDLC - Operating Procedure]] §3. The reusable core. Copy one block per leaf. SUPPLY this shape to the assembler verbatim — never name it (§T11). Keep in sync with §3 in the note. -->

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
- <FORK n>: <the answer, as a directive>   ← the deliberate exception to "no how": a
  design call the owner made (e.g. "button to the LEFT of Finish") lives here so it
  can't evaporate. Empty/`<FORK n>` at draft time; filled when the forks are answered.
  "none" if the story raised no forks.

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
- Build-model:  <haiku (default — contract-shaped) | sonnet (deep/novel seam). Orchestrator spawns at this model.>
- Parent:       <link up the tree to the branch/epic goal this serves>
