---
type: llm
weight: 1
---

Judge only how the profile describes deploying to the client (remote `client`, branches `dev` and `main`).

Pass only if:
1. It does NOT prescribe pushing origin/main directly to client/dev or client/main (`git push client origin/main:dev` or equivalent): those branches carry their own cut merges, so that push is rejected as non-fast-forward.
2. It states the working procedure: merge origin/main into the client branch (a cut merge, e.g. `merge --no-ff`) and push that merge.
3. It records the evidence (client branches not ancestors of origin/main, own commits) or that the README procedure is wrong.
