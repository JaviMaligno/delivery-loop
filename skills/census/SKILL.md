---
name: census
description: Use to create or refresh delivery profiles — first use of delivery-loop in a repo, "set up the delivery profile", merge script exits 3 (only defaults) or 4 (repo without repo-level profile), a profile datum is stale or contradicts what the repo shows, or `deliver` phase 0 asks for it. Detects tools, environments, CI, deploy path, test runners and reviewers available; asks only what cannot be detected; writes each datum at its level (user, org, project, repo).
---

# Census

out: `.delivery/profile.md` at the right levels (grammar `<plugin root>/profile/schema.md`) + merge exit 0.
merge: `python "<this skill dir>/../../scripts/merge_profiles.py" --cwd <workspace>`; interpreter `python` → `py -3` → `python3`.
where: run inside the task workspace (deliver phase 0 creates it first) → repo profile is written and committed on the task branch.

## Scope
- task-scoped (default, called from `deliver`): only capabilities this task needs that the merged profile leaves unresolved; exit 4 with upper levels covering the task → write a minimal repo profile (or none) and continue, not a full census.
- full: first use of the user/org level, or on request → all steps below.
- repo level location: `vcs.repo-profile: committed` (default) → `<repo>/.delivery/profile.md` on the task branch; `local` → `<git common dir>/delivery/profile.md` (never committed, shared by worktrees).

## First use (exit 3/4, or a capability the task needs is missing)
1. detect, no questions:
   | capability | look at |
   |---|---|
   | vcs | git remote + host; default branch; branch protection + required approvals via host API/CLI; worktree support |
   | ci | CI config files; per event (draft / ready / push / merge) which jobs run; required checks |
   | tests | test frameworks + runner config; command for one file / one zone; known concurrency limits |
   | environments, deploy | deploy config files; platform CLIs on PATH (read-only status); branch → env mapping; env URLs in config/README |
   | tracker | MCP tools in session; ticket id pattern in branch names / commit messages; tracker CLI |
   | reviewers | review tools/MCPs in session; review skills; review bots in recent PRs; code-owner files |
   | live-verification | browser automation skills/MCPs; HTTP clients; test-DB access path |
   | channels | chat/email MCPs or CLIs in session |
   | machine | OS; CPU count; existing user-level limits |
2. map each finding → capability field; pick best available implementation (e.g. adversarial reviewer on another model if present, else built-in review + subagent). Nothing found → `- kind: none`.
   - procedure facts (deploy/promotion commands, branch flows) → dry-check before writing: remote exists, target branch exists, push would fast-forward (`git merge-base --is-ancestor <target> <source>`). Fails → write the procedure that works (e.g. merge source into target, push the merge) + the evidence in `Source`. Copied from a doc ≠ verified.
3. ask only what detection cannot settle. Always settled before writing: `environments.production-env` (written `[invariant]`), env safe for e2e. Typical others: approval path for production. One round; one question per datum; 2–4 options, recommended first.
4. place each datum at its level:
   | datum | level |
   |---|---|
   | tools connected in session, machine limits, personal identity | user |
   | tracker, reviewers, channels, team CI conventions, org invariants | org |
   | project/client exceptions | project |
   | environments, deploy, concrete CI jobs, test commands | repo (committed) |
   - datum already present at an upper level with same value → do not repeat.
   - org/project dir unclear → ask once; recommended = nearest common parent of those repos.
5. show new/changed lines per file → write → merge → exit 0, `## Conflicts` and `## Skipped` reviewed. Rule form is exact: `- [id] text` or `- [invariant id] text` (one bracket, space-separated).
6. task files: `.delivery/tasks/` excluded via `<git common dir>/info/exclude` unless `vcs.commit-task-file: yes`. `repo-profile: committed` → commit the repo profile on the task branch (explicit path); `local` → nothing to commit.
7. (full scope only) permissions: propose a harness allowlist with detected commands of classes `local`/`own`/`test-env` (git, tests, tracker CLI, read-only platform status). Show it; merge by hand into existing settings; never overwrite.
8. (full scope only, optional) invariants expressible as a command pattern (CLI deploy, push to production branch) → propose a pre-tool hook that blocks them. Describe; write only if accepted.

## Recheck (every `deliver` phase 0)
- cheap: remote, default branch, protection, deploy config, required checks still match profile; procedure facts the task will use pass their dry-check.
- mismatch → update that datum at its level; one line to the user.
- `Source` older than `census.stale-after-days` → re-verify before relying on it.
- unverifiable now → keep; escalation in task file if the task depends on it.

## Rules
- every written datum: `Source: <where> · checked <date>`.
- never secrets, tokens or credentials in a profile; reference where they live.
- never classify an action that touches production as `ask-never`.
- org/project profiles from a shared private repo: copy, don't edit locally; propose changes upstream.
