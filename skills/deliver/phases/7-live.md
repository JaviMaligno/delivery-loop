# Phase 7 — live verification

in: inventory (or mini-inventory) + test env serving the SHA.
out: QA plan (skill `qa-design`) executed (skill `qa-execution`): status + evidence per ID · bugs outside spec apart · regression smoke result.
done-when: every ID ✅ or ⚠️ with evidence, or ❌/🔄 explicitly escalated · visual evidence for every ID with something to see · smoke done.

status: ✅ PASS · ⚠️ PASS + note · ❌ fail · 🔄 not run. ❌/🔄 never close silently.

behaviours:
- never against `environments.production-env` (invariant).
- visual evidence: captures/recording per ID from the deployed env. No visual surface (API, queue) → real response or query, with date + env.
- regression: neighbour flows sharing code with the change (from the diff: who imports what was touched) smoke-tested live; before/after in the same env when a baseline exists.
- "read in code" never reported as "measured".
- test data → prefixed, cleaned at the end (rule `authority/[delete-exceptions]`).
- browser driver: confirm viewport non-zero and page visible before trusting clicks.

capabilities: live-verification, environments.
absent: live-verification none → HTTP/data checks only, say which IDs lack visual evidence and why.
size-variants: trivial → mini-inventory IDs + smoke.
skip-when: never.
