# Phase 4 — implement

in: plan (or mini-inventory).
out: commits: failing test → code → passing test; test names and commit messages cite IDs.
done-when: tests of the touched zone executed and green (output captured).

behaviours:
- respect `machine` limits (concurrency, local-forbidden).
- static checks first when they answer the question (diff, grep, read, single test).
- before each edit: which ID does this serve? none → deferred list.
- old test failing because it encodes the defect → amend with reason.
- parallel subagents only on disjoint files; one writer per workspace; subagents commit, never push.
- `vcs` rules: explicit add paths, branch check before commit, orchestrator backup-pushes.
- each plan step closes with a commit (WIP if incomplete) + a log line with its SHA; never leave a finished step uncommitted.

capabilities: vcs, machine.
absent: no test framework → add the minimal one the stack uses, or escalate if that is a design choice.
size-variants: none.
skip-when: never.
