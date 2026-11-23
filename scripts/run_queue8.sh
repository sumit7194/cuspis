#!/bin/zsh
# Queue part 8: EXP-084c amendment-2 core set, remaining geometries W6P6, W4P8, W8P8 at n = 2 (one at a time, nice 12, no-kill), then READ.
# Waits for queue part 7b (EXP-085 B-E rerun) and starts only on its clean completion (gate below). Routes stay on HOLD until the Bridge's go. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; unset CUSPIS_081E EXP085_A5
while ps -p ${RUNNER_Q7:-89902} >/dev/null; do sleep 30; done; echo "=== queue part 7b ended $(date '+%F %T')"
# Completion gate (Bridge 2026-11-23): start ONLY if 7b exited cleanly: its log carries "BCDE (amendment 5) rc 0" AND
# E.json exists, is newer than 7b's start, and has amendment == 5. Otherwise STOP -> HOLD (Cuspis messages the Bridge).
Q7LOG=${Q7LOG:-$D/run_queue7b.txt}; Q7RES=${Q7RES:-$D/exp085/E.json}; Q7SINCE=${Q7SINCE:-$(date -j -f "%F %T" "2026-11-23 20:56:36" +%s)}
okrc=$(grep -c "BCDE (amendment 5) rc 0 " $Q7LOG 2>/dev/null); mt=$(stat -f %m $Q7RES 2>/dev/null || echo 0)
am=$($PY -c "import json,sys; print(json.load(open(sys.argv[1])).get('amendment'))" $Q7RES 2>/dev/null)
if [ "${okrc:-0}" -ge 1 ] && [ $mt -gt $Q7SINCE ] && [ "$am" = "5" ]; then echo "=== GATE OK: 7b rc 0, E.json fresh ($(date -r $mt '+%T')), amendment 5"
else echo "=== STOP: predecessor 7b not clean (rc0 lines ${okrc:-0}, E.json mtime $mt vs since $Q7SINCE, amendment '$am') -> HOLD, part 8 NOT started $(date '+%F %T')"; exit 1; fi
[ -n "$Q8_DRYGATE" ] && { echo "=== DRYGATE: exiting before any geometry"; exit 0; }
for G in "6 6" "4 8" "8 8"; do
  set -- ${=G}; T=e84c_W$1P$2
  echo "=== $T start $(date '+%H:%M:%S')"
  pgate_run $D/$T.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --soft-cap-gb 1.0 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore exp084c_run.py $1 $2 2"
  rc=$?; echo "=== $T end $(date '+%H:%M:%S') rc $rc"; [ $rc -ne 0 ] && { echo "=== STOP: $T rc $rc"; exit 1; }
done
echo "=== e84c_READ start $(date '+%H:%M:%S')"
pgate_run $D/e84c_READ.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --log $D/e84c_READ.wd.log --stdout $D/e84c_READ.out -- $PY -u -W ignore exp084c_run.py READ"
echo "=== EXP-084c READ (amendment 2 core set) rc $? $(date '+%F %T')"; echo "=== HOLD (routes await the Bridge's go)"
