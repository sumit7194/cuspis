#!/bin/zsh
# Queue part 3: EXP-085 rerun under amendment 3 (post-firing, Bridge-accepted: q = 0 included; sweep to n = 256, 1% rule on 192/256).
# Waits for queue part 2 (11606) to reach its HOLD and exit; runs ALONE, no-kill watchdog. Routes remain on HOLD (Bridge go after 085 is read). [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; unset CUSPIS_081E
while ps -p ${RUNNER_Q2:-11606} >/dev/null; do sleep 30; done; echo "=== queue part 2 ended $(date '+%F %T')"
echo "=== exp085 start $(date '+%H:%M:%S')"
pgate_run $D/exp085.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --soft-cap-gb 3.0 --log $D/exp085.wd.log --stdout $D/exp085.out -- $PY -u -W ignore exp085_run.py all"
echo "=== EXP-085 rc $? $(date '+%F %T')"; echo "=== HOLD before routes (Bridge go after 085 is read)"
