#!/usr/bin/env bash
# Keep GitHub (main) and the GitHub Pages replay (gh-pages) in step with the local codebase and the live run.
#   scripts/sync_github.sh          # one sync
#   scripts/sync_github.sh --loop   # every SYNC_INTERVAL seconds (default 600)
# Never commits secrets: .env, scripts/ssh_config, data/* (except data/snapshot), runs/ and scratch are git-ignored,
# and a scan refuses to push if anything key-shaped is staged.
set -uo pipefail
export PATH=/opt/anaconda3/bin:$PATH
cd "$(dirname "$0")/.."
ROOT=$PWD
PAGES=${PAGES_DIR:-$ROOT/../ltd-pages}
INTERVAL=${SYNC_INTERVAL:-600}
LOCK=$ROOT/data/.sync.lock
mkdir -p data/logs

sync_once() {
  if ! mkdir "$LOCK" 2>/dev/null; then echo "$(date '+%H:%M:%S') previous sync still running, skipping"; return 0; fi
  trap 'rmdir "$LOCK" 2>/dev/null' RETURN
  echo "== $(date '+%Y-%m-%d %H:%M:%S') sync"
  # 1. fresh snapshot of the live run (the server runs on the GPU box)
  if ssh -F scripts/ssh_config -o ConnectTimeout=15 ltd 'cd ~/ltd && python3 -B -m phoenixastar.snapshot' >/dev/null 2>&1; then
    rsync -az -e "ssh -F scripts/ssh_config" gpubox:ltd/web/public/data/ web/public/data/ || true
    rsync -az -e "ssh -F scripts/ssh_config" gpubox:ltd/data/snapshot/ data/snapshot/ 2>/dev/null || true
    echo "snapshot pulled"
  else
    echo "box unreachable: keeping the previous snapshot"
  fi
  # 2. README / docs result blocks
  python3 docs/update_results.py >/dev/null 2>&1 && echo "docs refreshed" || echo "docs refresh failed (kept old)"
  # 3. static replay build
  (cd web && VITE_STATIC=1 npm run build -- --outDir dist-static >/dev/null 2>&1) && echo "static site built" || { echo "static build failed"; return 1; }
  # 4. commit + push main
  git add -A
  if git diff --cached --quiet; then
    echo "main: nothing new"
  else
    BOXIP=$(awk '/HostName/{print $2; exit}' scripts/ssh_config 2>/dev/null | sed 's/\./\\./g')
    PAT="sk-[A-Za-z0-9_-]{20,}|apk_user_[A-Za-z0-9]{10,}|past_sk_[A-Za-z0-9]{10,}|tml-[A-Za-z0-9]{20,}|BEGIN [O]PENSSH"
    [ -n "$BOXIP" ] && PAT="$PAT|$BOXIP"
    if git diff --cached -U0 | grep -E -q "$PAT"; then
      echo "REFUSING TO COMMIT: something key-shaped is staged"; git reset -q; return 1
    fi
    git commit -q -m "Auto-sync: live snapshot $(date -u '+%Y-%m-%d %H:%M UTC')

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && echo "main: committed"
    git push -q origin main 2>&1 | tail -1 && echo "main: pushed"
  fi
  # 5. publish the replay to gh-pages
  if [ -d "$PAGES/.git" ] || [ -f "$PAGES/.git" ]; then
    rsync -a --delete --exclude .git --exclude .nojekyll web/dist-static/ "$PAGES/"
    touch "$PAGES/.nojekyll"
    (cd "$PAGES" && git add -A && if git diff --cached --quiet; then echo "pages: nothing new"; else
       git commit -q -m "Replay update $(date -u '+%Y-%m-%d %H:%M UTC')

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git push -q origin gh-pages 2>&1 | tail -1; echo "pages: pushed"; fi)
  else
    echo "pages worktree missing at $PAGES"
  fi
}

if [ "${1:-}" = "--loop" ]; then
  while true; do sync_once; sleep "$INTERVAL"; done
else
  sync_once
fi
