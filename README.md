# delivery-loop

Claude Code plugin: take a task from its source (ticket, requirements document, request) to a change verified live in a non-production environment, promoted and closed — in any environment.

- **Core is tool-agnostic.** Phases declare what goes in, what comes out and the evidence that proves done; Claude picks how with what the session has.
- **Layered profiles** say what the environment is: tracker, VCS host and protection, CI per event, environments and deploy path, reviewers, verification tools, channels, machine limits, authority.
- **Few confirmations.** Detect first, ask once, store the answer at its level; act without asking inside the authority classes the profile allows.

## Install
```
claude plugin marketplace add JaviMaligno/delivery-loop
claude plugin install delivery-loop@delivery-loop
```

## Skills
| skill | role |
|---|---|
| `deliver` | orchestrator: phases 0–9, size, authority, report |
| `census` | first use / recheck: detect environment, ask what's missing, write profiles |
| `spec` | inventory with stable IDs, gaps, scope control, review doc |
| `qa-design` | per-ID verification plan with named captures |
| `qa-execution` | run the plan live, evidence, bug hunt, cleanup |

## Profiles
`.delivery/profile.md` per level, merged far → near by `scripts/merge_profiles.py`:

| level | file |
|---|---|
| L0 defaults | `profile/defaults.md` (this plugin) |
| user | `~/.claude/delivery/profile.md` |
| org / project | `.delivery/profile.md` in the directory grouping those repos |
| repo | `<repo>/.delivery/profile.md` (committed) |

Nearest level wins; rules merge by id; `[invariant]` items cannot be relaxed below. Grammar: `profile/schema.md`. Examples (fictitious org): `examples/`.

Real org profiles belong in that org's private repo, not here.

## Phases
0 start · 1 spec · 2 gaps · 3 plan · 4 implement · 5 review · 6 integrate · 7 live verification · 8 promote · 9 close. Trivial tasks skip 1–3; large ones add baseline inventory and one plan per PR. Close requires evidence per ID (visual where possible) and proof that nothing else broke.

## Development
```
python -m unittest discover -s tests
python scripts/check_agnostic.py [--denylist private-terms.txt]
claude plugin validate .
```
`check_agnostic.py` fails if the core names a concrete tool; private repos pass their own company/client terms with `--denylist`.

Design: `docs/specs/2026-10-20-delivery-loop-design.md`.

## License
MIT
