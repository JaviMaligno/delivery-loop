# delivery-loop

A Claude Code plugin that takes a task from its source (a ticket, a requirements document or a plain request) all the way to a change that is **merged, deployed to a test environment, verified live, handed over for promotion and closed** — with evidence at every step.

You ask the way you always do:

```
implement ABC-123
```

and Claude runs a fixed delivery loop instead of improvising one.

## Why

Claude can already write the code. What usually goes wrong is everything around it: work that already exists on a forgotten branch gets redone, a review is skipped because the change "looked small", "deployed" is taken to mean "serving", the ticket is closed with no proof, or Claude asks the same five questions about your environment every session.

delivery-loop fixes the process, not the code:

- **One loop, ten phases, each with a done-when.** No phase closes without evidence: command output, test id, capture, query.
- **Your environment is written down once.** Layered profiles (you, your org, a project, a repo) say which tracker, VCS host, CI, environments, deploy path, reviewers and verification tools you use, and what Claude may do without asking. Claude detects what it can and asks only the rest, once.
- **Safety lines that cannot be crossed.** Production is named in the profile as an invariant: Claude never tests or writes there, and actions that touch it are never "act without asking".

## What a run looks like

A real run on a small API-contract ticket, started with only the ticket id:

1. **Start** — read the ticket, found an open PR and a branch from an earlier attempt, and resumed at *review* instead of redoing the work. Sized it as trivial (one surface, no design choice).
2. **Review** — three rounds of code review plus an independent second opinion; every finding fixed and re-reviewed or disputed with proof. Mutation checks confirmed the new test fails when it should.
3. **Integrate** — full test suite green, merged, confirmed the build published the image under the expected name, bumped the test environment through its config repo.
4. **Live** — confirmed the test environment serves the exact commit, then exercised the real endpoint and compared its output with the contract.
5. **Promote / close** — promotion to the next environments belongs to another team there, so the loop prepared the hand-off; it opened one follow-up ticket for the out-of-scope findings, commented the evidence on the ticket and closed it.

Everything it decided and why lives in a task file (`<git common dir>/delivery/tasks/<slug>/task.md`), next to its spec, plan and evidence: outside the working tree, never committed, kept after the worktree is removed.

## Install

```
claude plugin marketplace add JaviMaligno/delivery-loop
claude plugin install delivery-loop@delivery-loop
```

Restart Claude Code. The first time you run it in a repo, the `census` skill detects your setup and asks one short round of questions; answers are saved in the profile at the right level.

If your organisation already keeps a shared org profile, copy it to the directory that holds your repos (`<repos dir>/.delivery/profile.md`) before the first run, and census will only ask what it leaves open.

## Skills

| skill | role |
|---|---|
| `deliver` | the orchestrator: phases 0–9, task size, authority, final report |
| `census` | first use / recheck: detect the environment, ask what is missing, write profiles |
| `spec` | turn the source into an inventory with stable IDs, log gaps, control scope, review doc |
| `qa-design` | per-ID verification plan with named captures |
| `qa-execution` | run that plan against the deployed test environment, collect evidence, hunt bugs, clean up |

`deliver` triggers on its own when you hand Claude a ticket with intent to build or fix (in any language); `/delivery-loop:deliver <ticket>` forces it.

## Phases

| # | phase | done when |
|---|---|---|
| 0 | start | workspace ready, profile valid, work already done found, task sized |
| 1 | spec | every point of the source has an ID or a reason to exclude it |
| 2 | gaps | no open gap blocks the plan |
| 3 | plan | reviewed; every ID has a step |
| 4 | implement | tests for the touched zone green, executed |
| 5 | review | no blocking finding open (task size never removes reviewers) |
| 6 | integrate | the test environment serves the exact commit |
| 7 | live | every ID passes with evidence, plus a regression smoke |
| 8 | promote | merge to the production branch verified — or an explicit hand-off when promotion belongs to someone else |
| 9 | close | tracker and git state match the report |

Trivial tasks skip 1–3; large ones add a baseline inventory and one plan per PR with a human checkpoint between PRs. Work can enter at any phase: phase 0 reads the evidence (branches, PRs, deploys), not the ticket status.

## Profiles

`.delivery/profile.md` per level, merged from far to near by `scripts/merge_profiles.py`:

| level | file | typically holds |
|---|---|---|
| defaults | `profile/defaults.md` (this plugin) | authority classes, invariants, methodology |
| user | `~/.claude/delivery/profile.md` | your machine, access, language, your own autonomy |
| org / project | `.delivery/profile.md` in the directory grouping those repos | tracker, VCS and CI conventions, environments, reviewers, channels |
| repo | `<repo>/.delivery/profile.md` | branches, test commands, environment URLs of that repo |

The nearest level wins; rules merge by id; items marked `[invariant]` cannot be relaxed below. Grammar in `profile/schema.md`; fictitious examples in `examples/`. Real org profiles belong in that org's private repo, not here.

### How much it does on its own

Every action has a class (`local`, `own`, `test-env`, `production`, `third-party`, `irreversible`) and every class a policy (`ask-never`, `ask`, `show-text-first`). Defaults: act freely on your machine, your branches and the test environment; ask before production or irreversible actions; show the exact text before anything other people will read. Tighten it in your user profile while you get used to it, for example:

```markdown
## authority
- class-test-env: ask
```

## Development

```
python -m unittest discover -s tests
python scripts/check_agnostic.py [--denylist private-terms.txt]
claude plugin validate .
```

`check_agnostic.py` fails if the core names a concrete tool; private repos pass their own company and client terms with `--denylist`. Changes are recorded in `CHANGELOG.md`. Design notes: `docs/specs/2026-10-20-delivery-loop-design.md`.

## License

MIT
