# Defaults (L0)

Every item is overridable by key/id unless `[invariant]`.

## authority
- class-local: ask-never
- class-own: ask-never
- class-test-env: ask-never
- class-production: ask
- class-third-party: show-text-first
- class-irreversible: ask
- read: local
- workspace: local
- commit: local
- zone-tests: local
- push-own-branch: own
- open-draft-pr: own
- run-reviewers: own
- update-own-ticket: own
- merge-integration: test-env
- deploy-test-env: test-env
- set-test-env-vars: test-env
- live-e2e: test-env
- merge-production: production
- set-production-vars: production
- send-message: third-party
- client-visible-comment: third-party
- force-push: irreversible
- delete-unmerged-branch: irreversible
- delete-data: irreversible
Rules:
- [invariant class-policies] Policies: ask-never = act without asking · ask = one question before acting · show-text-first = show exact text, act on approval.
- [delete-exceptions] delete-data needs no question when the plan explicitly includes it, or the data was created by this task for testing and is not needed afterwards.
- [class-moves] Move an action with `<action>: <class>` at a lower level; new action keys allowed. Never move an action that touches production into an ask-never class.
- [production-path] merge-production follows `channels.approvals` / `reviewers` weight approves when the profile defines them; else ask.
- [pre-decisions] Phase 0: one round with what the profile leaves open for this task (real data read/write, human-only checks, actions outside their class) → D0.x in the task file. Unanswered → named escalation, never an assumption.
- [escalation] One question per decision, 2–4 options, recommended first. Keep working on everything independent of the answer.
- [answer-routing] Durable answer → profile at its level. Task-only answer → task file.

## environments
Rules:
- [invariant no-prod-testing] Never test or write against production. Production data is read only from inside its environment.
- [production-env-required] `production-env` must name the production environment (census asks); locked with [invariant] where it is set.

## deploy
Rules:
- [served-sha] Deploy success ≠ serving: confirm the environment serves the expected SHA.
- [wait-by-id] Capture the run/deploy id or SHA before waiting; wait for that one, not "the latest".

## vcs
- isolation: worktree
- commit-task-file: no
- repo-profile: committed
Rules:
- [fresh-base] Isolated workspace from the freshly fetched base branch.
- [no-stash] Never stash; set work aside with a WIP commit.
- [explicit-add] Stage by explicit path; never add-all.
- [env-files] Copy untracked env files into the workspace before running anything that needs them.
- [check-branch] Check the current branch right before each commit.
- [backup-push] Orchestrator pushes the branch as soon as it has commits worth keeping; subagents commit, never push.
- [merged-means-deleted] After a verified merge: delete remote+local branch, remove workspace.

## ci
Rules:
- [last-commit] A CI verdict counts only for the last pushed commit.
- [no-probe-push] Never push just to see what CI says.

## reviewers
Rules:
- [all-available] Run every available reviewer on the full diff before opening the PR.
- [finding-outcome] Each finding: fixed, disputed with proof (file:line, test, output), or deferred with a ticket.
- [re-review] After fixing blocking findings, review again, passing the previous verdict when the reviewer supports it.
- [not-approval] An automated pass ≠ a valid approval unless the host counts it.

## census
- stale-after-days: 30

## transversal
Rules:
- [verify-at-source] Verify in code, environment or original document; never in a summary, plan or memory.
- [read-not-measured] "Read in code" ≠ "measured in the environment"; say which.
- [evidence] No phase closes without evidence: command output, test id, capture, query.
- [obvious-decisions] Take obvious decisions and write them: "Decided: …, because …".
- [old-tests] A test that encodes the defect is amended with the reason; never trim the fix to go green.
- [scope] Nothing more, nothing less than the agreed scope; extras → deferred list.
- [check-blockers] Probe before declaring something missing, blocked or impossible.
- [state-at-source] Work state comes from git, PRs and deploys; a tracker status or a document is a hint, not evidence.
- [precedence] Source > spec > plan > code.
- [decision-change] Acting against a recorded decision (D0.x, plan, escalation answer) needs a new decision written first in the task file: what changes, why, and its source (user answer, profile rule, instructions or memory read mid-task). Never override a recorded decision silently.
- [report] Report: decided+why · open with recommendation · assumed · out of scope · where to look.
