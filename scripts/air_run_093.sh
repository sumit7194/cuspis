#!/bin/zsh
# EXP-093 (P-1) on the MacBook Air (amendment 1, e8a1c06). Runs ONLY inside ~/GitHub/fleet-air/corner_function/scripts.
# Step 1: IDENTITY route W2P6 (fresh; no checkpoint present). Step 2: route W2P8, ONLY after the office creates exp081d_results/identity_pass.go
# (identity graded on the office Mac). nice 10, caffeinate -i, no-kill watchdog, freepct_guard v3 LOW 25 / HIGH 35 (PID-scoped, pause-only), no caps.
# CUSPIS_081E / CUSPIS_087 unset (k <= 2 convention, as EXP-089). STOP on rc != 0 or a pre-existing checkpoint. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; unset CUSPIS_081E CUSPIS_087; source tools/pgate.sh
PY=$HOME/GitHub/fleet-air/.venv/bin/python; D=exp081d_results; L=$D/air_run_093.txt; mkdir -p $D
stop() { echo "=== STOP: $1 $(date '+%F %T')" >> $L; touch $D/air_run_093.done; exit 1; }
echo "=== air_run_093 start $(date '+%F %T') PID $$ host $(hostname -s)" >> $L
rm -f $D/air_run_093.done; DONE_FILE=$D/air_run_093.done LOW=25 HIGH=35 nohup zsh tools/freepct_guard.sh $$ $L 'exp08[0-9]|watchdog\.py' > /dev/null 2>&1 &
step() { local T=$1; shift; echo "=== $T start $(date '+%F %T')" >> $L
  pgate_run $D/$T.wd.log "nice -n 10 $PY tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore $*"
  local rc=$?; echo "=== $T rc $rc $(date '+%F %T')" >> $L; [ $rc -ne 0 ] && stop "$T rc $rc"; return 0; }
for c in sigma_W2_P6_box6 sigma_W2_P8_box8; do ls $D/${c}_c2_cp12_sc3.0_dd0_ckpt.json > /dev/null 2>&1 && stop "checkpoint $c exists before a fresh route"; done
step air_id_route_W2P6 exp081d_route.py 2 6 6
echo "=== identity route done; waiting for $D/identity_pass.go (office grades the identity) $(date '+%F %T')" >> $L
until [ -e $D/identity_pass.go ] || [ -e $D/identity_fail.stop ]; do sleep 60; done
[ -e $D/identity_fail.stop ] && stop "office: identity not passed"
step air_route_W2P8 exp081d_route.py 2 8 8
echo "=== EXP-093 W2P8 route done on the Air $(date '+%F %T')" >> $L; touch $D/air_run_093.done
