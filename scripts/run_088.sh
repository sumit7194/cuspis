#!/bin/zsh
# EXP-088 checks (registered c9aa1ea): E, C, D, A in sequence, after the W10P10 t0 job frees its core (fleet <= 9). nice 12, no-kill watchdog.
# Each mode is minutes; A's P = 10 honest saddles peak ~3 GB (084 k = 2.5 measured 3.03 GB). [model: Opus 5.5]
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; unset CUSPIS_081E CUSPIS_087; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; L=$D/run_088.txt
while ps -p ${WAIT_PID:-0} > /dev/null 2>&1; do sleep 60; done; echo "=== core free $(date '+%F %T')" >> $L
for m in E C D A; do echo "=== e88_$m start $(date '+%F %T')" >> $L
  pgate_run $D/e88_$m.wd.log "nice -n 12 $PY tools/watchdog.py --interval 5 --log $D/e88_$m.wd.log --stdout $D/e88_$m.out -- $PY -u -W ignore exp088_checks.py $m"
  rc=$?; echo "=== e88_$m rc $rc $(date '+%F %T')" >> $L
  [ $m = E ] && [ $rc -ne 0 ] && { echo "=== STOP: E found H_2 + sigma_2 non-PD (or E failed) -> C/D/A NOT run; tell the Bridge (Q1's premise) $(date '+%F %T')" >> $L; exit 1; }
done
echo "=== EXP-088 checks done $(date '+%F %T')" >> $L
