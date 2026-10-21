---
name: qa-design
description: Use to turn a spec inventory or reference document (client feedback, PRD, acceptance criteria) into an executable verification plan — per-ID sections with pre-conditions, steps, expected functional results, UX checks and named captures — for a human or `qa-execution` to run against a deployed environment. Triggers: "design the QA plan", "turn this feedback into verification steps", "what must we check in the deployed env to close this". Tool-agnostic.
---

# QA design

out: `<feature>-qa-plan.md` in the task's delivery dir when invoked from `deliver`; else `docs/qa-evidence/<YYYY-MM-DD>/`. Plans only; captures nothing; does not pick capture tools.
in: inventory (skill `spec`) or source doc · target env URL (from profile `environments`, never production, for stimulus IDs) · production read path for observation IDs · roles/accounts needed. Missing → ask before drafting.

## Header
```markdown
# QA plan — <feature>
date · source · target env · accounts (role + login method) · captures dir
notation: ✅ pass · ⚠️ pass + UX note · ❌ fail · 🔄 not measured yet (cause + dated wait)
```

## Cross-cutting conventions (once, top)
Examples: no clipped/overlapping labels · language consistent per locale · loading states settle · errors in user words, no raw codes · disabled controls explain why · destructive actions confirm unambiguously · every new colour/badge/icon has an explanation.

## Section per ID
```markdown
## <ID> — <title>
verbatim: > <source quote, original language>
delivered: <PR / commit / flag>
pre-conditions: <specific data shape; role> · data in target env: exists (record id + how checked) | fixture to create (name, prefix or marker, how to delete) | ⚠️ not reachable (why)
mode: stimulus (test env) | observation (only real traffic shows it: metric · read-only source in production · window)
trigger: <input known to exercise this ID | estimated rate in real traffic>
steps:
1. <action> → <observable consequence>
2. [capture 1] <what is in frame, why>
expected (functional): one bullet per assertion that can fail
UX checks: visibility, spacing, tooltip/label clarity, colour meaning
captures: <id>-01-<desc>.png …
status: 🔄
```

## Smoke (regression + invariants)
- neighbour flows sharing code with the change (who imports what was touched) → one short section each.
- invariants the feature must preserve (e.g. data never leaks to an external party) → section with why + steps + expected.

## Coverage table (end)
`| ID | status | note |` pre-filled 🔄 for every ID and smoke.

## Rare paths
ID whose path fires only on some inputs (a filter, a fallback, an error branch) → before any live run, one of: an input known to fire it · a sample size from the estimated rate, with its cost, agreed if it costs money · declared not observable live up front, naming the test that covers it (status ⚠️). Never discover after the run that the path did not fire.

## Self-check
every ID has a section and a trigger · every pre-condition checked against the target env before the plan is handed over, not assumed from the spec · cold tester can run each without asking · captures named as hypotheses · conventions not repeated per section · every UI ID has ≥1 UX check · fixtures named + cleanup tag.

UX heuristics: new colour indicator → explanation check · new action → disabled-state reason · auto-applied value → visible + overridable · new column → readable at smallest viewport, aligned by type · new error → user words.
