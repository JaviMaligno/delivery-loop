#!/usr/bin/env bash
# Builds a repo whose wiki documents a client push that git would reject:
# client/dev and client/main carry cut merges, so they are not ancestors of origin/main.
set -euo pipefail
echo "scaffold cwd: $(pwd)" >&2
g() { git -c user.name=eval -c user.email=eval@example.test "$@"; }
mkdir -p remotes
git init -q --bare remotes/origin.git
git init -q --bare remotes/client.git
git init -q -b main app
cd app
printf '# app\n\n## Deploy\nDeploy to the client dev environment with `git push client origin/main:dev`; production with `git push client origin/main:main`.\n' > README.md
echo 'v1' > app.txt
g add README.md app.txt && g commit -q -m "init"
git remote add origin ../remotes/origin.git
git remote add client ../remotes/client.git
git push -q origin main
for b in dev main; do
  g checkout -q -b "cut-$b"
  echo "client config $b" > client.cfg
  g add client.cfg && g commit -q -m "client-only config for $b"
  git push -q client "HEAD:$b"
  g checkout -q main
done
echo 'v2' > app.txt && g commit -q -am "feature"
git push -q origin main
for b in dev main; do
  git fetch -q client
  g checkout -q -b "merge-$b" "client/$b"
  g merge -q --no-ff origin/main -m "Merge origin/main into $b: cut 16-oct"
  git push -q client "HEAD:$b"
  g checkout -q main
done
echo 'v3' > app.txt && g commit -q -am "fix" && git push -q origin main
git fetch -q --all
git branch -q -D cut-dev cut-main merge-dev merge-main
