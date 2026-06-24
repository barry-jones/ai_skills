<!-- SOURCE: [[AI SDLC - Operating Procedure]] §6. Copy one per run; append the filled record to the note's §7 log. Operator-assembled: agent report fills 5 fields, host fills the rest. Keep in sync with §6. -->

### Run <n> — <date> — <story/epic title>
- Gateway:            <backlog / incident / AI-marked / task / technical task>
- Predicted size:     <leaf / branch + how many rungs>
- Actual size:        <what it turned out to be>                          (← agent report 6)
- Spec-weight vs reality: <did weight predict the seam? over/under?>      (← agent report 6)
- Cut tests:          <which fired, which helped, which missed> (epics/technical tasks only)
- Human gates fired:  <which of §2.3, and: could it have been automated? how?>
- Stop-and-report:    <did the agent stop when it should? false stops?>   (← agent report 4)
- Decision-survival:  <decisions in the diff ÷ decisions gated — from the output-check FORK→SLOT audit (H6)>
- Where it was hard:  <the actual friction>                               (← agent report 7)
- Cost:               <wall-clock: from orchestrator timestamps, per leaf · tokens: ⧗ from /usage (cold agent has "no counter") · est. $> 
                      <the seam-read dominates; recorded to make "worth handing off?" measurable, esp. large/multi-repo>
- Verdict:            <shipped / aborted / reshaped>                      (← output-check)
- Promote to thinking? <a durable finding → add as transition in [[SDLC and AI - Discussion]]>

<!-- Cost capture reminder: model is set per spawn (Agent `model` param). Tokens are NOT
visible to the spawned agent — run `/usage` after the session and paste the in/out delta to
fill the token half of Cost. Wall-clock is already captured host-side per leaf. -->
