---
name: ai-sdlc
description: Run a piece of work through the AI SDLC Operating Procedure from an entry point (gateway) to a verified, recorded result. Routes the gateway, drives the core loop (shape → size → decompose → packet → handoff → run → verify → record), and spawns cold implementation agents with controlled models while capturing per-agent wall-clock and a token-fill checklist. Use when the user says "run this through the SDLC", "ai-sdlc", "take this story/defect/task through the process", names a gateway (backlog story, incident, AI-marked, task, technical task), or wants to hand a leaf to a cold agent and get a Run Record back.
---

# AI SDLC orchestrator

Runnable counterpart to **[[AI SDLC - Operating Procedure]]** (the note is canonical;
this skill is the executable harness). It takes work in at a **gateway**, runs the core
loop, **spawns cold agents with model control**, and records **wall-clock per agent + a
token-fill checklist** so "worth handing off?" stays measurable.

The note holds the *why* and the full prose. This file holds the *do-it-in-order*, plus the
two things the note can't: **model selection per spawn** and **timing capture**.

## Canonical prompts (in `prompts/`, extracted from the note — keep in sync)

| Phase | File | Note § | Model |
|-------|------|--------|-------|
| Gateway entry (router) | this file, §"Gateways" | §1 | — |
| Story → spec + forks | `prompts/spec-draft.md` | §2a | **sonnet** |
| Defect → diagnosis | `prompts/investigate.md` | §2b | **sonnet** |
| AI-marked shape-check | `prompts/gateway-ai-marked.md` | §1 | sonnet |
| Task work fast-path | `prompts/gateway-task-work.md` | §1 | sonnet |
| Technical task → cut | `prompts/gateway-technical-task.md` | §1 | sonnet |
| Task Packet shape | `prompts/task-packet.md` | §3 | — (template) |
| Handoff wrapper | `prompts/handoff.md` | §3a | — (template) |
| Assemble handoff(s) | `prompts/assembly.md` | §3b | **sonnet** |
| **Implement a leaf (cold)** | the assembled handoff | §3 run | **haiku** |
| Check the outputs | `prompts/output-check.md` | §11 (new) | **sonnet** |
| Run Record | `templates/run-record.md` | §6 | — (template) |

**Model rule (from Run 11):** the frontier model earns its keep in the *draft/judgement*,
not the *build*. Default: **sonnet** for spec-draft / assembly / output-check; **haiku**
for the per-packet implementation. A packet may override its build model (set
`Build-model:` in the handoff Harness) — bump to sonnet for a deep/novel seam, keep haiku
for contract-shaped work. **Templates are SUPPLIED to every spawn, never named** (§T11): the
implementation agent gets the full assembled handoff text, the assembler gets §3 + §3a
verbatim. Naming a section instead of pasting it = reinvented/dropped block.

## How to run it

### 0. Pick the gateway (§1)
Ask which the work is, or infer:

| Gateway | Enter with | First job |
|---------|-----------|-----------|
| Backlog story / epic | `prompts/spec-draft.md` | shape → size |
| Incident / defect | `prompts/investigate.md` | diagnose → route |
| AI-marked story | `prompts/gateway-ai-marked.md` | shape-check the flag, THEN spec-draft |
| Task work | `prompts/gateway-task-work.md` | collapse to ~2-line leaf, straight to packet |
| Technical task | `prompts/gateway-technical-task.md` | find the reference path, cut carrys into leaves |

### 1. Front half — draft + forks  (model: sonnet)
Spawn (or run inline) the gateway prompt. Output is a **spec draft + forks**, ending on the
forks. **STOP.** No assembled packet yet. Bring the forks to the human.

### 2. Human answers the forks
The irreducible job. Trivial / not-worth-it → tell the human to just do it.

### 3. Handoff — assemble  (model: sonnet, FRESH context)
Run `prompts/assembly.md` with: the §2a draft + the human's answers + `task-packet.md` +
`handoff.md` pasted in. It bakes answers into the packet and emits **one filled handoff per
leaf** + a FORK→SLOT map + block checklist. The fresh context is the gate (§T11) — do not
assemble inside the spec-draft chat.

### 4. Pre-flight
RE-confirm a green baseline (re-run the verifier; the draft's baseline count can't carry
forward). If red, stop — fix the harness before handing off.

### 5. Run each leaf — spawn a COLD agent  (model: haiku unless the packet overrides)
For each leaf, in dependency order:

1. **Record `started_at`** (wall-clock, host-side — this is the timing the agent can't give you).
2. Spawn with the `Agent` tool:
   - `subagent_type: general-purpose` (or `claude`)
   - `model: haiku`  ← or the packet's `Build-model:` override
   - `prompt:` = the **entire assembled handoff text for that leaf**, pasted verbatim
     (supplied, never named).
3. When it returns, **record `ended_at`**; `wall_clock = ended_at − started_at`.
4. The agent's final report fills §6 fields 2–8 **except tokens**: cold agents usually
   **can't see tokens** ("no counter", Run 8) — that is expected, not a failure.

### 6. Capture cost — the token-fill checklist
Model control is solved (the `model` param above). **Token/time telemetry is the gap the
user named** — handle it like this:

- **Wall-clock:** you (the orchestrator) already have it from the timestamps in step 5. This
  is per-leaf and reliable. Record it.
- **Tokens:** the spawned agent cannot self-report them. They live in the host telemetry,
  surfaced by the **`/usage`** command — which the agent cannot call and you cannot read
  programmatically mid-run. So:
  - In the Run Record Cost field, write wall-clock now, and mark tokens `⧗ from /usage`.
  - **Tell the human:** "run `/usage` after this session and paste the in/out token delta —
    I'll fill the Cost field." Do NOT guess a number (§3a item 8).
  - If a future harness exposes a token counter to agents, the handoff's report item 8 already
    asks for it; until then, host-fill from `/usage`.
- Per-leaf attribution: because each leaf is a **separate spawn**, its wall-clock is clean.
  Token attribution from `/usage` is session-level — note that, and split by leaf only if the
  human ran `/usage` between spawns.

### 7. Verify — run the output-check  (model: sonnet)
Run `prompts/output-check.md` against each returned leaf: goals→tests survival, the seam
re-run, the diff at the seam (not the whole diff), and the FORK→SLOT decision-survival audit
(H6). It produces a PASS / RESHAPE / ABORT verdict and the decision-survival ratio.

### 8. Human gates (irreducible)
Verify the seam (re-run + read the seam diff), review the un-mechanizable (naming /
abstraction / convention). The output-check feeds these; it does not replace them.

### 9. Record the run
Fill `templates/run-record.md` from: the agent's report (fields 2–8), your timestamps (Cost
wall-clock), the output-check (goal→test survival, decision-survival), and operator-only
fields (Gateway, Predicted size, Verdict, Promote). Append it to the note's §7 log. Promote
any durable finding to [[SDLC and AI - Discussion]].

## What this skill does NOT do
- It does not auto-answer forks (the human gate — §2a/§3b STOP).
- It does not push (commit only).
- It does not invent token numbers (host-fills from `/usage`).
- It does not re-read the codebase at assembly (formatting, not a third seam-read — §3b).

## Single-source debt
The `prompts/` files are extracted copies of the note's §2a/§2b/§3/§3a/§3b. **If you edit a
section in [[AI SDLC - Operating Procedure]], edit the matching file here** (and vice-versa).
The note is the source of truth for prose; these files are the source of truth for what gets
pasted into a spawn.
