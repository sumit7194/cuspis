#!/bin/zsh
# DEPRECATED 2026-11-25 (Sumit's standing rule: NO job-ending caps): this runner passes kill-mode watchdog flags
# (--stop-on-pressure-warn / --pressure-stop-level). Convert to the no-kill watchdog before any reuse. Body kept for the record.
echo "DEPRECATED: $0 uses kill-mode flags; refusing to run (see header)" >&2; exit 2
# EXP-081d Stage-2 gate 2, attempt 2: k = 3 probe ALONE (attempt 1 pressure-killed at 7.32 GB while still rising, with the control alongside); soft 9.0 / hard 11.0 GB; k = 3 memory probe (Bridge-approved 2026-11-23; no R read: --production-only, separate _probe checkpoint).
# P3 : k = 3 W12P12b12, hardest node only (index 47, s = 5.972) -> per-process peak of the node phase.
# P25: known-answer control, the same probe at k = 2.5 W10P10b10 (full-run node-phase peak measured 2.90 GB; checks phase 3.20 GB).
#      If P25 reproduces ~2.9 the single-node probe captures the peak; if it reads lower, the creep is cumulative and
#      P3 is scaled by (full / probe) at k = 2.5. Caps: soft at the expected peak, hard well above it; pressure-stop on. [model: Opus 5.5]
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results
job() { local name=$1 cap=$2 soft=${SOFT:-}; shift 2; echo "=== $name start $(date '+%H:%M:%S')"
  pgate_run $D/$name.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --stop-on-pressure-warn --cap-gb $cap ${soft:+--soft-cap-gb $soft} --log $D/$name.wd.log --stdout $D/$name.out -- $PY -u -W ignore $*" || echo "=== $name FAILED"
  echo "=== $name end $(date '+%H:%M:%S')"; tail -1 $D/$name.wd.log; }
P3()  { SOFT=9.0 job probe_k3_W12P12b12 11.0 exp081d_route.py 12 12 12 --production-only --nodes 47:48 --tag-suffix _probe; echo "=== P3 complete $(date)"; }
$1
