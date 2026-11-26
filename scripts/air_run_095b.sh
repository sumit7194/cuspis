#!/bin/zsh
# EXP-095 W4P10 ALONGSIDE W2P10 (Bridge 2026-11-26 ~18:20: W2P10 peak 1.52 GB <= 2.5, Air free 69% >= 40%). Runs ONLY in ~/GitHub/fleet-air/corner_function_095b/scripts (separate folder: no shared checkpoint path).
# Route W4P10 only. The serial runner (air_run_095.sh) would start a duplicate W4P10 after W2P10: a PID-scoped pause guard holds it. nice 10, caffeinate -i, no-kill watchdog, freepct_guard v3
# LOW 25 / HIGH 35 (PID-scoped, pause-only), a 3 GB pause-only peak hold per step (SIGSTOP only; resume only on the Bridge's word). No caps.
# CUSPIS_081E / CUSPIS_087 unset. STOP on rc != 0 or a pre-existing checkpoint. This script prints NO values. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; unset CUSPIS_081E CUSPIS_087; source tools/pgate.sh
PY=$HOME/GitHub/fleet-air/.venv/bin/python; D=exp081d_results; L=$D/air_run_095b.txt; mkdir -p $D
stop() { echo "=== STOP: $1 $(date '+%F %T')" >> $L; touch $D/air_run_095b.done; exit 1; }
echo "=== air_run_095b start $(date '+%F %T') PID $$ host $(hostname -s)" >> $L
rm -f $D/air_run_095b.done; DONE_FILE=$D/air_run_095b.done LOW=25 HIGH=35 nohup zsh tools/freepct_guard.sh $$ $L 'exp08[0-9]|watchdog\.py' > /dev/null 2>&1 &
step() { local T=$1; shift; echo "=== $T start $(date '+%F %T')" >> $L
  DONE_FILE=$D/air_run_095b.done nohup zsh tools/peak_hold.sh $$ $D/$T.wd.log 3 $L exp081d_route > /dev/null 2>&1 &
  echo "=== $T peak hold armed (PID $!, 3 GB, pause-only)" >> $L
  pgate_run $D/$T.wd.log "nice -n 10 $PY tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore $*"
  local rc=$?; echo "=== $T rc $rc $(date '+%F %T')" >> $L; [ $rc -ne 0 ] && stop "$T rc $rc"; return 0; }
for c in sigma_W4_P10_box10; do ls $D/${c}_c2_cp12_sc3.0_dd0_ckpt.json > /dev/null 2>&1 && stop "checkpoint $c exists before a fresh route"; done
step air_route_W4P10 exp081d_route.py 4 10 10
echo "=== EXP-095 W4P10 route done on the Air $(date '+%F %T')" >> $L; touch $D/air_run_095b.done
