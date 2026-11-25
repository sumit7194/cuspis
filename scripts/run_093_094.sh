#!/bin/zsh
# EXP-093 (P-1) route W2P8 and EXP-094 (P-2) honest n = 2 at W2P6, W4P6 (registered f874dac). Bridge order: AFTER the W12 chain
# (run_k3 -> run_087w12), one for one on the same core; sequential; nice 12; no-kill watchdog; pgate; free >= 50% at each launch.
# Starts only when run_087w12.done exists (whatever its outcome: that job's result does not gate these). CUSPIS_081E / CUSPIS_087 unset
# (k <= 2 convention, as EXP-089). STOP on rc != 0. Stale-file guard for the fresh W2P8 checkpoint. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; unset CUSPIS_081E CUSPIS_087; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; L=$D/run_093_094.txt; K=${K3DIR:-$D}
echo "=== run_093_094 armed $(date '+%F %T'); waiting for $K/run_087w12.done" >> $L
until [ -e $K/run_087w12.done ]; do sleep 60; done; echo "=== W12P12 t0 job done -> P-1 next $(date '+%F %T')" >> $L
gate() { local f; while true; do f=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}')
  (( f >= 50 )) && { echo "=== GATE $1 $(date '+%F %T'): free ${f}% -> LAUNCH" >> $L; return; }; echo "=== GATE $1: WAIT free ${f}%" >> $L; sleep 300; done; }
step() { local T=$1; shift; gate $T; echo "=== $T start $(date '+%F %T')" >> $L
  pgate_run $D/$T.wd.log "nice -n 12 $PY tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore $*"
  local rc=$?; echo "=== $T rc $rc $(date '+%F %T')" >> $L; [ $rc -ne 0 ] && { echo "=== STOP: $T rc $rc" >> $L; touch $D/run_093_094.done; exit 1; }; return 0; }
CK=$D/sigma_W2_P8_box8_c2_cp12_sc3.0_dd0_ckpt.json; [ -e $CK ] && { echo "=== STOP: $CK exists before the fresh route (stale-file guard)" >> $L; touch $D/run_093_094.done; exit 1; }
T0=$(date +%s); step e93_route_W2P8 exp081d_route.py 2 8 8
[ -e $CK ] && [ $(stat -f %m $CK) -ge $T0 ] && grep -q '"n1c"' $CK || { echo "=== STOP: W2P8 checkpoint missing, stale or without n1c" >> $L; touch $D/run_093_094.done; exit 1; }
echo "=== stale-file guard PASS: $CK" >> $L
step e94_n2_W2P6 exp084c_run.py 2 6 2
step e94_n2_W4P6 exp084c_run.py 4 6 2
echo "=== P-1 route and P-2 runs done $(date '+%F %T') (grading scripts run separately)" >> $L; touch $D/run_093_094.done
