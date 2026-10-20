# Scope checklist

before any change not traceable to an ID, in order:
1. serves an in-scope ID? → do it, cite ID.
2. refactor required to land an ID safely? → separate minimal commit `refactor: … (enables SPEC-n)`.
3. bug the user would be surprised is broken? → stop, tell the user; separate PR / bundle / defer is their call.
4. else → deferred file, no change.

user says "also do Y" → do it + inventory row `out-of-spec-addition`.

```markdown
# Deferred — <feature>
## <slug>
noticed-while: SPEC-n · idea: <what> · value: <why> · where: <paths, approach> · not-now: <reason>
```
