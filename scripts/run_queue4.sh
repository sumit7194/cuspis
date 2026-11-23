#!/bin/zsh
# Queue part 4: EXP-084c KA + planted normalisation, then the registered dry run (k = 1, W2P4b4, n = 2) ALONE, then HOLD
# (the remaining geometries are sized from the measured dry-run cost). Waits for queue part 3 (EXP-085 rerun). No-kill watchdog. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; unset CUSPIS_081E
job() { local name=$1 soft=$2; shift 2; echo "=== $name start $(date '+%H:%M:%S')"
  pgate_run $D/$name.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --soft-cap-gb $soft --log $D/$name.wd.log --stdout $D/$name.out -- $PY -u -W ignore $*"; local rc=$?
  echo "=== $name end $(date '+%H:%M:%S') rc $rc"; tail -1 $D/$name.wd.log; return $rc; }
while ps -p ${RUNNER_Q3:-12889} >/dev/null; do sleep 30; done; echo "=== queue part 3 ended $(date '+%F %T')"
job e84c_KA 2.0 exp084c_run.py KA; echo "=== EXP-084c KA rc $?"
job e84c_dry 3.0 exp084c_run.py 2 4 2; echo "=== EXP-084c dry run rc $?"
echo "=== HOLD (084c remaining geometries sized from the dry run; routes on HOLD) $(date '+%F %T')"
