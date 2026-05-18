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

Present inbox items 1 at a time. For each item show the formatted task and a suggestion. User responds: accept / discuss / provide context. Move to next batch when batch resolved.

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

**Infer from task content, don't ask unless unclear:**
```
context: #phone, #email, #computer, Personal, Work, Errands etc — infer from task name, tags, notes, project
```

---

## Project vs multi-step task rule

A **project** = an outcome requiring multiple actions that stands alone as its own goal, with its own why and done-looks-like.

A **multi-step task** = multiple actions that serve an existing project. File as steps under that project, not a new project entry.

A **standalone task** = a single action with no natural project home. Fine on its own.

When in doubt: fewer projects is better. A bloated project list is harder to review than a well-organised one.

---

## Context inference

Infer context from task name, existing tags, notes, and project. Do not ask. Examples:
- mentions phone number, "call", "ring", "speak to" → `#phone`
- mentions email, "send", "reply", "message" → `#email`
- mentions code, Rally, GitHub, deployment, Confluence → `#computer`
- personal finance, home, family → `Personal`
- work system, team, product → `Work`
- shops, post office, Halifax, physical errand → `Errands`

If genuinely ambiguous, make best guess and note it.

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

- Process inbox
- Scan Next Actions — pick what to do today. Prioritise by urgency, energy, time available, context. Flag anything that should be done today but isn't in Next Actions.

---

## Context test

Before any item leaves inbox:
- Task record has: next action starting with verb, project, one-line why if not obvious, link to supporting material
- Support note has: why it matters, what done looks like, deadline or horizon, dependencies, reference material
- If project still on your mind after processing — not enough captured. System should carry the load.

---

## Output — end of session

Produce a markdown manual update checklist the user applies in Nirvana.
Save to: `~/nirvana-review/YYYY-MM-DD-{mode}-checklist.md`

### Format

```markdown
# Nirvana Update Checklist — YYYY-MM-DD (Daily / Weekly Review)

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
location:
why:
description:
steps:

---

## Projects needing a next action
- [Project name] → suggested next action
```

Rules:
- Every processed inbox item appears in exactly one section. Nothing processed silently.
- Inbox items are never "new" or "deleted" — they are updated+moved or closed.
- Use `#### ` headers to separate entries — not `---` (avoids ambiguity with section dividers).
- Omit optional fields entirely when not applicable rather than leaving blank.
- `project: none` for standalone tasks with no natural project home.

---

## Considerations
- Related or duplicate tasks: always check before creating new
- Follow GTD methodology throughout
- Each item reviewed one at a time within its batch
- Batches of 5 keep momentum without overwhelming
- Display each item in task format with suggestion before asking for decision
