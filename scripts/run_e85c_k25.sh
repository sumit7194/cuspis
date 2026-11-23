#!/bin/zsh
# EXP-085c k = 2.5 geometries (W5P10, W10P10) + READ, AFTER the part-8 runner exits (its 084c READ included); measured peak > 0.5 GB expected,
# so it runs alone (no part-8 job beside it). STOP on any failed control. nice 12, no-kill. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results
while ps -p ${RUNNER_Q8:-91526} >/dev/null; do sleep 60; done; echo "=== part-8 runner ended $(date '+%F %T')"
one() { T=$1; shift; echo "=== $T start $(date '+%H:%M:%S')"
  pgate_run $D/$T.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --soft-cap-gb 4.0 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore exp085c_run.py $*"
  rc=$?; echo "=== $T rc $rc $(date '+%F %T')"; [ $rc -ne 0 ] && { echo "=== STOP: $T rc $rc"; exit 1; }; return 0; }
one e85c_G_W5P10 GEOM 5 10
one e85c_G_W10P10 GEOM 10 10
one e85c_READ READ
echo "=== EXP-085c done $(date '+%F %T')"
