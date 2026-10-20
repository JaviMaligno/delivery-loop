# Phase 9 — close

in: verified merge.
out: tracker → `state-done` with evidence links · evidence linked in PR + ticket · merged branches deleted (remote+local) · workspaces removed · test data cleaned · report.
done-when: tracker state + git state match the report; no ID without evidence.

behaviours:
- evidence (visual where possible) + regression proof are part of the close, not optional.
- report separates "requested works" (per ID, evidence) from "rest still works" (CI on last commit, neighbour smoke, baseline compare).
- remove workspaces safely: check for links/junctions inside first; never force.
- unbacked branches or leftover WIP → say so.
- durable learnings from escalations → profile at their level.

capabilities: tracker, vcs, channels.
absent: tracker none → evidence linked in PR only, say so.
size-variants: none.
skip-when: never.
