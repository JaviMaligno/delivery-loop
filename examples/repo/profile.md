# Repo level — commit as <repo>/.delivery/profile.md

## environments
- staging: https://staging.acme-corp.test · branch develop
- live: https://acme-corp.test · branch release
- production-env: live [invariant]

## deploy
- via: pipeline
- served-sha-check: GET /version → sha field
Rules:
- [pipeline-only] Deploy only by merging; never trigger the deploy job by hand.
Source: .gitlab-ci.yml · checked 2026-09-15

## ci
- required-checks: unit, integration
