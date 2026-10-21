# Phase 6 — integrate

in: reviewed branch.
out: PR (draft if `ci.on-draft` is light) · tracker → `state-review` · merge to `vcs.integration-branch` (action `merge-integration`) · deploy to test env (`deploy-test-env`).
done-when: test env serves the exact merged SHA (checked, not inferred); or no test env exists and that is stated, with observation IDs moved after phase 8.

behaviours:
- first: re-merge + diff against the ruling merge (deliver Start 5), logged.
- capture run/deploy id or SHA before waiting; wait for that one.
- deploy only through `deploy.via`; never out-of-band.
- CI red → confirm the run is for the last pushed commit before diagnosing.
- served check = evidence that this change is served (the SHA the platform reports, or content only this change produces); never an inference such as a new artefact. Write which check was used; profile `deploy.served-sha-check` first, its fallback when the primary needs access the session lacks.
- action owned by someone else (`· owner`) → rule `authority/[action-owner]`.

capabilities: vcs, ci, deploy, environments, tracker.
absent: test env down or not serving after the deploy → `environments.fallback-test-env` if declared, else escalate with measured state (last SHA served, since when); never switch env on your own · no integration branch → deploy the PR branch to a preview/test env · no non-production env at all (integration = production) → stimulus IDs need one: escalate; observation IDs are verified after phase 8 · deploy none → escalate · ci none → zone tests are the CI evidence.
size-variants: none.
skip-when: never.
