# Phase 9 — close

in: verified merge, or hand-off from phase 8 per `tracker.done-on-handoff`.
out: tracker → `state-done` with evidence links · evidence linked in PR + ticket · merged branches deleted (remote+local) · workspaces removed · test data cleaned · report.
done-when: tracker state + git state match the report; no ID without evidence; test data cleaned or recorded as not reversible.

behaviours:
- evidence (visual where possible) + regression proof are part of the close, not optional.
- report separates "requested works" (per ID, evidence) from "rest still works" (CI on last commit, neighbour smoke, baseline compare).
- delete a squash-merged branch: local git cannot see it as merged → confirm the PR state is merged at the host, then force-delete local; never force-delete on git's word alone.
- remove workspaces safely: check for links/junctions inside first; never force. Task file or evidence still inside → move them out first, then remove; never leave a workspace behind to keep them.
- final tracker state differs from the one planned in phase 0 → only under rule `transversal/[decision-change]`, and the report says so.
- unbacked branches or leftover WIP → say so.
- durable learnings from escalations → profile at their level.

capabilities: tracker, vcs, channels.
absent: tracker none → evidence linked in PR only, say so.
size-variants: none.
skip-when: never.
