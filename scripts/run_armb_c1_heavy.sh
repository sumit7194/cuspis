#!/bin/zsh
# EXP-083 R3' arm (b) C1 heavy geometries (registered 4ee07fe). Gate: not before 07:30 (Bridge: CPU saturated until tabula ends).
# One job at a time, nice 12, watchdog cap 1.5 GB (declared: P10 ~0.75 GB formula), disk floor 5 GB, pressure stop.
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; PY=../.venv/bin/python
while [ $(date +%H%M) -lt 0730 ]; do sleep 120; done; echo "=== gate open $(date)"
for G in 2:6:4:2 4:6:4:2 2:6:4:3 4:6:4:3 2:8:4:2 4:8:4:2 4:8:8:2 8:8:8:2 2:10:4:2 4:10:4:2 2:12:4:2 4:12:4:2; do
  IFS=: read W P B C <<< "$G"; tag=c1_W${W}P${P}box${B}c${C}; echo "=== $tag start $(date '+%H:%M:%S')"
  nice -n 12 $PY tools/watchdog.py --log exp083_armb/$tag.wd.log --cap-gb 1.5 --min-disk-gb 5 --stop-on-pressure-warn --stdout exp083_armb/$tag.out -- $PY -u -W ignore exp083_armb_c1.py $W $P $B $C || echo "=== $tag FAILED"
  grep "C1 W\|plant" exp083_armb/$tag.out; tail -1 exp083_armb/$tag.wd.log; done
echo "=== C1 heavy complete $(date)"
