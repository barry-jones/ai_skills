---
name: nirvana-review
description: Interactive GTD review session using NirvanaHQ task data. Fetches all tasks, then guides the user through inbox processing and system review one section at a time. Triggers on "weekly review", "daily review", "morning review", or "review my tasks".
---

## Getting data

Run the analysis script — it fetches, validates, and formats everything in one pass:

```
python {skill_base_dir}\scripts\analyse_tasks.py          # daily (default)
python {skill_base_dir}\scripts\analyse_tasks.py weekly   # weekly
```

`{skill_base_dir}` is shown in the skill header at the top of this file. The script:
- Auto-fetches from NirvanaHQ if today's JSON is missing (token must be cached in `~/.nirvana_review`)
- Detects and rejects raw API dumps — tells you to run `nirvana_review.py` first if needed
- Outputs SNAPSHOT, INBOX, OVERDUE, DUE TODAY, PROJECT NEXT ACTIONS, STANDALONE in one read

Read the script output and proceed. Do not query the JSON separately.

---

## Review types

**Daily (15–20 min):** Fast, execution-focused. Mind Sweep → Snapshot → Inbox → Needs Immediate Attention → Suggested Focus for Today.
**Weekly (60–90 min):** Full system review structured as GET CLEAR → GET CURRENT → GET CREATIVE. All daily sections (as GET CURRENT) plus Horizons Check, Project Health, Overdue & Waiting, Pattern Analysis, Someday/Maybe (with trigger sweep), Clean-up, Weekly Priorities.

Ask which type at the start if not specified.

---

## Orientation

From the SNAPSHOT section of the script output, present:

> **[date · mode]** X inbox · Y overdue (A actionable / B waiting) · Z due today · N active projects (M without next action) · N next actions

Then begin the review.

---

## DAILY REVIEW

### 0. Mind Sweep

Before touching the system, ask: "What has your attention right now — anything not yet captured?"

Prompt once, briefly. If anything surfaces, capture it to the inbox before proceeding. Do not dwell here — one sweep, then move on.

### 1. Inbox

Present inbox items **one at a time**. Show the task and a suggestion. User responds: accept / discuss / provide context / skip. Move on only when resolved or skipped. No batching.

Skip this section entirely if inbox is empty.

For each item:
- Actionable? No → delete, file as reference, or Someday/Maybe.
- Yes, under 2 min → do now.
- Yes, delegate → Waiting For with person + date.
- Yes, defer → single next physical action starting with a verb.
- Multiple actions + warrants own outcome → project. Multiple actions + fits existing project → multi-step task. Single action, no natural project → standalone.
- Always check for duplicates or related tasks.

If it can't be answered, it's not ready to leave inbox. Either think it through now, or the next action is to do that thinking.

### 2. Needs Immediate Attention

Group overdue actionable tasks by urgency and impact — don't list them item by item. For each cluster, note what's at stake and what a decision would look like. Lead with the tasks most likely to be blocking other people or projects. This should also include a project overview, again by urgency, we should be heading towards goals. I want a quick overview of the state of things.

Then surface external blockers: Waiting For items where the follow-up date has passed. For each, present the person, what's outstanding, and how long it's been sitting. 

Be direct. This section should create urgency where it's warranted and help the user decide what needs to move today.

### 3. Suggested Focus for Today

Apply the four GTD engagement filters to select 3–5 tasks:
1. **Context** — what can actually be done right now given location and tools?
2. **Time available** — how long does the user have before their next commitment?
3. **Energy** — match task energy demands to current energy level (ask if not obvious)
4. **Priority** — within what fits the above, lead with highest-leverage actions

Lead with things that unblock others, meet a deadline, or close a blocker. Say *why* each task matters, not just what it is.

Priority order (within the energy/context filter):
1. Anything blocking another person or project
2. Tasks due today or tomorrow
3. Project-critical next actions (the single task most unblocking each active project)
4. Standalone tasks with near-term due dates

End with: **Total committed: Xh · energy profile (Xh high / Xh medium / Xh low)**

---

## WEEKLY REVIEW

### GET CLEAR (before running the script)

Walk through this before presenting any task data:

