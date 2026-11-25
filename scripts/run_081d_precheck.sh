#!/bin/zsh
# DEPRECATED 2026-11-25 (Sumit's standing rule: NO job-ending caps): this runner passes kill-mode watchdog flags
# (--stop-on-pressure-warn / --pressure-stop-level). Convert to the no-kill watchdog before any reuse. Body kept for the record.
echo "DEPRECATED: $0 uses kill-mode flags; refusing to run (see header)" >&2; exit 2
# EXP-081d pre-checks (existing geometries only). One job at a time, nice 12, watchdog 1.5 GB, pgate. [model: Opus 5.5]
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; WD="$PY tools/watchdog.py --min-disk-gb 5 --stop-on-pressure-warn --cap-gb 1.5"; D=exp081d_results; mkdir -p $D
job() { local name=$1; shift; echo "=== $name start $(date '+%H:%M:%S')"; pgate_run $D/$name.wd.log "nice -n 12 $WD --log $D/$name.wd.log --stdout $D/$name.out -- $PY -u -W ignore $*" || echo "=== $name FAILED"; tail -1 $D/$name.wd.log; tail -4 $D/$name.out; }
for W in 2 4; do job pre_W${W}P4 exp081d_route.py $W 4 4; job pre_W${W}P4_full exp081d_route.py $W 4 4 --full --production-only; job pre_W${W}P4_rd1 exp081d_route.py $W 4 4 --rank-drop 1 --production-only; done
job pre_W8P8_ka exp081d_route.py 8 8 8 --production-only --nodes 0:1 --tag-suffix _ka
job pre_check exp081d_precheck.py
echo "=== precheck complete $(date)"
