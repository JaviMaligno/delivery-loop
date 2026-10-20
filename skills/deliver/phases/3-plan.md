# Phase 3 — plan

in: inventory + gap log + real code read (paths the change touches, callers, sibling paths) + task file.
out: plan: small steps, each with IDs covered + its test · `Out of scope` section (always) · D0.x embedded.
done-when: reviewed by an agent (another model family if available); every non-blocked ID has ≥1 step.

behaviours:
- inspect real code/commands before writing steps; no placeholders; each step self-contained (usable verbatim as an agent prompt).
- TDD in the plan: failing test → implementation → passing test → commit, separate steps.
- nothing more, nothing less: extras → deferred list.
- plan is not a gate for the user to read; decisions close in conversation.

capabilities: reviewers (plan audit).
absent: no other-model reviewer → fresh subagent audits.
size-variants: large → one plan per PR; human checkpoint between PRs; baseline tag on base before touching code.
skip-when: trivial.
