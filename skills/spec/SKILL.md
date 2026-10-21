---
name: spec
description: Use when work must comply with a reference someone else wrote — client feedback document, PRD, requirements, ticket acceptance criteria, regulatory constraints, QA/acceptance-test document. Extracts points with stable IDs, logs gaps that need a human, gates plan and tests against IDs, blocks scope creep, and produces a point-by-point review document with evidence. Also use when verifying finished work against a previously supplied reference.
---

# Spec

contract: the source document. Every plan step, test, commit and verification traces to an ID.

## Outputs (dir: `vcs.delivery-dir`, with or without `deliver`; slug = feature)
| file | phase | template |
|---|---|---|
| `<feature>-inventory.md` | ingest | `references/inventory.md` |
| `<feature>-gaps.md` | gaps | `references/gaps.md` |
| `<feature>-deferred.md` | any | `references/scope.md` |
| `<feature>.md` review doc | close | `references/review.md` |
evidence: `<evidence dir>/screenshots/<id>-<n>-<desc>.png` + `visual-qa.md` index; evidence dir = `live-verification.evidence-dir`.

## Steps
1. ingest: locate exact source (ambiguous reference → ask for the path; wrong version = rework). Read whole; convert binary docs to text first. One row per atomic requirement.
2. gaps: ambiguous criteria, missing client data/assets, internal conflicts, undocumented external systems, subjective words without target → gap. Present all in one pass, grouped by ID. Needs external answer → `gap-blocked` + owner + what + date asked. Workable with placeholder → stays `pending` + `assumption:` note.
3. plan gate: each step cites IDs; `Out of scope` section always present; every non-blocked, in-scope ID has ≥1 step.
4. implement: test names and commits cite IDs; scope checklist (`references/scope.md`) before any change not traceable to an ID.
5. verify: re-read the original source (not the inventory). Per ID gather evidence; UI ID → capture from deployed env, mandatory; no evidence → not `resolved`. No browser → escalate to get one; never `resolved` without the capture.
6. review doc: summary table + per-ID detail + deferred section.

## IDs and statuses
- `SPEC-<n>[a-z]`; stable, never renumbered; redundant → `out-of-scope` with reason.
- statuses: `pending` · `gap-blocked` · `out-of-scope` · `resolved` (only with evidence).
- surface: `UI` · `backend` · `infra` · `docs` · `process` → drives review depth.
- user-authorised extra → row `out-of-spec-addition`.

## Stop when
- plan step cites no ID · softening a hard requirement instead of logging a gap · UI ID `resolved` without capture · review doc lacks deferred section · implementation before plan gate.
