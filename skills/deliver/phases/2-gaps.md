# Phase 2 — gaps

in: inventory.
out: gap log (skill `spec`): only decisions a human must take, each with options + recommendation.
done-when: no open gap blocks the plan; blocked IDs `gap-blocked`, rest proceed.

behaviours:
- obvious decision (a teammate with context would answer without hesitation) → take it, write "Decided: …, because …".
- data/code can answer it → answer it, don't ask.
- business, money, client-system decisions → human, with recommendation.
- never build on an assumption the pending answer could contradict.

capabilities: none.
absent: n/a.
size-variants: none.
skip-when: trivial.
