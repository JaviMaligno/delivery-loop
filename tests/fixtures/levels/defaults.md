# Defaults (fixture)

## environments
- production-env: prod [invariant]
Rules:
- [invariant no-prod-testing] Never test or write against production.

## vcs
- isolation: worktree
Rules:
- [no-stash] Never use stash; commit WIP instead.
