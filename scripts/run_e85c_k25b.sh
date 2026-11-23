#!/bin/zsh
# EXP-085c k = 2.5 (W5P10, W10P10) + READ: Bridge one-off option (b) 2026-11-24, beside part 8 only, one geometry at a time, nice 12,
# watchdog inform/pause (never kill). STOP before W10P10 if W5P10 wall > 1800 s (report first). READ only after both GEOM pass. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results
wall() { grep -h "# exit" $1 | tail -1 | sed -E 's/.*wall ([0-9]+) s.*/\1/'; }
peak() { grep -h "# exit" $1 | tail -1 | sed -E 's/.*= ([0-9.]+) GB.*/\1/'; }
one() { T=$1; shift; echo "=== $T start $(date '+%H:%M:%S')"
  pgate_run $D/$T.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --soft-cap-gb 3.15 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore exp085c_run.py $*"
  rc=$?; echo "=== $T rc $rc wall $(wall $D/$T.wd.log) s peak $(peak $D/$T.wd.log) GB (estimate ~1 GB + install, <= 3.15 GB) $(date '+%F %T')"
  [ $rc -ne 0 ] && { echo "=== STOP: $T rc $rc"; exit 1; }; return 0; }
one e85c_G_W5P10 GEOM 5 10
w=$(wall $D/e85c_G_W5P10.wd.log); (( ${w:-0} > 1800 )) && { echo "=== STOP: W5P10 wall $w s > 1800 s -> report to the Bridge before W10P10"; exit 3; }
one e85c_G_W10P10 GEOM 10 10
one e85c_READ READ
echo "=== EXP-085c done $(date '+%F %T')"
