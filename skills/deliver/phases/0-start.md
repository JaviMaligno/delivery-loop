# Phase 0 — start

in: task (ticket ref | document | request) + merged profile.
out: workspace · profile valid (merge exit 0) · task file · size+reason · D0.x · tracker at `state-start`.
done-when: every capability the task needs is resolved in the profile or listed as named escalation.

behaviours:
- order: workspace → census (first use or recheck) in the workspace → re-merge `--cwd <workspace>` → rest.
- workspace per `vcs.isolation` from fresh base; branch name per `tracker.branch-naming` when a ticket exists; reuse an existing workspace/branch for this task.
- apply `vcs` rules (env files, no stash).
- semantic contradictions between rules with different ids → nearer level wins unless it weakens an invariant → note in task file + report.
- size: trivial (one surface, no design choice, ≤ 3 files) · feature · large (multi-PR, redesign, > 10 source points) → write reason.
- trivial → mini-inventory in task file: IDs from the request, one line each.
- pre-decisions: rule `authority/[pre-decisions]`.
- ticket → `tracker.state-start` (class `own`).

capabilities: vcs, tracker, machine.
absent: tracker none → no ticket steps, say so · no git repo → escalate (isolation needs one).
size-variants: none.
skip-when: never.
