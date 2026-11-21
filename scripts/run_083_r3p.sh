#!/bin/zsh
# EXP-083 R3' chain (registered c9a0ed0), one job at a time, nice 12, watchdog 1.5 GB. Arm (a) only.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
PY=../.venv/bin/python; WD="$PY tools/watchdog.py --cap-gb 1.5 --min-disk-gb 5 --stop-on-pressure-warn"
run() { local name=$1; shift; echo "=== $name start $(date '+%H:%M:%S')"; eval nice -n 12 $WD --log exp083_r3p/$name.wd.log --stdout exp083_r3p/$name.out -- $PY -u -W ignore "$@" || echo "=== $name FAILED"; echo "=== $name end $(date '+%H:%M:%S')"; }
# 1. Arb honest arm (a) at P = 4 (081b geometries), n <= 12
for W in 2 4; do run arb_W${W}P4a exp083_arb.py $W 4 12 a exp083_r3p/W${W}P4a.json; done
# 2. production port at P = 2, n = 1..72 ; planted at n = 1..3 ; link
for W in 2 4; do run port_W${W}P2_base exp083_r3p_run.py $W 2 72 base
  for v in scut_low merge_tiny drop_pole res_scale dd1; do run port_W${W}P2_$v exp083_r3p_run.py $W 2 3 $v; done
  run port_W${W}P2_link exp083_r3p_run.py $W 2 1 link; done
# 3. production port at P = 4, n = 1..8 ; planted n = 1..3 ; link
for W in 2 4; do run port_W${W}P4_base exp083_r3p_run.py $W 4 6 base
  for v in scut_low merge_tiny drop_pole res_scale dd1; do run port_W${W}P4_$v exp083_r3p_run.py $W 4 2 $v; done
  run port_W${W}P4_link exp083_r3p_run.py $W 4 1 link; done
echo "=== R3' chain complete $(date)"
