# Phase 6 — integrate

in: reviewed branch.
out: PR (draft if `ci.on-draft` is light) · tracker → `state-review` · merge to `vcs.integration-branch` (action `merge-integration`) · deploy to test env (`deploy-test-env`).
done-when: test env serves the exact merged SHA (checked, not inferred).

behaviours:
- capture run/deploy id or SHA before waiting; wait for that one.
- deploy only through `deploy.via`; never out-of-band.
- CI red → confirm the run is for the last pushed commit before diagnosing.

capabilities: vcs, ci, deploy, environments, tracker.
absent: no integration branch → deploy the PR branch to a preview/test env; none exists → escalate (phase 7 needs a deployed non-production env) · deploy none → escalate · ci none → zone tests are the CI evidence.
size-variants: none.
skip-when: never.
