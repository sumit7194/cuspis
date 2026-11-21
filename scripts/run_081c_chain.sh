#!/bin/zsh
# EXP-081c registered order (8fcfb84 + R1 440b49f): posctl W2P8b4 -> posctl W4P8b8 -> W2P8b8 (081b numerics) -> W8P8 target.
# One job at a time, nice 12, watchdog cap 1.5 GB, disk floor 5 GB, pressure stop. Stops at the first failure.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
PY=../.venv/bin/python; WD="$PY tools/watchdog.py --cap-gb 1.5 --min-disk-gb 5 --stop-on-pressure-warn"
run() { local name=$1; shift; echo "=== $name start $(date '+%H:%M:%S')"; eval nice -n 12 $WD --log exp081c_results/$name.wd.log --stdout exp081c_results/$name.out -- $PY -u -W ignore "$@"; local rc=$?; echo "=== $name exit $rc $(date '+%H:%M:%S')"; tail -1 exp081c_results/$name.wd.log; return $rc; }
run posctl_W2P8b4 exp081c_route.py 2 8 4 posctl || exit 1
run posctl_W4P8b8 exp081c_route.py 4 8 8 posctl || exit 2
run W2P8b8_081b exp081b_worker.py 2 8 8 2 12 3.0 0 || exit 3
cp exp081b_results/sigma_W2_P8_box8_c2_cp12_sc3.0_dd0.json exp081b_results/sigma_W2_P8_box8_c2_cp12_sc3.0_dd0_ckpt.json exp081c_results/
run target_W8P8b8 exp081c_route.py 8 8 8 target || exit 4
echo "=== chain complete $(date '+%H:%M:%S')"
