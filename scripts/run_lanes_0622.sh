#!/bin/zsh
# Relaunch after the 06:29 pressure cascade (2026-11-22). Two lanes (2 cores), nice 12, watchdog unchanged, every job behind tools/pgate.sh
# (pressure normal >= 300 s before launch; retry <= 3 on a pressure kill; killed outputs kept as *_killed0629.*).
#  lane A: R3' arm-(a) P4 ports (registered scope: base n <= 6, planted n <= 2, link), then the heavy C1 chain (not before 07:30).
#  lane B: 081c W8P8b8 target, resumed from its per-g checkpoint, then census / N4c / analyze are run by hand.
#  07:47 change: lane A = ports only, lane C = heavy C1 (own lane, 2 cores with A); PGATE_STABLE=60 between jobs (the
#  watchdog monitors pressure while a job runs; 300 s before each of ~20 jobs cost ~1.5 h of idle).
#  NOT here: Arb P = 4 arm (b) (~3 GB) -- held until the Bridge says tabula is done.   [model: Opus 5.5]
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; WD="$PY tools/watchdog.py --min-disk-gb 5 --stop-on-pressure-warn"
job() { local dir=$1 name=$2 cap=$3; shift 3; echo "=== $name start $(date '+%H:%M:%S')"
  pgate_run $dir/$name.wd.log "nice -n 12 $WD --cap-gb $cap --log $dir/$name.wd.log --stdout $dir/$name.out -- $PY -u -W ignore $*" || echo "=== $name FAILED"
  echo "=== $name end $(date '+%H:%M:%S')"; tail -1 $dir/$name.wd.log; }
laneA() {
  for W in 2 4; do job exp083_r3p port_W${W}P4_base 1.5 exp083_r3p_run.py $W 4 6 base
    for v in scut_low merge_tiny drop_pole res_scale dd1; do job exp083_r3p port_W${W}P4_$v 1.5 exp083_r3p_run.py $W 4 2 $v; done
    job exp083_r3p port_W${W}P4_link 1.5 exp083_r3p_run.py $W 4 1 link; done
  echo "=== lane A ports done $(date)"; }
laneC() { while [ $(date +%H%M) -lt 0730 ]; do sleep 120; done; echo "=== C1 gate open $(date)"
  for G in 2:6:4:2 4:6:4:2 2:6:4:3 4:6:4:3 2:8:4:2 4:8:4:2 4:8:8:2 8:8:8:2 2:10:4:2 4:10:4:2 2:12:4:2 4:12:4:2; do
    IFS=: read W P B C <<< "$G"; job exp083_armb c1_W${W}P${P}box${B}c${C} 1.5 exp083_armb_c1.py $W $P $B $C
    grep "C1 W\|plant" exp083_armb/c1_W${W}P${P}box${B}c${C}.out; done; echo "=== lane A complete $(date)"; }
laneB() { job exp081c_results target_W8P8b8 1.5 exp081c_route.py 8 8 8 target; echo "=== lane B complete $(date)"; }
case $1 in A) laneA;; B) laneB;; C) laneC;; esac
