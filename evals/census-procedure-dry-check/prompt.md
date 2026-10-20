---
max_turns: 10
allowed_tools: [Read, Glob, Grep, Skill]
---

Run the delivery-loop census for this repo. Facts already gathered (do not try to run commands):

- The project wiki says: "Deploy to the client's dev environment with `git push client origin/main:dev`; production with `git push client origin/main:main`."
- `git remote -v` lists `origin` and `client`.
- `git merge-base --is-ancestor client/dev origin/main` → exit 1. `git rev-list --count origin/main..client/dev` → 38. Its last merge commits are titled "Merge origin/main into dev: cut 16-oct", "Merge origin/main into dev: cut 20-oct".
- `git merge-base --is-ancestor client/main origin/main` → exit 1 (3 commits of its own).

Write the `## deploy` section you would put in the repo profile (profile grammar: `- key: value` fields, `Rules:` then `- [id] text`, `Source:` line). Output only that section plus at most 3 lines of explanation.
