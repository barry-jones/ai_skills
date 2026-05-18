---
name: nirvana-review
description: Interactive GTD review session using NirvanaHQ task data. Fetches all tasks, then guides the user through inbox processing and system review one section at a time. Triggers on "weekly review", "daily review", "morning review", or "review my tasks".
---

## Review types

**Daily (15–20 min):** Process inbox → scan Next Actions → pick today's work.
**Weekly (60–90 min):** Get Clear → Get Current → Get Creative. Full system review.

Ask which type at the start if not specified.

---

## Inbox processing

Present inbox items **one at a time**. Show the formatted task and a suggestion. User responds: accept / discuss / provide context / skip. Move to next item only when current item is resolved or skipped. No batching.

For every item work through:
- What is this, exactly?
- Is it actionable?
  - No → delete, file as reference, or move to Someday/Maybe
  - Yes, under 2 min → do it now
  - Yes, delegate → Waiting For with person + date
  - Yes, defer → define single next physical action starting with a verb
- One action closes it, or needs more?
  - More than one action AND warrants its own outcome → project
  - More than one action AND fits inside an existing project → multi-step task, not a new project
  - Single action with no natural project home → standalone task (not everything needs a project)
- Always check: is this a duplicate or related to an existing task or project in the system?

If the item cannot be answered, it is not ready to leave the inbox. Either do the thinking now or the next action is to do the thinking.

---

## Task fields

**Collect during review:**

```
title: single next action starting with a verb
original title: original text if title was changed
project: project name (or "standalone")
waiting: person name if delegated
due date: yyyy-mm-dd if applicable
location: inbox / next / waiting / scheduled / someday
why: one line if not obvious
description: supporting context — why it matters, what done looks like, dependencies, links
steps: numbered list if multi-step task
time: 5m / 10m / 15m / 30m / 45m / 1h / 2h / 3h / 4h / 6h / 8h
energy: low / medium / high
```

**Infer from task content, don't ask unless genuinely ambiguous:**
```
context: infer from task — #phone (call/ring/speak to), #email (send/reply/message), #computer (code/Rally/GitHub/deployment/Confluence), Personal (finance/home/family), Work (team/product/system), Errands (shops/post office/physical errand)
```

---

## Weekly review phases

### Get Clear
- Process inbox to zero using rules above
- Empty head — anything not captured yet?

### Get Current
- Every active project: does it have at least one next action? If not, add one or move to Someday/Maybe
- Every project: does support note have why, done-looks-like, deadline/horizon, dependencies?
- Waiting For list: anything overdue needing a chase?
- Flag projects with no next action — present to user with suggested fix
- Flag overdue items — group by urgency

### Get Creative
- Someday/Maybe: anything now relevant to promote? Anything to delete?
- New ideas to capture?

---

## Daily review

1. Process inbox (one at a time)
2. Today's work selection (see below)

---

## Today's work selection

Do not present a flat list. Structure in priority order:

### 1. Overdue (must address)
All tasks past due date. For each: title, project, due date, time estimate. User decides: do today / reschedule / drop.

### 2. Due today
Tasks due today. Format: title, project, time, energy.

### 3. Project-critical next actions
For each active project, the single task that most unblocks progress. Grouped by project.

```
[Project name]
  → [task title]
     time: Xh  energy: low/med/high  due: YYYY-MM-DD or none
```

### 4. Standalone / other next actions
Remaining next actions not attached to a project. After the above groups.

After presenting: ask which to commit to today. Produce a **Today's Plan** in the checklist with selected tasks, total committed time, and energy profile.

---

## Context test

Before item leaves inbox:
- Next action starts with verb, project assigned, why noted if not obvious
- Description has: done looks like, deadline/horizon, dependencies, links
- Still on your mind after? Not enough captured — system must carry the load

---

## Exit / output at any time

User can say **"done"**, **"stop"**, **"output checklist"**, or **"exit"** at any point. On any of these: immediately generate and save the markdown checklist for all decisions made so far. Partial reviews are valid.

Also auto-save after every 10 items processed, in case session is interrupted.

---

## Output

Produce a markdown manual update checklist the user applies in Nirvana.
Save to: `~/nirvana-review/YYYY-MM-DD-{mode}-checklist.md`

### Format

```markdown
# Nirvana Update Checklist — YYYY-MM-DD (Daily / Weekly Review)

---

## Today's Plan
Total committed time: Xh Xm
Energy profile: Xh high / Xh medium / Xh low

### [Project name]
- [ ] [task title] — Xh, high energy

### Standalone
- [ ] [task title] — 15m, low energy

---

## Overdue — decisions made
- "[title]" — [reschedule to YYYY-MM-DD / drop / doing today]

---

## Close in inbox
- "[original title]" — reason (e.g. duplicate of "X", no longer relevant)

---

## Inbox items — update and move
Existing inbox items that have been processed. Update fields in Nirvana then move to the correct location.

#### [original title or updated title]
title: updated title if changed (omit if unchanged)
project: project name — or "none" if standalone
context: Work / Personal / #phone / #email / #computer / Errands etc
waiting: person name (omit if not applicable)
due date: YYYY-MM-DD (omit if not applicable)
location: next / waiting / scheduled / someday
time: 5m / 10m / 15m / 30m / 45m / 1h / 2h / 3h / 4h / 6h / 8h
energy: low / medium / high
why: one line if not obvious (omit if obvious)
description: updated description — why it matters, done looks like, dependencies, links
steps:
  1. first action
  2. second action
  (omit if single action)

---

## Update existing tasks
Changes to tasks already in next / waiting / projects (not inbox items).

- Task: "[title]" ([current project])
  Change: [what to update and why]

---

## Still in inbox — unresolved
- "[original title]" — reason (e.g. needs more context, project not agreed)

---

## New tasks to create
Genuinely new tasks not captured anywhere yet (e.g. from projects review, waiting for chase, get creative).

#### [title]
title:
project:
context:
waiting:
due date:
time:
energy:
location:
why:
description:
steps:

---

## Projects needing a next action
- [Project name] → suggested next action

---

## Projects — effort summary

| Project | Remaining tasks | Total estimated time | Next due |
|---------|----------------|----------------------|----------|
| [name]  | X tasks         | Xh Xm                | YYYY-MM-DD |
```

Rules:
- Every processed inbox item appears in exactly one section. Nothing processed silently.
- Inbox items are never "new" or "deleted" — they are updated+moved or closed.
- Use `#### ` headers to separate entries — not `---` (avoids ambiguity with section dividers).
- Omit optional fields entirely when not applicable rather than leaving blank.
- `project: none` for standalone tasks with no natural project home.
- time and energy required on all processed tasks — prompt if missing.

