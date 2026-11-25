#!/bin/zsh
# DEPRECATED 2026-11-25 (Sumit's standing rule: NO job-ending caps): this runner passes kill-mode watchdog flags
# (--stop-on-pressure-warn / --pressure-stop-level). Convert to the no-kill watchdog before any reuse. Body kept for the record.
echo "DEPRECATED: $0 uses kill-mode flags; refusing to run (see header)" >&2; exit 2
# EXP-081d Stage 1 (registration 963c8f5; runs only after the Bridge's GO). Three lanes, nice 12, watchdog per lane, pgate, pressure-stop.
# Declared: L1/L2 cap 2.3 GB (formula k = 2.5 ~1.5 GB), L3 cap 1.0 GB (k = 1.5 ~0.5 GB); total formula <= 3.4 GB. [model: Opus 5.5]
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results
job() { local name=$1 cap=$2 soft=${SOFT:-}; shift 2; echo "=== $name start $(date '+%H:%M:%S')"
  pgate_run $D/$name.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --stop-on-pressure-warn --cap-gb $cap ${soft:+--soft-cap-gb $soft} --log $D/$name.wd.log --stdout $D/$name.out -- $PY -u -W ignore $*" || echo "=== $name FAILED"
  echo "=== $name end $(date '+%H:%M:%S')"; tail -1 $D/$name.wd.log; }
L1() { job route_W10P10b10 2.3 exp081d_route.py 10 10 10; job c1_W10P10b10 2.3 exp083_armb_c1.py 10 10 10 2; echo "=== L1 complete $(date)"; }
L2() { job route_W5P10b10 2.3 exp081d_route.py 5 10 10; job c1_W5P10b10 2.3 exp083_armb_c1.py 5 10 10 2
       [ -f $D/sigma_W4_P8_box8_c2_cp12_sc3.0_dd0_ckpt.json ] || cp exp081c_results/sigma_W4_P8_box8_c2_cp12_sc3.0_dd0_ckpt.json $D/
       job checks_W4P8b8 1.5 exp081d_route.py 4 8 8; echo "=== L2 complete $(date)"; }
L3() { job census 1.0 exp081d_census.py 3:6:6 6:6:6 5:10:10 10:10:10
       for g in "3 6 6" "6 6 6" "5 10 10" "10 10 10"; do job step0_${g// /_} 1.0 exp081d_step0.py $g; done
       job route_W3P6b6 1.0 exp081d_route.py 3 6 6; job route_W6P6b6 1.0 exp081d_route.py 6 6 6
       job c1_W3P6b6 1.0 exp083_armb_c1.py 3 6 6 2; job c1_W6P6b6 1.0 exp083_armb_c1.py 6 6 6 2; echo "=== L3 complete $(date)"; }
# relaunch (2026-11-22 ~21:55, Bridge OK + Sumit: soft caps that inform): route then C1 in the same lane, so C1 grades against the STORED T_sad
L1b() { SOFT=3.5 job route_W10P10b10 5.0 exp081d_route.py 10 10 10; SOFT=3.5 job c1_W10P10b10 5.0 exp083_armb_c1.py 10 10 10 2; echo "=== L1b complete $(date)"; }
L2b() { SOFT=3.5 job route_W5P10b10 5.0 exp081d_route.py 5 10 10; SOFT=3.5 job c1_W5P10b10 5.0 exp083_armb_c1.py 5 10 10 2
        [ -f $D/sigma_W4_P8_box8_c2_cp12_sc3.0_dd0_ckpt.json ] || cp exp081c_results/sigma_W4_P8_box8_c2_cp12_sc3.0_dd0_ckpt.json $D/
        SOFT=2.0 job checks_W4P8b8 3.0 exp081d_route.py 4 8 8; echo "=== L2b complete $(date)"; }
case $1 in L1) L1;; L2) L2;; L3) L3;; L1b) L1b;; L2b) L2b;; esac
