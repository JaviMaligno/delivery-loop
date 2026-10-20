# Merged delivery profile

Levels (far → near):
- L0: defaults.md
- L1: home/.claude/delivery/profile.md
- L2: home/org/.delivery/profile.md
- L3: home/org/proj/.delivery/profile.md
- L4: home/org/proj/repo/.delivery/profile.md

## environments
- production-env: prod [invariant] ← L0
- dev: https://dev.acme-corp.test · branch staging ← L4
Rules:
- [invariant no-prod-testing] Never test or write against production. ← L0
- [client-env] Validate in the client's own test environment. ← L3
- [no-prod-testing-2] Smoke tests may read production. ← L4

## vcs
- isolation: branch ← L2
Rules:
- [no-stash] Stash is fine for quick switches. ← L2

## machine
- test-concurrency: 2 ← L1
Rules:
- [no-local-builds] Never run builds or servers locally. ← L1

## tracker
- kind: issue-tracker ← L2
Rules:
- [read-all] Read description, comments and attachments before planning. ← L2
Source: org handbook · checked 2026-10-01 ← L2

## deploy
- via: git-integration ← L4
Source: deploy config · checked 2026-10-20 ← L4

## Conflicts
- environments/production-env: invariant from L0 kept; L3 tried to change it
