# Phase 6 — integrate

in: reviewed branch.
out: PR (draft if `ci.on-draft` is light) · tracker → `state-review` · merge to `vcs.integration-branch` (action `merge-integration`) · deploy to test env (`deploy-test-env`).
done-when: test env serves the exact merged SHA (checked, not inferred).

behaviours:
- capture run/deploy id or SHA before waiting; wait for that one.
- deploy only through `deploy.via`; never out-of-band.
- CI red → confirm the run is for the last pushed commit before diagnosing.
- served check = content evidence: a literal of the change present in what the env serves, a new route answering ≠404, the SHA the platform reports. "A new file appeared" is not evidence. Write which check was used; profile `deploy.served-sha-check` first, its fallback when the primary needs access the session lacks.
- action owned by someone else (`· owner`) → join their batch (one deploy/cut at a time), don't run a parallel one; rule `authority/[waits]`.

capabilities: vcs, ci, deploy, environments, tracker.
absent: test env down or not serving after the deploy → `environments.fallback-test-env` if declared, else escalate with measured state (last SHA served, since when); never switch env on your own · no integration branch → deploy the PR branch to a preview/test env; none exists → escalate (phase 7 needs a deployed non-production env) · deploy none → escalate · ci none → zone tests are the CI evidence.
size-variants: none.
skip-when: never.
