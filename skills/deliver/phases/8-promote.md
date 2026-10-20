# Phase 8 — promote

in: change verified live (phase 7 done).
out: PR ready → full CI on last commit → valid approval → merge to `vcs.production-branch` (action `merge-production`, rule `authority/[production-path]`).
done-when: merge verified against git (fetch + commit/file present on target), not against a command's echo; or promotion explicitly handed off with reason, owner and prepared material.

behaviours:
- before merge: all checks success on head SHA, mergeable, correct base, head = local HEAD.
- promotion between long-lived branches keeps shared history (merge commit, no squash) unless profile says otherwise.
- never relax protection to get through.
- promotion not done in this task (authority says it is not ours, batched release, out of agreed scope) → phase still closes: task file + report state why, what is pending, who owns it and what was prepared for them (branch/PR, SHA, evidence).
- integration branch = production branch (or none) → phase 6 only deployed a preview; this phase does the merge, after phase 7.

capabilities: vcs, ci, reviewers, channels.
absent: ci none → zone tests + phase 7 evidence are the gate; say so.
size-variants: large → one promotion per PR in plan order.
skip-when: never.
