# Org level (fictitious acme-corp) — copy to <dir grouping acme-corp repos>/.delivery/profile.md

## tracker
- kind: Jira
- branch-naming: <TICKET-ID>-<short-slug>
- state-start: Doing
- state-review: Code Review
- state-done: Shipped
Source: acme-corp wiki "Ticket flow" · checked 2026-08-11

## vcs
- host: GitLab
- integration-branch: develop
- production-branch: release
- protection: release requires MR + 2 approvals
- required-approvals: 2

## ci
- provider: GitLab CI
- on-draft: unit tests
- on-ready: unit + integration + e2e
- on-merge: deploy only

## reviewers
- 1-human: code owner of the touched path · weight approves
- 2-second-opinion: subagent with the ticket and the diff · weight advisory
- 3-security: security reviewer skill · weight blocking
Rules:
- [security-on-auth] Run 3-security whenever auth, payments or personal data are touched.

## channels
- approvals: email to the release manager
- notices: none
