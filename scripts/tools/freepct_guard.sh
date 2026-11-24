#!/bin/zsh
# Free-memory pause guard (Bridge 2026-11-24; 081e W12 window). Every DT s read the system-wide free percentage; if it stays below LOW (30)
# for HOLD_S (60 s), SIGSTOP every process matching PATTERN and log "PAUSE-FREE"; resume (SIGCONT, "RESUME-FREE") once it stays >= HIGH (40)
# for RESUME_S (120 s). Never kills. Exits when DONE_FILE exists (resuming first if paused). Test hook: FAKE_FREE_FILE (one integer per
# line, one per poll; the guard exits at its end). v2: no subshell for the reading (v1's counter inside $(...) never advanced). [model: Opus 5.5]
PATTERN=$1; LOG=$2; LOW=${LOW:-30}; HIGH=${HIGH:-40}; HOLD_S=${HOLD_S:-60}; RESUME_S=${RESUME_S:-120}; DT=${DT:-30}
paused=0; lowsince=0; highsince=0; idx=0; F=""
read_free() {
  if [ -n "$FAKE_FREE_FILE" ]; then idx=$((idx + 1)); F=$(sed -n "${idx}p" $FAKE_FREE_FILE)
  else F=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}'); fi; }
while true; do
  [ -n "$DONE_FILE" ] && [ -e "$DONE_FILE" ] && { [ $paused = 1 ] && pkill -CONT -f "$PATTERN"; exit 0; }
  read_free; if [ -z "$F" ]; then [ -n "$FAKE_FREE_FILE" ] && { [ $paused = 1 ] && pkill -CONT -f "$PATTERN"; exit 0; }; sleep $DT; continue; fi
  now=$(date +%s)
  if [ $paused = 0 ]; then
    if (( F < LOW )); then (( lowsince == 0 )) && lowsince=$now
      if (( now - lowsince >= HOLD_S )); then pkill -STOP -f "$PATTERN"; paused=1; highsince=0
        echo "=== PAUSE-FREE $(date '+%F %T'): free ${F}% < ${LOW}% for >= ${HOLD_S} s -> SIGSTOP '$PATTERN' (tell the Bridge)" >> $LOG; fi
    else lowsince=0; fi
  else
    if (( F >= HIGH )); then (( highsince == 0 )) && highsince=$now
      if (( now - highsince >= RESUME_S )); then pkill -CONT -f "$PATTERN"; paused=0; lowsince=0
        echo "=== RESUME-FREE $(date '+%F %T'): free ${F}% >= ${HIGH}% for >= ${RESUME_S} s -> SIGCONT" >> $LOG; fi
    else highsince=0; fi
  fi
  sleep $DT
done
