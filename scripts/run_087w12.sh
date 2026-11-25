#!/bin/zsh
# EXP-087 recompute at W12P12 (Bridge 2026-11-25 ~23:10): t0 flag OFF (KA against the 081e route's stored -486.137451254695) then ON.
# ORDER (registered chain not reordered): starts only after run_k3 completes (route W12, then C1 W12), replacing C1's core one for one;
# sequential, single core, no parallel run. If run_k3 STOPs instead of completing, this runner does NOT start: it logs and exits (Bridge decides).
# Memory: 5-6.5 GB expected on a 16 GB box. Gate: free >= 50% (the launch level of run_k3 / run_087c), plus pgate pressure-normal >= 300 s;
# otherwise it WAITS (never runs under the level). Free-memory guard v3 (PID-scoped, pause-only) on this runner. No-kill watchdog.
# CUSPIS_081E=1 (the route that stored the KA value ran with it); CUSPIS_087 unset (exp087_t0.py sets the flag in-process, OFF then ON).
# [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 CUSPIS_081E=1; unset CUSPIS_087; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; L=$D/run_087w12.txt; T=e87_t0_W12P12; STORED=-486.137451254695; K=${K3DIR:-$D}   # K3DIR: test hook only (where run_k3.done/.txt live)
echo "=== run_087w12 armed $(date '+%F %T'); waiting for run_k3 ($K/run_k3.done)" >> $L
until [ -e $K/run_k3.done ]; do sleep 60; done
grep -q "=== k = 3 window complete" $K/run_k3.txt || { echo "=== NOT STARTED: run_k3 ended without 'k = 3 window complete' (a STOP?) -> ask the Bridge $(date '+%F %T')" >> $L; exit 1; }
echo "=== run_k3 complete -> W12P12 t0 next $(date '+%F %T')" >> $L
while true; do f=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}')
  (( f >= 50 )) && { echo "=== GATE $T $(date '+%F %T'): free ${f}% (>= 50) -> LAUNCH (pgate next)" >> $L; break; }
  echo "=== GATE $T $(date '+%F %T'): WAIT free ${f}%" >> $L; sleep 300; done
rm -f $D/run_087w12.done; DONE_FILE=$D/run_087w12.done nohup zsh tools/freepct_guard.sh $$ $L 'exp087_t0|watchdog\.py' > /dev/null 2>&1 &
echo "=== $T start $(date '+%F %T')" >> $L
pgate_run $D/$T.wd.log "nice -n 12 $PY tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore exp087_t0.py 12 12 $STORED"
rc=$?; echo "=== $T rc $rc $(date '+%F %T')" >> $L; touch $D/run_087w12.done
grep -q "KA OFF vs stored.*PASS" $D/$T.out && echo "=== KA OFF PASS (string in $T.out)" >> $L || echo "=== KA OFF NOT PASS -> the ON value is not usable; tell the Bridge" >> $L
