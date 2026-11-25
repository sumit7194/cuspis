#!/bin/zsh
# DEPRECATED 2026-11-25 (Sumit's standing rule: NO job-ending caps): this runner passes kill-mode watchdog flags
# (--stop-on-pressure-warn / --pressure-stop-level). Convert to the no-kill watchdog before any reuse. Body kept for the record.
echo "DEPRECATED: $0 uses kill-mode flags; refusing to run (see header)" >&2; exit 2
# Lane B (2026-11-22, Bridge GO 08:29 after tabula): C2 at P = 2 (W2, W4, n <= 24, registered 4ee07fe), then the declared Arb P = 4
# arm (b) (~3 GB, cap 3.2 GB), one W at a time, the 3 GB job alone in this lane. pgate (60 s) + watchdog, nice 12.  [model: Opus 5.5]
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; WD="$PY tools/watchdog.py --min-disk-gb 5 --stop-on-pressure-warn"
job() { local dir=$1 name=$2 cap=$3; shift 3; echo "=== $name start $(date '+%H:%M:%S')"
  pgate_run $dir/$name.wd.log "nice -n 12 $WD --cap-gb $cap --log $dir/$name.wd.log --stdout $dir/$name.out -- $PY -u -W ignore $*" || echo "=== $name FAILED"
  echo "=== $name end $(date '+%H:%M:%S')"; tail -1 $dir/$name.wd.log; }
for W in 2 4; do job exp083_armb c2_W${W}P2 1.5 exp083_armb_c2.py $W 2 24; grep -E "n=|route" exp083_armb/c2_W${W}P2.out | tail -4; done
for W in 2 4; do job exp083_r3p arb_W${W}P4b 3.2 exp083_arb.py $W 4 6 b exp083_r3p/W${W}P4b.json; done
echo "=== lane B2 complete $(date)"
