# Inventory template

```markdown
# Spec inventory — <feature>
source: <path/URL> · version: <version or "received YYYY-MM-DD"> · updated: <date>

| ID | verbatim | interpretation | surface | location | status |
|----|----------|----------------|---------|----------|--------|
| SPEC-1 | "<exact quote>" | <one sentence> | UI | p.2 §1.a | pending |
| SPEC-2a | "<quote part 1>" | ... | backend | p.2 §2 | pending |
| SPEC-2b | "<quote part 2>" | ... | UI | p.2 §2 | gap-blocked |
```

rules:
- verbatim = exact source text, source language.
- interpretation = one sentence; needs more → split row.
- one atomic requirement per row ("filter by A and by B" → 2a, 2b).
- surface depth: UI → manual steps + capture; backend → test/log pointer; infra → dashboard/healthcheck; docs → diff; process → new process description.
