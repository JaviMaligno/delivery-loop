# Gap log template

```markdown
# Gaps — <feature>
inventory: <path> · updated: <date>

## Open
### GAP-1 — SPEC-1: "<word>" underspecified
question: <concrete question, options if possible>
recommendation: <option + reason>
owner: <who answers> · blocks: SPEC-1 · status: pending (asked YYYY-MM-DD)

## Resolved
### GAP-0 — SPEC-4 — resolved YYYY-MM-DD
answer: <answer + where it was given>
applied: <inventory change>
```

add a gap when: two different builds satisfy the text · asset/credential/data/mapping missing · two points conflict · external system undocumented · subjective term without target.
workaround possible → status stays `pending`, row note `assumption: <placeholder until GAP-n>`.
