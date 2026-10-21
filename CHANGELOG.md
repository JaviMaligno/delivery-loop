# Changelog

## 0.3.1
First feature-size run (a ticket sized feature, end to end to the test env).
- deliver: phase log has one line per phase of the size path, skipped ones with their reason; phases whose `out` names a plugin skill invoke it. The run logged 0 → 4 with spec, gaps and plan folded into the task file, and never invoked `spec`, `qa-design` or `qa-execution`.
- qa-design: `trigger` per ID and a Rare paths section. The changed path fires on ~4% of responses; 20 live calls were spent before finding it never fired.
- deliver phase 7: evidence never in a session temp dir (the run wrote it to the job dir, deleted with the session).

## 0.3.0
Frictions from two live runs (a ticket end to end on a client project, and a release session).
- deliver: task file `owner` + since; log lines timed with `date -u`, written per step; `phase <n> loaded` line; re-merge on entering phases 6 and 7 (a rule changed mid-task and the run kept the stale one).
- deliver phase 0: resume checks the task file owner and last write; session listings miss live sessions.
- deliver phase 4: each step closes with a commit (WIP if incomplete) + log line; a dead session lost uncommitted steps.
- deliver phase 5: diff is the literal `git diff`; a hand-built diff without hunk headers gave false "no tests" findings.
- deliver phase 6: served check by content (literal of the change, new route ≠404), never "a new file appeared" (two false positives); fallback check when the primary needs missing access; test env down → declared fallback or escalation; owned actions joined, not duplicated.
- deliver phase 7: fix loop — one fix branch per pass, close on a clean pass (a run spent 4 CI cycles fixing defects one by one); evidence dir from the profile; non-reversible test data recorded with its previous value.
- deliver phases 8–9: `tracker.done-on-handoff`; squash-merged branches force-deleted only after the host says merged.
- defaults: authority rules `action-owner` and `waits` (deadline + default; a run stopped waiting for a peer that never answered); fields `tracker.done-on-handoff: no`, `live-verification.evidence-dir`.
- schema: `environments.test-env`, `fallback-test-env`, `live-verification.evidence-dir`, `· owner` on authority actions.

## 0.2.3
- census: new Start section — run the merge before detecting or asking; anything the merge shows at any level is settled and never asked again; only files the merge lists are profiles. A first-use run with an org profile present skipped the merge, asked which env is production (already an org invariant) and read a set-aside backup file as a profile.
- deliver phase 5: size never removes reviewers; a trivial run replaced the profile's blocking reviewer with reading its own diff.

## 0.2.2
- defaults: transversal rule `decision-change` — acting against a recorded decision (D0.x, plan, answer) needs a new written decision with its source; a live run planned "stop at review state" and then closed the ticket from a memory rule without saying so.
- deliver phase 8: a promotion that is not ours or is batched closes as an explicit hand-off (reason, owner, prepared material) instead of being skipped silently.
- deliver phase 9: a final tracker state different from the planned one only under `decision-change`, stated in the report.

## 0.2.1
- deliver: description triggers on a ticket id with build/fix intent in any language and says to invoke before touching code; a session given "implementa <ticket>" skipped the skill and redid work already on a local branch.
- deliver phase 0: ticket-id branch match is case-insensitive and includes local-only branches with unpushed commits.

## 0.2.0
- deliver phase 0: work state from git, PRs and deploys, never from tracker status alone; entry phase = first phase whose done-when is unmet; ask live sessions already on the ticket.
- census: dry-check procedure facts (target branch exists, push fast-forwards) before writing them; a doc is not verification.
- deliver phase 0: repos derived from the ticket, one workspace per repo for multi-repo tasks; workspace ready to run; task file excluded via `info/exclude`, never `.gitignore`.
- census: task-scoped by default (only what the task needs and upper levels leave open); allowlist and hooks only in full scope.
- profiles: local repo level `<git common dir>/delivery/profile.md` (never committed, shared by worktrees), chosen with `vcs.repo-profile: local`.
- defaults: transversal rule `state-at-source`; field `vcs.repo-profile: committed`.
- deliver phase 0: no new branch when no code change is expected; size measures work left.
- census: exact rule form stated.
- evals: `resume-tracker-state` (3/3 with plugin), `census-procedure-dry-check` (not discriminative yet: facts are given in the prompt; needs a scaffolded repo).

## 0.1.0
- First release: deliver (phases 0–9), census, spec, qa-design, qa-execution; layered profiles; merge and agnostic scripts.
