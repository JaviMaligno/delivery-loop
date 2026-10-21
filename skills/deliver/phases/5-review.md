# Phase 5 — review

in: full branch diff + spec (ticket / plan / PR body). Diff = literal output of `git diff <base>...HEAD` (split by whole files if large); never summarised, reconstructed or hand-edited.
out: verdict per reviewer in `reviewers` order; each finding: fixed | disputed with proof | deferred with ticket.
done-when: no blocking finding open; re-review done after blocking fixes.

behaviours:
- give adversarial reviewers the goal (ticket, plan) so they can measure drift.
- verify each finding before acting; a fix must not reintroduce the pattern it corrects.
- never send lockfiles, generated files or secrets.
- size never removes reviewers: a trivial diff still goes through every reviewer the merged profile lists. Reading your own diff is not a reviewer.

capabilities: reviewers.
absent: reviewers none → built-in code review + one fresh subagent with the spec.
size-variants: large → also review the combined diff of each PR batch before it merges.
skip-when: never.