**Collect loose materials** — "Any paper, notes, receipts, or captured items not yet in the system?"
**Empty your head** — Run a brief Incompletion Trigger sweep. Prompt across these categories (don't list them all — pick 5–7 that feel relevant and ask about them conversationally):

*Professional:* Projects started not completed · commitments to others · communications to make · reports/writing to finish · meetings to debrief · waiting for replies · professional development · financial items
*Personal:* Home/household issues · health appointments · family commitments · upcoming events · personal admin · finances · legal matters · learning goals · errands

Capture anything surfaced to the inbox before proceeding.

---

Then run the analysis script and proceed with GET CURRENT (sections 0–3 from Daily Review, but skip section 0 since we just did it) → GET CREATIVE (sections 7+).

---

### GET CURRENT

Runs all Daily sections (1–3) first, then continues:

### 4. Project Health

Review every active project. For each, show:
- Next action (or flag if missing)
- Any overdue waiting items
- Whether it's moved since last week (infer from due dates / task state)

Group into: **Moving** · **Stalled — needs a next action** · **Blocked externally**

For stalled projects: apply the Natural Planning Model — ask in order:
1. *Why* — is the purpose still clear and relevant?
2. *What* — what does success look like for this project?
3. *Brainstorm* — what are all the things that need to happen?
4. *Organize* — what's the sequence or priority among those things?
5. *Next action* — what's the single next physical action?

If the project is still on Barry's mind after this, more capture is needed. If purpose is no longer relevant → Someday/Maybe or drop.

For projects with no next action: flag prominently and don't let them pass without a decision.

### 4b. Horizons of Focus Alignment

Check that the project list reflects Barry's higher horizons. Present this as a quick scan, not an interrogation — one or two pointed questions per horizon:

**H3 (1–2 year goals):** Do the active projects collectively move the needle on his current goals (CTO of Optum UK, London Marathon, property goals, financial targets)? Any goal with no active project?

**H2 (Areas of focus):** Any area of responsibility (Family, Home, Productivity, Work, Software Development, Finances, Cooking, Personal Growth) with nothing active or no recent action — is that intentional?

**H4/H5 (Vision / Purpose):** Skip unless a project review triggered a "does this still align?" question. Flag it if so — don't force it every week.

Flag misalignments. If a goal has no project, prompt to create one or park it in Someday/Maybe. If a project has no goal-connection, prompt to check whether it still belongs active.

### 5. Overdue & Waiting Review

Group overdue items by project. For each: decide to do this week / reschedule / drop / chase.
For Waiting For items: is this person overdue? Prompt for a chase action or a decision to take it back.

### 6. Pattern Analysis

Look across the whole system and surface structural issues. Examples of things to flag:
- Tasks missing time or energy estimates — prompt to add them
- Clusters of standalones that belong together or under an existing project
- High-effort tasks (3h+) sitting in Next with no scheduling intent — they need time-blocking or breaking down
- Recurring themes in what keeps going overdue — is there a capacity or prioritisation issue?
- Projects that haven't moved in multiple weeks
- Multiple versions of the same task (duplicates, stale copies)

Be specific and honest. This section is where the review earns its keep.

### GET CREATIVE

### 7. Someday/Maybe + Creative Sweep

Review the Someday/Maybe list:
- Anything to promote to active now? (If yes → project with next action)
- Anything no longer of interest? → delete, don't hesitate

Then ask: "Any new, hare-brained, creative, risk-taking ideas — anything you've been meaning to explore or try?" Capture them here without judgement.

Final trigger check: "Anything from the week — conversations, reading, observations — that's still sitting in the back of your mind that you haven't captured?"

Treat this section as genuinely creative, not just administrative. Ideas are valid captures.

### 8. Clean-up

- Standalone tasks: scan for anything stale, dead, or that belongs under a project
- Tasks with no time/energy estimates: flag and prompt
- Completed projects that are still marked active: archive them
- Duplicates: identify and recommend which to keep

### 9. Weekly Priorities

Name 3–5 focus areas for the coming week — not a task list, but the outcomes that matter. Ground them in the project health and overdue reviews just completed. Be direct about what's most important and why.

---

## Task fields

```
title: verb-first next action
original title: if title was changed
time: 5m / 10m / 15m / 30m / 45m / 1h / 2h / 3h / 4h / 6h / 8h
energy: low / medium / high
waiting: person name if delegated
project: name or "standalone"
due date: yyyy-mm-dd if applicable
location: next / waiting / scheduled / someday
why: one line if not obvious
description: done-looks-like, deadline/horizon, dependencies, links
steps: numbered list if multi-step
context: infer — #phone (call/ring/speak), #email (send/reply/message),
         #computer (code/Rally/GitHub/Confluence/deployment),
         Personal (finance/home/family), Work (team/product/system),
         Errands (shops/post office/physical errand)
```

Infer context from the task title — don't ask unless genuinely ambiguous.

---

## Context test (before item leaves inbox)

- Next action starts with a verb, project assigned, why noted if not obvious.
- Description has: done looks like, deadline/horizon, dependencies, links.
- Still on your mind after processing? Not enough captured — the system must carry the load.

---

## Exit / output

"done" / "stop" / "output checklist" / "exit" → immediately generate and save the checklist. Partial reviews are valid.
Auto-save after every 10 items processed — write the partial checklist to the output file so progress is preserved if the session is long.

---

## Output

Save to: `~/nirvana-review/YYYY-MM-DD-{mode}-checklist.md`

Produce a markdown manual update checklist. Include only sections that have content. Use `#### ` headers to separate entries within a section (not `---`). Omit optional fields entirely when not applicable.

**Sections:**

**Today's Plan** — `- [ ] task title — Xh, energy`, grouped by project then Standalone. Header: total committed time + energy profile (Xh high / Xh medium / Xh low).

**Overdue — decisions made** — `"title" — reschedule YYYY-MM-DD / drop / doing today`

**Close in inbox** — `"title" — reason (duplicate of X / no longer relevant / etc.)`

**Inbox items — update and move** — one `#### title` block per processed item. Show changed fields only; omit unchanged. Required on every item: project, location, time, energy. Optional: title (if changed), waiting, due date, why, description, steps, context.

**Update existing tasks** — changes to tasks already in next/waiting/projects: `Task: "title" (project) — what to change and why`

**Still in inbox — unresolved** — `"title" — reason (needs more context / project not agreed / etc.)`

**New tasks to create** — genuinely new captures not yet in the system (from projects review, waiting-for chase, get creative). Same fields as inbox items.

**Projects needing a next action** — `Project name → suggested next action`

**Projects — effort summary** — table: Project | Remaining tasks | Total estimated time | Next due

**Rules:**
- Every processed inbox item appears in exactly one section. Nothing processed silently.
- Inbox items are updated+moved or closed — never treated as "new" or "deleted".
- time and energy required on all processed tasks — prompt the user if missing.
- `project: none` for standalone tasks with no natural project home.
