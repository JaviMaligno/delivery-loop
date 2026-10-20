---
type: llm
weight: 1
---

Pass only if:
1. The section does NOT tell to push origin/main directly to client/dev or client/main (that push would be rejected as non-fast-forward).
2. It states the working procedure: merge origin/main into the client branch (a cut merge, e.g. `merge --no-ff`) and push that merge; dev before main.
3. It records the evidence (not ancestor / own commits) or that the wiki was wrong, in `Source` or a rule.
4. It follows the grammar: rules have ids in brackets; there is a `Source:` line.
