# Changelog

## 0.6.1
- Codex: `.codex-plugin/plugin.json` + `.agents/plugins/marketplace.json` over the same `skills/`; `$deliver <ticket>` invokes it. A test keeps names and versions of both harnesses' manifests in sync. Skills name script paths relative to "the dir of this SKILL.md" instead of a harness placeholder. <!-- agnostic-ok -->
- `task_log.py --owner <session>` creates the task file skeleton with its time from the clock, or takes it over (rewrites `owner`, logs the change). A run wrote the header's time by hand because the script only appended log lines.
- `merge_profiles.py --out` prints only levels, `## Conflicts`, `## Missing`, `## Skipped` and the saved path; the full merge is in the file. Each re-merge printed ~400 lines into the session.

## 0.6.0
From a live run that closed on production behaviour (a fix already deployed; the ticket's closing criterion was days of real traffic without the error).
- verification modes: each QA ID is `stimulus` (exercised in the test env, as before) or `observation` (only real traffic shows it: metric · read-only source in production · window). Default rule `environments/[observe-not-test]`: reading production's own observability from inside it is observation, not testing; never a stimulus, never a write. Phase 7 only knew the test env; the run had to invent the distinction.
- 🔄 means "not measured yet" and always carries its cause and a dated wait (or an escalation); ⚠️ is never used for something not measured; an open 🔄 blocks phase 9 (ticket stays in review) and the resume re-enters phase 7 for those IDs only. A criterion left unmeasured by a platform outage was marked ⚠️ and read as a pass.
- what instructions did not achieve is now mechanical: `merge_profiles.py --out` saves the ruling merge (UTC time + hash per level) in the delivery dir, and phases 6/7 diff their re-merge against that file; `scripts/task_log.py` writes every log line with the time from the clock. Runs typed log times from memory despite the `date -u` instruction (second occurrence) and had no saved merge to diff.

## 0.5.0
Frictions from three live runs on two projects (a ticket already delivered months before, a monitor ticket on a repo owned by another team, a feature end to end with code).
- delivery dir: `vcs.delivery-dir`, default `<git common dir>/delivery/tasks/<slug>/`, holds task file (`task.md`), spec docs, plan, QA plan and evidence. Outside every working tree: nothing to exclude, never pushed, survives workspace removal, exists for tasks with no workspace. Replaces the 0.4.2 location (read on resume, moved). `vcs.commit-task-file` removed. Runs wrote spec and plan in a versioned `docs/` of a repo pushed to a client, kept evidence inside a worktree, and had no place for the task file when there was no code to change.
- deliver phase 0: checks the reported behaviour in the current code (or reproduces it), not only the ticket id; "already resolved by another change" is an entry (phase 7). A run sized a feature already fixed by a PR that never cited the ticket.
- deliver phase 0: tracker state follows the entry phase (≤ 5 start, 6–7 review, ≥ 8 untouched); never moves back. A run moved a ticket in production since months to "in progress".
- deliver phase 0: no workspace and no branch when no code will change (verification on merged work, or a repo that is not ours).
- merge: required fields `environments.production-env` and `environments.test-env` (or `- kind: none`) → `## Missing` in the output; phase 0 runs census for them. A run reached live verification with no test env in the profile and exit 0.
- merge: a line continuing a bullet → exit 1 with `file:line`. A rule wrapped by an editor was cut silently.
- deliver phases 6 and 7: re-merge is the first step, logged (a run skipped it).
- deliver phase 7: each fixture gets a `pending cleanup` line in the task file when created; leaving with pending lines → written in the ticket first. Marker in another field when the id comes from the data.
- qa-design: each pre-condition says whether the data exists in the target env (record + how checked), which fixture creates it, or ⚠️ unreachable — checked before the run.
- defaults: authority rule `release-owner` — production promotion owned by someone else (release process, client) → a hand-off stated as a fact, no question or recommendation about the release; report section "handed off".
- census: recheck re-verifies layout facts (repo location, `levels` links, paths) every time; a moved repo kept a dated link that was already false.

## 0.4.2
- deliver: task file and evidence live in the main checkout (`.delivery/tasks/<slug>[/]`), never inside the task worktree; phase 9 moves them out before removing a workspace. The feature run kept its evidence inside the worktree and then skipped the cleanup to avoid deleting it.

## 0.4.1
- deliver phase 7, qa-execution: the visual check is mandatory, the tool is not. No browser tool in the profile → any one the session has; none → escalate to get one connected; IDs with something to see never close on HTTP/data checks alone. `live-verification.ui` is a personal choice (user level) and may list fallbacks; `test-identity` says how it logs in.

## 0.4.0
- profiles: any level (repo, local repo or an intermediate dir) can link a project level outside its ancestors with `## levels` → `- project: <dir>`; merged right before the linking profile; one hop; a dir without a profile → exit 1. For repos or apps that do not live under their project's directory. census links instead of copying; app-specific rules go in the app's own level.
- defaults: transversal rule `source-conflict` — profile vs instructions or memory → newer dated source wins, the stale one is fixed at its source. A live run tested with an account a stale memory still pointed to, against a newer rule.
- schema: `live-verification.test-identity`; deliver phase 7 acts only as that identity.
- merge_profiles: the `repo level` line shows the repo files actually used (it showed the committed path when only the local profile existed).
- evals: `census-real-repo` with a scaffolded repo (local bare remotes; client branches carrying cut merges, README documenting a push git rejects). Run with `--scaffold`. On Windows shell tools are refused (no sandbox backend), so the agent reads `.git` directly: with plugin 2/3, without 0/3. Shell grants work where the sandbox exists.

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
