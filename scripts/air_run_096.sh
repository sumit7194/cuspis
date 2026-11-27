#!/bin/zsh
# EXP-096 / EXP-097 jobs on the Air (registration notes/EXP-096_097_registration.md, 4624f77; Bridge GO 2026-11-27).
# Runs ONLY in ~/GitHub/fleet-air/corner_function_096/scripts. Usage: air_run_096.sh LABEL FLAG081E ARGS...   (FLAG081E: 1 or 0)
#   W12P12 uses CUSPIS_081E=1 (as run_087w12.sh, which stored the t0 values); W8P8 / W10P10 and EXP-097 leave it unset
#   (the k <= 2.5 convention; the 081e filter changes no pole list at W8P8 / W10P10). CUSPIS_087 always unset.
# nice 10, caffeinate -i, no-kill watchdog, freepct_guard v3 LOW 20 / HIGH 30 (Bridge, Sumit's note: the Air runs only our jobs),
# PID-scoped, pause-only. No caps. Prints NO values. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; unset CUSPIS_087; source tools/pgate.sh
T=$1; F=$2; shift 2; [ "$F" = 1 ] && export CUSPIS_081E=1 || unset CUSPIS_081E
PY=$HOME/GitHub/fleet-air/.venv/bin/python; D=exp081d_results; L=$D/air_run_096.txt; mkdir -p $D
echo "=== $T start $(date '+%F %T') PID $$ host $(hostname -s) CUSPIS_081E=${CUSPIS_081E:-unset} args: $*" >> $L
rm -f $D/$T.done; DONE_FILE=$D/$T.done LOW=20 HIGH=30 nohup zsh tools/freepct_guard.sh $$ $L 'exp09[67]|watchdog\.py' > /dev/null 2>&1 &
echo "=== $T freepct_guard PID $! (LOW 20 / HIGH 30, pause-only)" >> $L
pgate_run $D/$T.wd.log "nice -n 10 caffeinate -i $PY tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore $*"
rc=$?; echo "=== $T rc $rc $(date '+%F %T')" >> $L; touch $D/$T.done; exit $rc
