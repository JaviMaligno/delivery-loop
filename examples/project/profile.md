# Project level (one acme-corp product) — copy to <dir grouping that product's repos>/.delivery/profile.md

## reviewers
- 3-security: security reviewer skill · weight advisory
Rules:
- [security-on-auth] Run 3-security on every MR; this product handles health data.
Source: product security review · checked 2026-07-30

## authority
- live-e2e: production
Rules:
- [shared-staging] The staging env is shared with the vendor; ask before running e2e there.
