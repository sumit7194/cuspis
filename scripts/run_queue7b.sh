#!/bin/zsh
# Queue part 7b (rerun after the phase-B fix 29c26d3): EXP-085 phases B-E under amendment 5 (two-ended bracket, EXP085_A5=1), ALONE, no-kill (geometry builds ~2-3 GB).
# Starts at once (part 6 done). Routes stay on HOLD until the Bridge's go. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 EXP085_A5=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; unset CUSPIS_081E
echo "=== part 7b start $(date "+%F %T")"
echo "=== e85_BCDE_a5 start $(date '+%H:%M:%S')"
pgate_run $D/e85_BCDE_a5.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --soft-cap-gb 4.0 --log $D/e85_BCDE_a5.wd.log --stdout $D/e85_BCDE_a5.out -- $PY -u -W ignore exp085_run.py BCDE"
echo "=== EXP-085 BCDE (amendment 5) rc $? $(date '+%F %T')"; echo "=== HOLD (routes await the Bridge's go)"
