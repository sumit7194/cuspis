#!/bin/zsh
# EXP-096 amendment 6 (Bridge ruling 2026-11-28): one-chip KA-complete + localisation on the Mac mini. [model: Opus 5.5]
# ORDER: starts only after W6P12 lands (run_w6p12.done; touched only after its stale-file guard PASS). If W6P12 stops instead, this
# runner does NOT start: it logs and exits (Bridge decides). Then SEQUENTIAL, one core (replaces W6P12's core one for one):
#   1. known-answer control exp096_onoff.py 8 8 (flag unset): KA-complete-1chip must CLOSE and the plant must FIRE; else STOP, tell the Bridge.
#   2. exp096_onoff.py 12 12 (CUSPIS_081E=1, as run_087w12.sh): the target.
# Memory: W12P12 install ~3.4-3.8 GB (Air peak 3.78). Gate: free >= 50% + pgate pressure-normal >= 300 s; otherwise WAIT. Free-memory guard
# (PID-scoped, pause-only) on this runner; no-kill watchdog. No hard caps.
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; unset CUSPIS_087 CUSPIS_081E; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; L=$D/run_096a6.txt; W6=${W6DIR:-$D}   # W6DIR: test hook only
stop() { echo "=== STOP $(date '+%F %T'): $1 -> tell the Bridge" >> $L; touch $D/run_096a6.done; exit 1; }
echo "=== run_096a6 armed $(date '+%F %T'); waiting for $W6/run_w6p12.done" >> $L
until [ -e $W6/run_w6p12.done ]; do grep -q "^=== STOP" $W6/run_w6p12.txt 2>/dev/null && { echo "=== NOT STARTED: run_w6p12 STOPPED $(date '+%F %T') -> ask the Bridge" >> $L; exit 1; }; sleep 60; done
gate() { while true; do f=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}')
  (( f >= 50 )) && { echo "=== GATE $1 $(date '+%F %T'): free ${f}% (>= 50) -> LAUNCH (pgate next)" >> $L; break; }
  echo "=== GATE $1 $(date '+%F %T'): WAIT free ${f}%" >> $L; sleep 300; done; }
rm -f $D/run_096a6.done; DONE_FILE=$D/run_096a6.done nohup zsh tools/freepct_guard.sh $$ $L 'exp096_onoff|watchdog\.py' > /dev/null 2>&1 &
run() { local T=$1; shift; gate $T; echo "=== $T start $(date '+%F %T') args: $*" >> $L
  pgate_run $D/$T.wd.log "nice -n 12 $PY tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore exp096_onoff.py $*"
  local rc=$?; echo "=== $T rc $rc $(date '+%F %T')" >> $L; return $rc; }
run e96a6_W8P8 8 8 || stop "W8P8 control rc != 0"
grep -q "KA-complete-1chip.*CLOSES" $D/e96a6_W8P8.out && grep -q "PLANT.*FIRES (PASS)" $D/e96a6_W8P8.out || stop "W8P8 known-answer control FAILED (KA-complete-1chip or plant)"
echo "=== W8P8 control PASS (KA closes, plant fires) -> W12P12 next" >> $L
export CUSPIS_081E=1
run e96a6_W12P12 12 12 || stop "W12P12 rc != 0"
echo "=== run_096a6 complete $(date '+%F %T')" >> $L; touch $D/run_096a6.done
