#!/bin/zsh
# Queue part 6: EXP-084c cost-scaling points (production path): W4P4 n = 2 (W-scaling) and W3P6 n = 2 (P/Ny-scaling), one at a time,
# nice 12, no-kill. Waits for queue part 5 (EXP-085 a4 [+ BCDE]). The k-range is decided from these measurements BEFORE the 084c reading runs. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; unset CUSPIS_081E
job() { local name=$1 soft=$2; shift 2; echo "=== $name start $(date '+%H:%M:%S')"
  pgate_run $D/$name.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --soft-cap-gb $soft --log $D/$name.wd.log --stdout $D/$name.out -- $PY -u -W ignore $*"; local rc=$?
  echo "=== $name end $(date '+%H:%M:%S') rc $rc"; tail -1 $D/$name.wd.log; return $rc; }
while ps -p ${RUNNER_Q5:-35091} >/dev/null; do sleep 30; done; echo "=== queue part 5 ended $(date '+%F %T')"
job e84c_W4P4 0.5 exp084c_run.py 4 4 2; echo "=== 084c cost point W4P4 rc $?"
job e84c_W3P6 0.5 exp084c_run.py 3 6 2; echo "=== 084c cost point W3P6 rc $?"
echo "=== HOLD (084c k-range decided from the measured scaling) $(date '+%F %T')"
