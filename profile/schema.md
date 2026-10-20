# Profile schema

file: `.delivery/profile.md` per level; user level `~/.claude/delivery/profile.md`; L0 = plugin `profile/defaults.md`.
merge: `python "<plugin root>/scripts/merge_profiles.py" --cwd <workspace>` → merged profile, each item tagged `← Ln`. Never merge by hand.
exit: 0 ok · 1 malformed/unreadable (stderr `file:line`) · 3 nothing beyond L0 · 4 git repo without repo-level profile → 3/4 run `census`.

## Grammar
- keywords in English, content in any language. UTF-8 (BOM tolerated), LF or CRLF.
- `## <section>` → lowercased. Capabilities below + extra sections (`transversal`, `census`). Reserved: `conflicts`, `skipped`.
- field `- key: value` → key kebab-case; split on first `": "`; one line; non-empty; duplicate key in a file = error.
- locked field `- key: value [invariant]` (any case) → lower levels cannot change it.
- list = one key per item: `- dev: <url> · branch <b>`. Never multi-line.
- absent capability: `- kind: none` in that section.
- `Rules:` line → following `- ` bullets are rules: `- [id] text` | `- [invariant id] text`. id kebab-case, unique per section per file. Bullet without id = error.
- `Source: <where> · checked <YYYY-MM-DD>` → provenance; nearest level wins.
- ignored: text outside `- ` bullets, other bullet markers, fenced code blocks.

## Merge
| item | rule |
|---|---|
| field | nearest level wins; locked → kept, change reported in `## Conflicts` |
| rule | same id in section → nearest wins |
| invariant rule | id reserved across all sections: same id anywhere below → kept, reported; identical restatement in same section → silent |
| new id / key / section | added |
| Source | nearest wins |
| semantic contradiction, different id | not detected → `deliver` phase 0 review |

## Levels
| level | location | holds |
|---|---|---|
| L0 defaults | plugin `profile/defaults.md` | authority, invariants, methodology defaults |
| user | `~/.claude/delivery/profile.md` | `machine`, connected tools, personal identity |
| org | dir grouping the org's repos | `tracker`, `vcs`/`ci` conventions, `reviewers`, `channels` |
| project | dir grouping a client/product's repos | project exceptions |
| repo | `<repo>/.delivery/profile.md`, committed | `environments`, `deploy`, concrete `ci` |

- `~/.delivery/profile.md` = invalid → use user level.
- above the repo's git toplevel, dirs that are git roots are skipped and listed under `## Skipped`.

## Capabilities
| section | fields | examples |
|---|---|---|
| tracker | kind, read-rule, branch-naming, state-start, state-review, state-done | issue tracker, client document, none <!-- agnostic-ok --> |
| vcs | host, integration-branch, production-branch, protection, required-approvals, isolation (worktree\|branch), commit-task-file (yes\|no) | GitHub, GitLab, Azure DevOps <!-- agnostic-ok --> |
| ci | kind, provider, on-draft, on-ready, on-merge, required-checks | hosted CI, none |
| environments | `<name>: <url> · branch <b>` per env; `production-env: <name> [invariant]` | dev, staging, prod |
| deploy | kind, via (git-integration\|pipeline\|manual), served-sha-check | platform git integration, pipeline |
| reviewers | `<n>-<name>: <what> · weight approves\|blocking\|advisory`, ordered by n | human, approving bot, adversarial reviewer on another model, subagent |
| live-verification | kind, ui, api, data | browser automation, HTTP client, test-DB queries |
| channels | kind, approvals, notices | team chat, email, none |
| machine | test-concurrency, local-forbidden, os | `2`, `builds, servers, containers` |
| authority | `class-<class>: <policy>`; `<action>: <class>` | `merge-production: test-env` |
| census | stale-after-days | `30` |

## Authority
- classes: `local` · `own` · `test-env` · `production` · `third-party` · `irreversible`.
- policies: `ask-never` · `ask` · `show-text-first`.
- canonical actions + default classes: `defaults.md` §authority. New action keys allowed.

## Example
```markdown
## deploy
- via: git-integration
Rules:
- [no-cli-deploy] Deploy only through the git integration.
Source: deploy config · checked 2026-10-20
```
