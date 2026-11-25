#!/bin/zsh
# Disk guard for RUNNING jobs whose watchdog.py predates the no-kill rule (old copies SIGTERM at free disk < 5 GB). Sumit 2026-11-25: NO kill.
# Every DT s: free disk < PAUSE_AT (5.5 GB, ABOVE the old 5 GB kill) -> SIGSTOP each listed watchdog PID (verified: argv contains tools/watchdog.py)
# AND its descendants (so the old watchdog cannot fire its kill); resume both above RESUME_AT (6 GB). < 2 GB: CRITICAL alert. NEVER kills.
# Usage: disk_guard.sh LOG WD_PID [WD_PID ...]. Test hook: FAKE_DISK_FILE. Exits when every listed watchdog is gone. [model: Opus 5.5]
LOG=$1; shift; WDS=($@); PAUSE_AT=${PAUSE_AT:-5.5}; RESUME_AT=${RESUME_AT:-6.0}; DT=${DT:-30}; paused=0; crit=0
desc() { local p; for p in $(pgrep -P $1 2>/dev/null); do echo $p; desc $p; done; }
disk() { if [ -n "$FAKE_DISK_FILE" ]; then tail -1 $FAKE_DISK_FILE; else df -g . | awk 'NR==2{print $4}'; fi; }
while true; do
  alive=(); for w in $WDS; do c=$(ps -o command= -p $w 2>/dev/null); [[ "$c" == *tools/watchdog.py* ]] && alive+=($w); done
  (( ${#alive} == 0 )) && exit 0
  d=$(disk)
  if (( paused == 0 )) && awk -v d=$d -v t=$PAUSE_AT 'BEGIN{exit !(d < t)}'; then L=""
    for w in $alive; do kill -STOP $w && L="$L $w"; for p in $(desc $w); do kill -STOP $p && L="$L $p"; done; done
    paused=1; echo "=== PAUSE-DISK-GUARD $(date '+%F %T'): free disk ${d} GB < ${PAUSE_AT} -> SIGSTOP [${L# }] (old watchdogs + jobs; tell the Bridge)" >> $LOG
  elif (( paused == 1 )) && awk -v d=$d -v t=$RESUME_AT 'BEGIN{exit !(d > t)}'; then
    for w in $alive; do for p in $(desc $w); do kill -CONT $p; done; kill -CONT $w; done
    paused=0; crit=0; echo "=== RESUME-DISK-GUARD $(date '+%F %T'): free disk ${d} GB > ${RESUME_AT} -> SIGCONT" >> $LOG
  fi
  if (( crit == 0 )) && awk -v d=$d 'BEGIN{exit !(d < 2)}'; then crit=1; echo "=== CRITICAL-DISK-GUARD $(date '+%F %T'): free disk ${d} GB < 2 GB; everything of mine stays paused; tell the Bridge NOW (never killed)" >> $LOG; fi
  sleep $DT
done
