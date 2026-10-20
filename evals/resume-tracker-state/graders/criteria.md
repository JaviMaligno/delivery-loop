---
type: llm
weight: 1
---

Pass only if the response does all of these:
1. Treats the work as already implemented (merged PRs), not as a fresh start, despite the tracker saying Backlog. Proposing a new implementation branch, a new implementation plan, or re-implementing fails.
2. Puts the main work at live verification / close (phase 7 and/or 9), or explicitly says closing waits on the blocking ticket ENG-410.
3. Mentions recording the entry phase and its evidence (branches/PRs) in a task file or equivalent record.
4. Building the list of IDs/situations to verify (an inventory for verification) is allowed and is NOT a failure; only redoing implementation phases (plan, code) is.
