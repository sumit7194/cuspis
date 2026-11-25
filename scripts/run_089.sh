#!/bin/zsh
# EXP-089 (ii) wall test at P' = 6 (registered 7ef8dfa): fresh 081d routes W2P6b6, W4P6b6 (~40 min each), 085c GEOM W2P6, W4P6, then the grading.
# Starts when WAIT_PID (the W10P10 t0 job) exits AND the Bridge's go-token exists (the Bridge sequences the fleet <= 9). nice 12, no-kill watchdog; CUSPIS_081E/CUSPIS_087 unset. STOP on rc != 0. [model: Opus 5.5]
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; unset CUSPIS_081E CUSPIS_087; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; L=$D/run_089.txt
while ps -p ${WAIT_PID:-0} > /dev/null 2>&1; do sleep 60; done; echo "=== W10P10 done $(date '+%F %T')" >> $L
# FLEET gate (Bridge 2026-11-25 22:35): the fleet total cannot be counted reliably from here (a CPU-share count read 7 busy while 10 jobs ran:
# under contention niced jobs fall below any threshold). So the Bridge sequences: launch only after the go-token exists, which Cuspis
# creates on the Bridge's explicit go.
TOKEN=$D/run_089.go; echo "=== waiting for the Bridge's go-token ($TOKEN) $(date '+%F %T')" >> $L
until [ -e $TOKEN ]; do sleep 60; done; echo "=== go-token present -> launch $(date '+%F %T')" >> $L
step() { local T=$1; shift; echo "=== $T start $(date '+%F %T')" >> $L
  pgate_run $D/$T.wd.log "nice -n 12 $PY tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore $*"
  local rc=$?; echo "=== $T rc $rc $(date '+%F %T')" >> $L; [ $rc -ne 0 ] && { echo "=== STOP: $T rc $rc" >> $L; exit 1; }; return 0; }
step e89_route_W2P6 exp081d_route.py 2 6 6
step e89_route_W4P6 exp081d_route.py 4 6 6
step e89_G_W2P6 exp085c_run.py GEOM 2 6
step e89_G_W4P6 exp085c_run.py GEOM 4 6
step e89_wall exp089_wall.py
echo "=== EXP-089 (ii) done $(date '+%F %T')" >> $L
