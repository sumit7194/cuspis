#!/bin/zsh
# DEPRECATED 2026-11-25 (Sumit's standing rule: NO job-ending caps): this runner passes kill-mode watchdog flags
# (--stop-on-pressure-warn / --pressure-stop-level). Convert to the no-kill watchdog before any reuse. Body kept for the record.
echo "DEPRECATED: $0 uses kill-mode flags; refusing to run (see header)" >&2; exit 2
# EXP-081d Stage 2 (k = 3), SERIAL: one process at a time (Sumit 2026-11-23: "let it grow, lets see where it reaches solo").
# Measured per-process peak 7.32 GB (gate-2 probes, report 57471e3); 2 processes would be 14.6 GB > 13, so serial.
# Order: census + Step 0 at both k = 3 geometries FIRST (minutes); a Step-0 fail at s <= 1.974 voids the geometry (row S0, via
# exp081d_analyze.step0_cap), so its route is skipped. Then route W6 -> C1 W6 -> route W12 -> C1 W12.
# Caps: soft caps WARN only (log + stdout); the hard cap is a high backstop; pressure-stop is the real guard. nice 12, pgate.
# Expected (argued from measured ratios): route ~29 h each, C1 ~1-3 h, total ~62 h; check-in bound 3x = 90 h per route. [model: Opus 5.5]
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results
job() { local name=$1 cap=$2 soft=${SOFT:-}; shift 2; echo "=== $name start $(date '+%H:%M:%S')"
  pgate_run $D/$name.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --stop-on-pressure-warn --cap-gb $cap ${soft:+--soft-cap-gb $soft} --log $D/$name.wd.log --stdout $D/$name.out -- $PY -u -W ignore $*" || echo "=== $name FAILED"
  echo "=== $name end $(date '+%H:%M:%S')"; tail -1 $D/$name.wd.log; }
void() { $PY -c "import json,sys; import exp081d_analyze as A; c,v=A.step0_cap(json.load(open('$D/step0_W$1P12b12.json'))); print('step0 W$1: cap',c,'void node',v); sys.exit(1 if v is not None else 0)"; }
SOFT=2.0 job census_k3 4.0 exp081d_census.py 6:12:12 12:12:12
for W in 6 12; do SOFT=2.0 job step0_W${W}P12b12 4.0 exp081d_step0.py $W 12 12; done
for W in 6 12; do
  if void $W; then
    SOFT=8.0 job route_W${W}P12b12 11.0 exp081d_route.py $W 12 12
    SOFT=4.0 job c1_W${W}P12b12 8.0 exp083_armb_c1.py $W 12 12 2
  else echo "=== W$W VOID by Step 0 (row S0): route skipped -> STOP"; fi
done
echo "=== Stage2 complete $(date)"
