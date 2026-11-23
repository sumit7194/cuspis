#!/bin/zsh
# EXP-085w2 (registered a0a77fd): after the 085w runner exits: 2a, then 2b SC=3 (KA), then 2b SC=6. Side job beside part 8, nice 12, no-kill;
# STOP if a measured peak >= 0.5 GB. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; unset TIER1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results
while ps -p ${RUNNER_E85W:-19516} >/dev/null; do sleep 20; done; echo "=== 085w runner ended $(date '+%F %T')"
peak() { grep -h "# exit" $1 | tail -1 | sed -E 's/.*= ([0-9.]+) GB.*/\1/'; }
one() { T=$1; shift; echo "=== $T start $(date '+%H:%M:%S')"
  pgate_run $D/$T.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --soft-cap-gb 0.5 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore $*"
  rc=$?; pk=$(peak $D/$T.wd.log); echo "=== $T rc $rc peak ${pk:-?} GB $(date '+%F %T')"
  [ -n "$pk" ] && (( pk >= 0.5 )) && { echo "=== STOP: $T peak $pk GB >= 0.5 GB"; exit 2; }; return 0; }
one e85w2a exp085w2a.py
one e85w2b_sc3 exp085w2b.py 3
grep -q "KA: s_cut 3 reproduces stored 084c W4P4 n=2 qsad bitwise *PASS" $D/e85w2b_sc3.out || { echo "=== STOP: 2b KA did not pass; SC=6 not run"; exit 1; }
one e85w2b_sc6 exp085w2b.py 6
echo "=== EXP-085w2 done $(date '+%F %T')"
