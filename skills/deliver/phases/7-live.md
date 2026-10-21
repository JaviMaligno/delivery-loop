# Phase 7 — live verification

in: inventory (or mini-inventory) + test env serving the SHA; observation IDs: production serving it.
out: QA plan (skill `qa-design`) executed (skill `qa-execution`): status + evidence per ID · bugs outside spec apart · regression smoke result.
done-when: every ID ✅ or ⚠️ with evidence, ❌ escalated, or 🔄 with its cause and a dated wait · visual evidence for every ID with something to see · smoke done.

status: ✅ PASS · ⚠️ PASS + note · ❌ fail · 🔄 not measured yet. ❌/🔄 never close silently. 🔄 always carries its cause and a dated wait (rule `authority/[waits]`) or an escalation; ⚠️ is never used for something not measured.

behaviours:
- first: re-merge + diff against the ruling merge (deliver Start 5), logged.
- each ID has a mode (from `qa-design`): stimulus → exercised in the test env; observation → only real traffic shows it (rate, latency, an error that stopped) → production read only, per rule `environments/[observe-not-test]`: metric · source · window. Window not over, source unreachable, or the change reaches production only at phase 8 → 🔄 with a wait until it can be read (after phase 8 if needed); independent IDs go on.
- never a stimulus or a write against `environments.production-env` (invariant).
- act only as `live-verification.test-identity` when set; another account (found in a doc, memory, credentials file) → rule `transversal/[source-conflict]`, never just use it.
- visual evidence: captures/recording per ID from the deployed env. No visual surface (API, queue) → real response or query, with date + env.
- regression: neighbour flows sharing code with the change (from the diff: who imports what was touched) smoke-tested live; before/after in the same env when a baseline exists.
- "read in code" never reported as "measured".
- test data → prefixed (or marked in another field when the id comes from the data), cleaned at the end (rule `authority/[delete-exceptions]`). Not reversible → record in the ticket what changed and its previous value; that is a valid close.
- each fixture, the moment it is created → a `pending cleanup` line in the task file (id, env, how to delete it); struck when cleaned. Leaving with lines still pending (env down, session ending) → write them in the ticket first.
- evidence → `live-verification.evidence-dir` (default `<delivery-dir>/evidence/`); never a session temp dir or a workspace, both deleted before the task's record is.
- fix loop: a pass finds in-scope defects → finish the pass, then ONE fix branch with all of them → phases 4–6 once → full pass again. Never one cycle per defect. Phase closes only on a clean pass; out-of-scope findings → bugs list.

capabilities: live-verification, environments.
absent: no browser tool in the profile → any browser automation the session has; none → escalate once to get one connected (the tool is personal, the visual check is not); IDs with something to see never close on HTTP/data checks alone · no visual surface at all (API, queue) → HTTP/data checks, say so.
size-variants: trivial → mini-inventory IDs + smoke.
skip-when: never.
