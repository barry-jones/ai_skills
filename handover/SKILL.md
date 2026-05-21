---
name: handover
description: >
  Produces a structured context-transfer document ("handover") from the current conversation,
  designed to be pasted into a new chat or handed to a different AI agent to continue work.
  This is NOT a summary for human reading — it is an agent briefing that reconstructs intent,
  reasoning state, decisions made, and the exact task the receiving agent must perform, so it
  can begin work without asking questions the original conversation already answered.
  Use this skill whenever the user says things like: "hand this over", "pass this to another
  agent", "start a new chat from here", "spawn a branch", "create a handover", "distil this
  for a new session", "I want to continue this elsewhere", or any phrase implying they want
  to transfer the current conversation state to a fresh context window.
argument-hint: What will the next session focus on or do?
---

# Handover Skill

## Step 1: Identify scope

If the user hasn't specified what the receiving agent should focus on or do, ask before proceeding.
Otherwise infer it from their instruction. Determine whether this is a full-conversation handover
or a scoped branch (a subset of topics).

## Step 2: Extract the four layers

1. **Background context** — Role, system, constraints relevant to this topic only. Strip the rest.
2. **What was established** — Conclusions and decisions reached, with the reasoning where it affects
   what the receiving agent does. Not a transcript — a distillation.
3. **What remains open** — Unresolved questions, live options, unresolved trade-offs.
4. **The mission** — The explicit operative instruction to the receiving agent. Most important section.
   Be specific enough that the agent knows what to produce without asking follow-up questions.

## Step 3: Write the document

```markdown
# Handover: [Title]

> **For:** [Receiving agent's role, e.g. "A Claude instance asked to implement the sync strategy below"]
> **Date:** [Today's date]

## Context
[2–4 sentences. Who the user is, what system/workflow this relates to, relevant constraints.]

## What was established
[Bullet points. Conclusions and decisions as facts, not as "we discussed...". Include reasoning
where it would affect the receiving agent's approach.]

## What remains open
[Unresolved questions, live options, known trade-offs not yet resolved.]

## Your mission
[Specific instruction. Not "continue exploring X" but "Evaluate X given constraints A, B, C
and produce a recommendation with rationale."]

## Key terms / references
[Optional. Shared vocabulary, product names, file paths, URLs. Omit if not needed.
Do not summarise existing artifacts — reference them by path or URL instead.]
```

## Rules

- Write in third person ("The user is evaluating..."), not as a continuation of the chat
- Do not duplicate content from artifacts produced in the conversation — reference by path or URL
- Do not fabricate decisions; if something was raised but unresolved, it goes in "What remains open"
- Prefer short. A single-topic branch: ~200 words. A complex multi-topic session: 600–800 words max
- Present as a copyable code block, then offer a one-line opening prompt for the new session
- Note significant omissions if the conversation was long and content was deliberately excluded