#!/bin/zsh
# EXP-095 (83566e3) GEOM pieces on the Mac mini: exp085c_run.py GEOM 2 10, then GEOM 4 10. nice 15, pgate, no-kill watchdog, no caps.
# SEALED-READ: this script logs rc lines and the COUNT of PASS/FAIL verdict words only; no values. STOP on rc != 0 or a pre-existing G file. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; unset CUSPIS_081E CUSPIS_087; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; L=$D/run_095_geom.txt
echo "=== run_095_geom start $(date '+%F %T') PID $$" >> $L
for W in 2 4; do [ -e $D/exp085c/G_W${W}P10.json ] && { echo "=== STOP: G_W${W}P10.json exists before a fresh GEOM" >> $L; exit 1; }; done
for W in 2 4; do T=e95_G_W${W}P10; echo "=== $T start $(date '+%F %T')" >> $L
  pgate_run $D/$T.wd.log "nice -n 15 $PY tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore exp085c_run.py GEOM $W 10"
  rc=$?; echo "=== $T rc $rc; verdict words: PASS $(grep -c PASS $D/$T.out) FAIL $(grep -c FAIL $D/$T.out); $(tail -1 $D/$T.wd.log | grep -o 'PEAK.*') $(date '+%F %T')" >> $L
  [ $rc -ne 0 ] && { echo "=== STOP: $T rc $rc" >> $L; exit 1; }; done
echo "=== run_095_geom done $(date '+%F %T')" >> $L; touch $D/run_095_geom.done
