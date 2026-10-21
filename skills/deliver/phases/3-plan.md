# Phase 3 — plan

in: inventory + gap log + real code read (paths the change touches, callers, sibling paths) + task file.
out: plan in the delivery dir: small steps, each with IDs covered + its test · `Out of scope` section (always) · D0.x embedded.
done-when: reviewed by the profile's reviewers that take a plan (`· on plan|both`), else a fresh subagent (logged: no plan reviewer in the profile); every non-blocked ID has ≥1 step.

behaviours:
- inspect real code/commands before writing steps; no placeholders; each step self-contained (usable verbatim as an agent prompt).
- TDD in the plan: failing test → implementation → passing test → commit, separate steps.
- nothing more, nothing less: extras → deferred list.

capabilities: reviewers (plan audit).
absent: no plan reviewer → fresh subagent audits.
size-variants: large → one plan per PR; human checkpoint between PRs; baseline tag on base before touching code.
skip-when: trivial.
