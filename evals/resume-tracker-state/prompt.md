---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Deliver ticket ENG-412 end to end with the delivery-loop process. You are at phase 0. Facts already gathered (do not try to run commands):

- Tracker: ENG-412 "Invoice page must say what blocks the invoice", status **Backlog**, assigned to me. Blocked by ENG-410 "error battery" (In Progress). Acceptance: every situation reproduced in the test environment with captures.
- `git branch -a --list '*412*'` in the app repo: eng-412-r2 … eng-412-r13 and fix/eng-412-r13-guard, local and remote.
- PRs: 14 PRs from those branches, all MERGED into main between 12 and 14 Oct. No open PR.
- Test environment serves main (latest SHA includes all 14 merges).
- No task file exists for ENG-412.

Decide the entry phase and the first concrete actions. Answer in at most 12 lines.
