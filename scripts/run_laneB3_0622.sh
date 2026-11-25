#!/bin/zsh
# DEPRECATED 2026-11-25 (Sumit's standing rule: NO job-ending caps): this runner passes kill-mode watchdog flags
# (--stop-on-pressure-warn / --pressure-stop-level). Convert to the no-kill watchdog before any reuse. Body kept for the record.
echo "DEPRECATED: $0 uses kill-mode flags; refusing to run (see header)" >&2; exit 2
# Lane B (cont.): C2 at P = 4 (registered scope n <= 6): W2P4 now; W4P4 once lane A has written exp083_r3p/W4P4_link.json. [model: Opus 5.5]
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; WD="$PY tools/watchdog.py --min-disk-gb 5 --stop-on-pressure-warn"
job() { local dir=$1 name=$2 cap=$3; shift 3; echo "=== $name start $(date '+%H:%M:%S')"
  pgate_run $dir/$name.wd.log "nice -n 12 $WD --cap-gb $cap --log $dir/$name.wd.log --stdout $dir/$name.out -- $PY -u -W ignore $*" || echo "=== $name FAILED"
  echo "=== $name end $(date '+%H:%M:%S')"; tail -1 $dir/$name.wd.log; grep -E "n=|route" $dir/$name.out | tail -8; }
job exp083_armb c2_W2P4 1.5 exp083_armb_c2.py 2 4 6
until [ -f exp083_r3p/W4P4_link.json ]; do sleep 60; done; echo "=== W4P4 link present $(date '+%H:%M:%S')"
job exp083_armb c2_W4P4 1.5 exp083_armb_c2.py 4 4 6
echo "=== lane B3 complete $(date)"
