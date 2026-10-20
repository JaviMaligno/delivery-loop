---
name: deliver
description: Use when a task must be delivered end to end — from a ticket, a client/requirements document or a request to a change verified live in a non-production environment, promoted and closed. Triggers, in any language: a ticket id or URL with intent to build, fix or change something ("implement ABC-123", "implementa PROJ-45", "arregla <ticket>", "haz el ticket X"), "build/fix this end to end", "take this to done", a requirements document to comply with. Invoke it before touching code for such a request, even when the change looks small: phase 0 finds work already done and sizes the task, and a trivial size skips spec, gaps and plan. Adapts to the environment through layered profiles (tracker, CI, deploy, reviewers, verification tools). Not for read-only questions or exploration without a deliverable.
---

# Deliver

## Start
1. merge: `python "<this skill dir>/../../scripts/merge_profiles.py" --cwd <dir>`; interpreter `python` → `py -3` → `python3`.
   - exit 1 → fix the named `file:line`. exit 3/4 → census after the workspace exists (phase 0).
2. merged profile = authority for this task; each item tagged `← Ln`.
3. phase 0 creates the workspace → re-merge with `--cwd <workspace>`; that merge is the one that rules.
   - resume: phase 0 finds the entry phase from evidence (branches, PRs, deploys), not from the tracker state; work can start at any phase.
4. load `phases/<n>-*.md` when entering phase n; never all at once; log `phase <n> loaded` in the task file.
5. re-merge on entering phases 6 and 7: rules can change mid-task. Diff against the ruling merge → changed items in the task file; a changed item that affects a recorded decision → rule `transversal/[decision-change]`.

## Phases
| # | phase | done-when (summary) |
|---|---|---|
| 0 | start | workspace; profile valid; capabilities resolved or escalated; size; D0.x |
| 1 | spec | every source point has an ID or exclusion reason |
| 2 | gaps | no open gap blocks the plan |
| 3 | plan | agent-reviewed; every ID has a step |
| 4 | implement | zone tests green, executed |
| 5 | review | no blocking finding open |
| 6 | integrate | test env serves the exact SHA |
| 7 | live | every ID PASS with evidence or escalated; regression smoke done |
| 8 | promote | merge to production branch verified against git |
| 9 | close | tracker + git state = report |

## Size (phase 0, written with reason)
| size | path |
|---|---|
| trivial | 0 (mini-inventory) → 4 → 5 → 6 → 7 → 8 → 9 |
| feature | 0–9 |
| large | 0–9; phase 1 baseline inventory + parallel readers + completeness critic; phase 3 one plan per PR, human checkpoint between PRs |

## Task file
`.delivery/tasks/<slug>.md`: `owner: <session name> · since <UTC>` · size+reason · mini-inventory (trivial) · D0.x · escalations + answers · waits · phase log.
- log line: `<UTC from date -u> · phase <n> · <what> · <evidence pointer>`; never a time from memory.
- written as each step closes, not at phase end: a session can die mid-phase.

## Authority
- action → class → policy: merged `## authority` (`<action>: <class>`, `class-<class>: <policy>`).
- `ask-never` → act. `ask` / `show-text-first` → one question, 2–4 options, recommended first; continue independent work meanwhile.
- action with `· owner <who>` (another session or person) → coordinate with the owner, don't act; rule `authority/[action-owner]`.
- waiting on anyone (owner, peer session, human) → rule `authority/[waits]`: deadline + default written before waiting.
- answer → profile if durable, else task file.
- invariants never crossed, even if asked mid-task → state the invariant and its level.

## Transversal
merged `## transversal` rules apply in every phase.

## Delegation
session has a skill for a phase's discipline (brainstorming, TDD, debugging, plan writing, code review, verification) → may run inside the phase; phase contract decides done.

## Report (end, and on any stop)
decided+why · open (options + recommendation) · assumed · out of scope · where to look (PR, task file, evidence) · "requested works" vs "rest still works".
