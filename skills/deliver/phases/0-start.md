# Phase 0 — start

in: task (ticket ref | document | request) + merged profile.
out: delivery dir + task file · workspace when code will change · profile valid (merge exit 0, `## Missing` empty) · size+reason · D0.x · tracker state for the entry phase.
done-when: every capability the task needs is resolved in the profile, probed by the preflight, and working, substituted or listed as a named escalation.

behaviours:
- order: work state → delivery dir + task file → workspace (only if code will change) → census (first use, recheck, `## Missing`) in the workspace or repo → re-merge `--cwd <workspace>` → preflight → rest.
- work state from sources, never from tracker state alone (a ticket "not started" may have merged PRs): branches local+remote carrying the ticket id in any form the branch naming produces (local-only ones included), PRs (any state), workspaces, deploys, task file, blocking tickets.
- the reported behaviour itself, not only the ticket id: locate it in the current code of the integration branch (or reproduce it in the test env). Gone → find the change that removed it (log/blame of the lines) and say so; "already resolved by another change" is a valid entry: phase 7 against what is deployed. An id search alone misses fixes that never cited the ticket.
- entry phase = first phase whose done-when is not met by that evidence; write entry phase + evidence in the task file; earlier phases not redone.
- other live sessions/agents already on the ticket or its area → ask them before starting; never two writers on one branch.
- existing task file → read `owner` and the last log time. Owner alive = answers, or wrote recently; a session listing is not proof either way. Owner silent past the wait deadline → take over: `task_log.py <task.md> --owner <session>` (rewrites `owner`, logs the change), then log the takeover with the evidence (uncommitted files, last commit, last log line).
- repos: cwd is not a repo or the ticket names none → derive from the ticket (paths, components, linked PRs, labels the profile maps to repos) + candidate repos under cwd/project dir; unclear → ask once. Several repos → one workspace per repo, same branch name, PRs linked to each other.
- no code change expected (entry phase ≥ 7 on merged work, or a repo that is not ours) → no workspace and no branch; verify against the deployed SHA; delivery dir holds task file and evidence.
- workspace per `vcs.isolation` from fresh base; branch name per `tracker.branch-naming` when a ticket exists; reuse an existing workspace/branch for this task.
- workspace ready to run: untracked env files copied, dependencies installed or linked per profile rules; nothing of the delivery dir inside it.
- semantic contradictions between rules with different ids → nearer level wins unless it weakens an invariant → note in task file + report.
- size: trivial (one surface, no design choice, ≤ 3 files) · feature · large (multi-PR, redesign, > 10 source points) → write reason. Size measures the work left from the entry phase, not the work already done.
- trivial → mini-inventory in task file: IDs from the request, one line each.
- preflight: rule `authority/[preflight]` — every capability the task will use (tracker, VCS host, CI, reviewers, deploy/env reads, browser, test tools) probed with a real call; one round for what fails. Result in the task file.
- pre-decisions: rule `authority/[pre-decisions]`.
- tracker state (class `own`) by entry phase: ≤ 5 → `state-start`; 6–7 (merged, being verified) → `state-review`; ≥ 8 → leave it. Never move a ticket back to an earlier state.

capabilities: vcs, tracker, machine.
absent: tracker none → no ticket steps, say so · no git repo → escalate (isolation needs one).
size-variants: none.
skip-when: never.
