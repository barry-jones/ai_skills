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

Present inbox items **one at a time**. Show the task and a suggestion. User responds: accept / discuss / provide context / skip. Move on only when resolved or skipped. No batching.

For each item:
- Actionable? No → delete, file as reference, or Someday/Maybe.
- Yes, under 2 min → do now.
- Yes, delegate → Waiting For with person + date.
- Yes, defer → single next physical action starting with a verb.
- Multiple actions + warrants own outcome → project. Multiple actions + fits existing project → multi-step task. Single action, no natural project → standalone.
- Always check for duplicates or related tasks.

If it can't be answered, it's not ready to leave inbox. Either think it through now, or the next action is to do that thinking.

---

## Task fields

```
title: verb-first next action
original title: if title was changed
project: name or "standalone"
waiting: person name if delegated
due date: yyyy-mm-dd if applicable
location: next / waiting / scheduled / someday
why: one line if not obvious
description: done-looks-like, deadline/horizon, dependencies, links
steps: numbered list if multi-step
time: 5m / 10m / 15m / 30m / 45m / 1h / 2h / 3h / 4h / 6h / 8h
energy: low / medium / high
context: infer — #phone (call/ring/speak), #email (send/reply/message),
         #computer (code/Rally/GitHub/Confluence/deployment),
         Personal (finance/home/family), Work (team/product/system),
         Errands (shops/post office/physical errand)
```

Infer context from the task title — don't ask unless genuinely ambiguous.

---

## Weekly review phases

**Get Clear:** Process inbox to zero. Empty-head sweep — anything not captured yet?

**Get Current:**
- Every active project has at least one next action? If not: add one or move to Someday/Maybe.
- Every project note has: why, done-looks-like, deadline/horizon, dependencies?
- Waiting For: anything overdue needing a chase?
- Flag projects with no next action — present with suggested fix.
- Flag overdue items — group by urgency.

**Get Creative:** Someday/Maybe — anything to promote? Anything to delete? New ideas to capture?

---

## Daily review

1. Process inbox (one at a time)
2. Today's work selection

---

## Today's work selection

Priority order — do not present a flat list:

1. **Overdue** — all tasks past due date. For each: title, project, due date, time. Decide: do today / reschedule / drop.
2. **Due today** — title, project, time, energy.
3. **Project-critical** — the single task that most unblocks each active project, grouped by project.
4. **Standalone / other next actions** — remaining next actions not attached to a project.

After presenting: ask which to commit to today. Produce a **Today's Plan** with selected tasks, total committed time, and energy profile.

---

## Context test (before item leaves inbox)

- Next action starts with a verb, project assigned, why noted if not obvious.
- Description has: done looks like, deadline/horizon, dependencies, links.
- Still on your mind after processing? Not enough captured — the system must carry the load.

---

## Exit / output

"done" / "stop" / "output checklist" / "exit" → immediately generate and save the checklist. Partial reviews are valid.
Auto-save after every 10 items processed.

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
