# Review doc template

```markdown
# Spec review — <feature>
source: <path> · inventory: <link> · gaps: <link> · PR: <link> · date: <date>

## Summary
<delivered · gap-blocked · deferred — 2–3 lines>

## Compliance
| ID | description | surface | action | expected | evidence | status |
|----|-------------|---------|--------|----------|----------|--------|
| SPEC-1 | ... | UI | ... | ... | [capture](../qa-evidence/<date>/screenshots/spec-1-01-x.png) · `<test name>` | resolved |
| SPEC-3 | ... | backend | ... | ... | pending GAP-2 | gap-blocked |

## Detail
### SPEC-1 — <title>
quote: "<verbatim>" · interpretation: <one line>
changed: <paths, links>
tests: <names>
verify (UI): numbered steps a reviewer can reproduce · capture: <path>
verify (backend/infra): test / request / log query / dashboard
caveats: <follow-ups, pending external input with owner + date>

## Regression
CI on <sha>: <link> · neighbour smoke: <flows + result> · baseline compare: <result | none>

## Deferred / out of scope
| item | why | where |
```

visual index `docs/qa-evidence/<date>/visual-qa.md`:
```markdown
| capture | proves | environment | note |
```
depth: UI → capture always + steps; role/state-dependent → contrast captures (both roles, before/after). Backend → 1–2 lines + how to re-run.
