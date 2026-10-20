# Phase 5 — review

in: full branch diff (real, not summarised; split by whole files if large) + spec (ticket / plan / PR body).
out: verdict per reviewer in `reviewers` order; each finding: fixed | disputed with proof | deferred with ticket.
done-when: no blocking finding open; re-review done after blocking fixes.

behaviours:
- give adversarial reviewers the goal (ticket, plan) so they can measure drift.
- verify each finding before acting; a fix must not reintroduce the pattern it corrects.
- never send lockfiles, generated files or secrets.
- automated pass ≠ approval unless the host counts it.

capabilities: reviewers.
absent: reviewers none → built-in code review + one fresh subagent with the spec.
size-variants: large → also review the combined diff of each PR batch before it merges.
skip-when: never.
