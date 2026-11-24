#!/bin/zsh
# Free-memory pause guard v3 (Bridge fleet rule 2026-11-24: signal ONLY explicit, verified PIDs; never by pattern).
# Usage: freepct_guard.sh ROOT_PID LOG [ARGV_REGEX]. Every DT s: if system free% stays < LOW (30) for HOLD_S (60 s), SIGSTOP the
# DESCENDANTS of ROOT_PID (pgrep -P recursion from the recorded PID; the guard itself and its own children excluded) whose command line
# matches ARGV_REGEX (verified per PID just before signalling); record exactly those PIDs. Resume (SIGCONT) the SAME recorded PIDs, each
# re-verified (still alive, same command line), once free% stays >= HIGH (40) for RESUME_S (120 s). Never kills. Exits when ROOT_PID is gone
# or DONE_FILE exists (resuming first). Test hook: FAKE_FREE_FILE (one integer per poll; exits at its end). [model: Opus 5.5]
ROOT=$1; LOG=$2; RX=${3:-python}; LOW=${LOW:-30}; HIGH=${HIGH:-40}; HOLD_S=${HOLD_S:-60}; RESUME_S=${RESUME_S:-120}; DT=${DT:-30}
paused=0; lowsince=0; highsince=0; idx=0; F=""; typeset -A SAVED
read_free() { if [ -n "$FAKE_FREE_FILE" ]; then idx=$((idx + 1)); F=$(sed -n "${idx}p" $FAKE_FREE_FILE)
  else F=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}'); fi; }
descendants() { local p; for p in $(pgrep -P $1 2>/dev/null); do [ $p = $$ ] && continue; echo $p; descendants $p; done; }
resume_all() { local p c; for p in ${(k)SAVED}; do c=$(ps -o command= -p $p 2>/dev/null)
  [ -n "$c" ] && [ "$c" = "${SAVED[$p]}" ] && kill -CONT $p; done; SAVED=(); }
while true; do
  if ! kill -0 $ROOT 2>/dev/null || { [ -n "$DONE_FILE" ] && [ -e "$DONE_FILE" ]; }; then [ $paused = 1 ] && resume_all; exit 0; fi
  read_free; if [ -z "$F" ]; then [ -n "$FAKE_FREE_FILE" ] && { [ $paused = 1 ] && resume_all; exit 0; }; sleep $DT; continue; fi
  now=$(date +%s)
  if [ $paused = 0 ]; then
    if (( F < LOW )); then (( lowsince == 0 )) && lowsince=$now
      if (( now - lowsince >= HOLD_S )); then SAVED=(); local_list=""
        for p in $(descendants $ROOT); do c=$(ps -o command= -p $p 2>/dev/null); [[ -n "$c" && "$c" =~ $RX ]] || continue
          kill -STOP $p && SAVED[$p]="$c" && local_list="$local_list $p"; done
        paused=1; highsince=0; echo "=== PAUSE-FREE $(date '+%F %T'): free ${F}% < ${LOW}% for >= ${HOLD_S} s -> SIGSTOP PIDs [${local_list# }] (descendants of $ROOT; tell the Bridge)" >> $LOG; fi
    else lowsince=0; fi
  else
    if (( F >= HIGH )); then (( highsince == 0 )) && highsince=$now
      if (( now - highsince >= RESUME_S )); then echo "=== RESUME-FREE $(date '+%F %T'): free ${F}% >= ${HIGH}% for >= ${RESUME_S} s -> SIGCONT PIDs [${(k)SAVED}]" >> $LOG; resume_all; paused=0; lowsince=0; fi
    else highsince=0; fi
  fi
  sleep $DT
done
