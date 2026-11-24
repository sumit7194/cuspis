#!/bin/zsh
# Peak hold (Bridge 2026-11-24, 081e W12 route): wait for WDLOG to appear; every DT s read the newest watchdog data line's tree footprint
# (5th field, GB). If it reaches THRESH, SIGSTOP the verified DESCENDANTS of ROOT_PID whose command line matches ARGV_REGEX (PID-scoped,
# fleet rule) and log "HOLD-PEAK". It does NOT resume by itself: resume needs the Bridge's word (kill -CONT the logged PIDs).
# Exits when ROOT_PID is gone, after a hold, or when DONE_FILE exists. Never kills. [model: Opus 5.5]
ROOT=$1; WDLOG=$2; THRESH=$3; LOG=$4; RX=${5:-exp081d_route}; DT=${DT:-30}
descendants() { local p; for p in $(pgrep -P $1 2>/dev/null); do [ $p = $$ ] && continue; echo $p; descendants $p; done; }
while true; do
  kill -0 $ROOT 2>/dev/null || exit 0; [ -n "$DONE_FILE" ] && [ -e "$DONE_FILE" ] && exit 0
  if [ -e "$WDLOG" ]; then
    tot=$(grep -E '^ *[0-9]+\.[0-9]+ ' $WDLOG | tail -1 | awk '{print $5}')
    if [ -n "$tot" ] && awk -v t=$tot -v h=$THRESH 'BEGIN{exit !(t >= h)}'; then list=""
      for p in $(descendants $ROOT); do c=$(ps -o command= -p $p 2>/dev/null); [[ -n "$c" && "$c" =~ $RX ]] || continue; kill -STOP $p && list="$list $p"; done
      echo "=== HOLD-PEAK $(date '+%F %T'): tree footprint ${tot} GB >= ${THRESH} GB -> SIGSTOP PIDs [${list# }] (tell the Bridge; resume only on its word: kill -CONT those PIDs)" >> $LOG; exit 0; fi
  fi
  sleep $DT
done
