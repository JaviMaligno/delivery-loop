## environments
- dev: https://dev.acme-corp.test · branch staging
Rules:
- [invariant no-prod-testing] Never test or write against production.
- [no-prod-testing-2] Smoke tests may read production.

## deploy
- via: git-integration
Source: deploy config · checked 2026-10-20
