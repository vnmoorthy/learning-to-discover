#!/usr/bin/env bash
# Commit and push real changes every COMMIT_INTERVAL seconds (default 60). Never creates empty commits.
# Shares the lock with scripts/sync_github.sh so two git operations never overlap.
set -uo pipefail
export PATH=/opt/anaconda3/bin:$PATH
cd "$(dirname "$0")/.."
INTERVAL=${COMMIT_INTERVAL:-60}
LOCK=data/.sync.lock
mkdir -p data/logs

summary() {   # "web: Physics.tsx, App.tsx (+3 more); docs: README.md"
  git diff --cached --name-only | awk -F/ '{d=($2==""?"root":$1); f=$NF; if(!(d in n)){order[++k]=d}; n[d]++; if(n[d]<=2) names[d]=(names[d]?names[d]", ":"") f}
    END{for(i=1;i<=k;i++){d=order[i]; s=d": "names[d]; if(n[d]>2) s=s" (+"(n[d]-2)" more)"; out=(out?out"; ":"") s}; print out}'
}

while true; do
  if mkdir "$LOCK" 2>/dev/null; then
    git add -A
    if ! git diff --cached --quiet; then
      BOXIP=$(awk '/HostName/{print $2; exit}' scripts/ssh_config 2>/dev/null | sed 's/\./\\./g')
      PAT="sk-[A-Za-z0-9_-]{20,}|apk_user_[A-Za-z0-9]{10,}|past_sk_[A-Za-z0-9]{10,}|tml-[A-Za-z0-9]{20,}|BEGIN [O]PENSSH"
      [ -n "$BOXIP" ] && PAT="$PAT|$BOXIP"
      if git diff --cached -U0 | grep -E -q "$PAT"; then
        echo "$(date '+%H:%M:%S') REFUSING: key-shaped content staged"; git reset -q
      else
        MSG="$(summary)"
        git commit -q -m "Update ${MSG:0:180}

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git push -q origin main 2>&1 | tail -1
        echo "$(date '+%H:%M:%S') committed: ${MSG:0:160}"
      fi
    fi
    rmdir "$LOCK" 2>/dev/null
  fi
  sleep "$INTERVAL"
done
