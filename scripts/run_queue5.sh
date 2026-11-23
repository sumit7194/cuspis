#!/bin/zsh
# Queue part 5 (v2, adds the 084c KA_ALIAS diagnosis first, alone): EXP-085 amendment 4 (extrapolation + Watson KA + held-out n = 384), ALONE, no-kill; if it passes, EXP-085 phases B-E
# (normalisation controls, Sigma-sigma-dot per geometry, test (i), reading). Waits for queue part 4 (084c KA + dry run). Routes stay on HOLD. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; unset CUSPIS_081E
job() { local name=$1 soft=$2; shift 2; echo "=== $name start $(date '+%H:%M:%S')"
  pgate_run $D/$name.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --soft-cap-gb $soft --log $D/$name.wd.log --stdout $D/$name.out -- $PY -u -W ignore $*"; local rc=$?
  echo "=== $name end $(date '+%H:%M:%S') rc $rc"; tail -1 $D/$name.wd.log; return $rc; }
while ps -p ${RUNNER_Q4:-20651} >/dev/null; do sleep 30; done; echo "=== queue part 4 ended $(date '+%F %T')"
job e84c_ka_alias 2.0 exp084c_run.py KA_ALIAS; echo "=== EXP-084c KA_ALIAS diagnosis rc $?"
if job e85_a4 6.0 exp085_a4.py; then echo "=== EXP-085 amendment 4 PASS"; job e85_BCDE 3.0 exp085_run.py BCDE; echo "=== EXP-085 BCDE rc $?"
else echo "=== EXP-085 amendment 4 FAIL -> 085 stays INCONCLUSIVE"; fi
echo "=== HOLD (routes await the Bridge's go) $(date '+%F %T')"
