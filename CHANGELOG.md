# Changelog

## 0.2.0
- deliver phase 0: work state from git, PRs and deploys, never from tracker status alone; entry phase = first phase whose done-when is unmet; ask live sessions already on the ticket.
- census: dry-check procedure facts (target branch exists, push fast-forwards) before writing them; a doc is not verification.
- deliver phase 0: repos derived from the ticket, one workspace per repo for multi-repo tasks; workspace ready to run; task file excluded via `info/exclude`, never `.gitignore`.
- census: task-scoped by default (only what the task needs and upper levels leave open); allowlist and hooks only in full scope.
- profiles: local repo level `<git common dir>/delivery/profile.md` (never committed, shared by worktrees), chosen with `vcs.repo-profile: local`.
- defaults: transversal rule `state-at-source`; field `vcs.repo-profile: committed`.
- evals: `resume-tracker-state`, `census-procedure-dry-check` (from real failures of the first trial).

## 0.1.0
- First release: deliver (phases 0–9), census, spec, qa-design, qa-execution; layered profiles; merge and agnostic scripts.
