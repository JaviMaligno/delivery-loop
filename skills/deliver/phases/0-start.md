# Phase 0 — start

in: task (ticket ref | document | request) + merged profile.
out: workspace · profile valid (merge exit 0) · task file · size+reason · D0.x · tracker at `state-start`.
done-when: every capability the task needs is resolved in the profile or listed as named escalation.

behaviours:
- order: work state → workspace → census (first use or recheck) in the workspace → re-merge `--cwd <workspace>` → rest.
- work state from sources, never from tracker state alone (a ticket "not started" may have merged PRs): branches local+remote matching the ticket id case-insensitively (including local-only branches with unpushed commits), PRs (any state), workspaces, deploys, task file, blocking tickets. Entry phase = first phase whose done-when is not met by that evidence; write entry phase + evidence in the task file; earlier phases not redone.
- other live sessions/agents already on the ticket or its area → ask them before starting; never two writers on one branch.
- repos: cwd is not a repo or the ticket names none → derive from the ticket (paths, components, linked PRs) + candidate repos under cwd/project dir; unclear → ask once. Several repos → one workspace per repo, same branch name, PRs linked to each other.
- no code change expected (entry phase ≥ 7 on merged work) → no new branch; verify against the deployed SHA, workspace only for task file and evidence.
- workspace per `vcs.isolation` from fresh base; branch name per `tracker.branch-naming` when a ticket exists; reuse an existing workspace/branch for this task.
- workspace ready to run: untracked env files copied, dependencies installed or linked per profile rules; no delivery files committed unless the profile says so.
- task file: in the workspace at `.delivery/tasks/<slug>.md`; not committed → exclude via `<git common dir>/info/exclude`, never by editing tracked `.gitignore`.
- apply `vcs` rules (env files, no stash).
- semantic contradictions between rules with different ids → nearer level wins unless it weakens an invariant → note in task file + report.
- size: trivial (one surface, no design choice, ≤ 3 files) · feature · large (multi-PR, redesign, > 10 source points) → write reason. Size measures the work left from the entry phase, not the work already done.
- trivial → mini-inventory in task file: IDs from the request, one line each.
- pre-decisions: rule `authority/[pre-decisions]`.
- ticket → `tracker.state-start` (class `own`).

capabilities: vcs, tracker, machine.
absent: tracker none → no ticket steps, say so · no git repo → escalate (isolation needs one).
size-variants: none.
skip-when: never.
