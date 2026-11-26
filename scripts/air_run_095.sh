#!/bin/zsh
# EXP-095 on the MacBook Air (registration 83566e3, SEALED-READ). Runs ONLY inside ~/GitHub/fleet-air/corner_function/scripts.
# Route W2P10, then route W4P10 (serial: Cuspis Air budget 1 process). nice 10, caffeinate -i, no-kill watchdog, freepct_guard v3
# LOW 25 / HIGH 35 (PID-scoped, pause-only), a 3 GB pause-only peak hold per step (SIGSTOP only; resume only on the Bridge's word). No caps.
# CUSPIS_081E / CUSPIS_087 unset. STOP on rc != 0 or a pre-existing checkpoint. This script prints NO values. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; unset CUSPIS_081E CUSPIS_087; source tools/pgate.sh
PY=$HOME/GitHub/fleet-air/.venv/bin/python; D=exp081d_results; L=$D/air_run_095.txt; mkdir -p $D
stop() { echo "=== STOP: $1 $(date '+%F %T')" >> $L; touch $D/air_run_095.done; exit 1; }
echo "=== air_run_095 start $(date '+%F %T') PID $$ host $(hostname -s)" >> $L
rm -f $D/air_run_095.done; DONE_FILE=$D/air_run_095.done LOW=25 HIGH=35 nohup zsh tools/freepct_guard.sh $$ $L 'exp08[0-9]|watchdog\.py' > /dev/null 2>&1 &
step() { local T=$1; shift; echo "=== $T start $(date '+%F %T')" >> $L
  DONE_FILE=$D/air_run_095.done nohup zsh tools/peak_hold.sh $$ $D/$T.wd.log 3 $L exp081d_route > /dev/null 2>&1 &
  echo "=== $T peak hold armed (PID $!, 3 GB, pause-only)" >> $L
  pgate_run $D/$T.wd.log "nice -n 10 $PY tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore $*"
  local rc=$?; echo "=== $T rc $rc $(date '+%F %T')" >> $L; [ $rc -ne 0 ] && stop "$T rc $rc"; return 0; }
for c in sigma_W2_P10_box10 sigma_W4_P10_box10; do ls $D/${c}_c2_cp12_sc3.0_dd0_ckpt.json > /dev/null 2>&1 && stop "checkpoint $c exists before a fresh route"; done
step air_route_W2P10 exp081d_route.py 2 10 10
echo "=== EXP-095 W2P10 route done on the Air $(date '+%F %T')" >> $L
step air_route_W4P10 exp081d_route.py 4 10 10
echo "=== EXP-095 W4P10 route done on the Air $(date '+%F %T')" >> $L; touch $D/air_run_095.done
