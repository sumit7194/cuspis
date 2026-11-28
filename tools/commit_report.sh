#!/bin/zsh
# commit_report.sh: print the facts of the last commit and its push state, for pasting VERBATIM into reports. [model: Opus 5.5]
# Usage: tools/commit_report.sh [N]   (N = how many recent commits to list; default 1). Read-only except `git fetch`.
cd "$(git rev-parse --show-toplevel)" || exit 1
n=${1:-1}; git fetch -q origin 2>/dev/null; fetched=$?
echo "repo      $(basename $(pwd))   branch $(git rev-parse --abbrev-ref HEAD)"
echo "HEAD      $(git rev-parse HEAD)"
up=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null)
if [ -n "$up" ]; then
  echo "upstream  $up $(git rev-parse $up)   (fetch rc $fetched)"
  read ahead behind <<< "$(git rev-list --left-right --count HEAD...$up)"
  if [ "$ahead" = 0 ] && [ "$behind" = 0 ]; then echo "push      PUSHED (HEAD == $up)"; else echo "push      NOT IN SYNC: ahead $ahead, behind $behind"; fi
else echo "push      NO UPSTREAM"; fi
git log -n $n --format='commit    %h %ad %s' --date=format:'%F %T'
echo "worktree  $(git status --porcelain --untracked-files=no | wc -l | tr -d ' ') tracked files modified"
