---
name: qa-design
description: Use to turn a spec inventory or reference document (client feedback, PRD, acceptance criteria) into an executable verification plan — per-ID sections with pre-conditions, steps, expected functional results, UX checks and named captures — for a human or `qa-execution` to run against a deployed environment. Triggers: "design the QA plan", "turn this feedback into verification steps", "what must we check in the deployed env to close this". Tool-agnostic.
---

# QA design

out: `docs/qa-evidence/<YYYY-MM-DD>/<feature>-qa-plan.md`. Plans only; captures nothing; does not pick capture tools.
in: inventory (skill `spec`) or source doc · target env URL (from profile `environments`, never production) · roles/accounts needed. Missing → ask before drafting.

## Header
```markdown
# QA plan — <feature>
date · source · target env · accounts (role + login method) · captures dir
notation: ✅ pass · ⚠️ pass + UX note · ❌ fail · 🔄 not run
```

## Cross-cutting conventions (once, top)
Examples: no clipped/overlapping labels · language consistent per locale · loading states settle · errors in user words, no raw codes · disabled controls explain why · destructive actions confirm unambiguously · every new colour/badge/icon has an explanation.

## Section per ID
```markdown
## <ID> — <title>
verbatim: > <source quote, original language>
delivered: <PR / commit / flag>
pre-conditions: <specific data shape; role; fixture prefix + cleanup tag if created>
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

## Self-check
every ID has a section · cold tester can run each without asking · captures named as hypotheses · conventions not repeated per section · every UI ID has ≥1 UX check · fixtures named + cleanup tag.

UX heuristics: new colour indicator → explanation check · new action → disabled-state reason · auto-applied value → visible + overridable · new column → readable at smallest viewport, aligned by type · new error → user words.
