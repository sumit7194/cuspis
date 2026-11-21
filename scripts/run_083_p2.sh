#!/bin/zsh
# EXP-083 R2 (+A1): P = 2 honest Arb data, n <= 48, one job at a time, nice 12, watchdog 1.5 GB.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
for W in 2 4; do for arm in a b; do
  nice -n 12 ../.venv/bin/python tools/watchdog.py --log exp083_r2/W${W}P2${arm}.wd.log --cap-gb 1.5 --min-disk-gb 5 --stop-on-pressure-warn --stdout exp083_r2/W${W}P2${arm}.out -- ../.venv/bin/python -u -W ignore exp083_arb.py $W 2 48 $arm exp083_r2/W${W}P2${arm}.json || { echo "STOP at W${W} arm ${arm}"; exit 1; }
done; done; echo "P=2 data complete $(date)"
