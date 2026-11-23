#!/bin/zsh
# EXP-085c (registered f3fa752) tier order, side job beside part 8, after the 085w2 runner exits: TORUS -> SECTOR -> GEOM (k <= 2, 6 geometries).
# STOP on any failed control (rc != 0) or measured peak >= 0.5 GB. k = 2.5 geometries and READ run after part 8. nice 12, no-kill. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results
while ps -p ${RUNNER_E85W2:-31312} >/dev/null; do sleep 20; done; echo "=== 085w2 runner ended $(date '+%F %T')"
peak() { grep -h "# exit" $1 | tail -1 | sed -E 's/.*= ([0-9.]+) GB.*/\1/'; }
one() { T=$1; shift; echo "=== $T start $(date '+%H:%M:%S')"
  pgate_run $D/$T.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --soft-cap-gb 0.5 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore exp085c_run.py $*"
  rc=$?; pk=$(peak $D/$T.wd.log); echo "=== $T rc $rc peak ${pk:-?} GB $(date '+%F %T')"
  [ $rc -ne 0 ] && { echo "=== STOP: $T rc $rc (control failed or crash)"; exit 1; }
  [ -n "$pk" ] && (( pk >= 0.5 )) && { echo "=== STOP: $T peak $pk GB >= 0.5 GB (beside-part-8 rule)"; exit 2; }; return 0; }
one e85c_TORUS TORUS
one e85c_SECTOR SECTOR
for G in "2 4" "4 4" "3 6" "6 6" "4 8" "8 8"; do set -- ${=G}; one e85c_G_W$1P$2 GEOM $1 $2; done
echo "=== EXP-085c k <= 2 done $(date '+%F %T') (k = 2.5 + READ after part 8)"
