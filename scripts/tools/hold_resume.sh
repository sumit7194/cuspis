#!/bin/zsh
# Bridge standing answer (2026-11-25) for a 10 GB HOLD-PEAK on the W12 route: RESUME if system free >= 40% (sustained RESUME_S = 120 s),
# else stay parked and keep checking. Resumes ONLY the PIDs logged on the HOLD-PEAK line, each re-verified (alive, argv matches RX).
# Logs the system free % at the hold and at the resume. One-shot (exits after a resume, or when DONE_FILE exists). Never kills. [model: Opus 5.5]
LOG=$1; RX=${2:-exp081d_route}; DT=${DT:-30}; RESUME_S=${RESUME_S:-120}; HIGH=${HIGH:-40}
freepct() { if [ -n "$FAKE_FREE_FILE" ]; then idx=$((idx+1)); F=$(sed -n "${idx}p" $FAKE_FREE_FILE); else F=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}'); fi; }
idx=0; until grep -q "HOLD-PEAK" $LOG 2>/dev/null; do [ -n "$DONE_FILE" ] && [ -e "$DONE_FILE" ] && exit 0; sleep $DT; done
PIDS=(${=$(grep "HOLD-PEAK" $LOG | tail -1 | sed -E 's/.*SIGSTOP PIDs \[([0-9 ]*)\].*/\1/')}); freepct
echo "=== HOLD-RESUME watcher: hold seen; system free at hold ${F}%; PIDs [${PIDS}]; rule: resume if free >= ${HIGH}% for ${RESUME_S} s (Bridge) $(date '+%F %T')" >> $LOG
since=0
while true; do freepct; [ -z "$F" ] && exit 0; now=$(date +%s)
  if (( F >= HIGH )); then (( since == 0 )) && since=$now
    if (( now - since >= RESUME_S )); then ok=""
      for p in $PIDS; do c=$(ps -o command= -p $p 2>/dev/null); [[ -n "$c" && "$c" =~ $RX ]] && kill -CONT $p && ok="$ok $p"; done
      echo "=== RESUME-HOLD $(date '+%F %T'): system free ${F}% >= ${HIGH}% for ${RESUME_S} s -> SIGCONT [${ok# }] (peak hold NOT re-armed; guard v3 remains)" >> $LOG; exit 0; fi
  else since=0; fi; sleep $DT; done
