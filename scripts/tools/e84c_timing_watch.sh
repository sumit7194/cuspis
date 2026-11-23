#!/bin/zsh
# Part-8 timing watch (Bridge 2026-11-23): log each 084c geometry's wall time against its projection; if W4P8 runs past
# 1.5x its projection (lower end 5.2 h -> 7.8 h = 28080 s) while still running, write an OVERRUN line BEFORE W8P8 can start. [model: Opus 5.5]
L=${1:-exp081d_results/run_queue8.txt}; typeset -A PROJ; PROJ=(W6P6 6122 W4P8 18362 W8P8 20848)   # W-corrected projection, seconds
ep() { date -j -f "%F %H:%M:%S" "$(date +%F) $1" +%s; }
for T in W6P6 W4P8 W8P8; do
  until grep -q "=== e84c_$T start" $L 2>/dev/null; do grep -q "STOP" $L 2>/dev/null && exit 0; sleep ${DT:-60}; done
  s=$(date +%s); warned=0
  until grep -q "=== e84c_$T end" $L; do
    if [ $T = W4P8 ] && [ $warned = 0 ] && [ $(( $(date +%s) - s )) -gt ${OVR:-28080} ]; then
      echo "=== TIMING OVERRUN: e84c_W4P8 still running after $(( ($(date +%s) - s) / 60 )) min > 1.5x projection (7.8 h); report to the Bridge before W8P8 $(date '+%F %T')" >> $L; warned=1; fi
    grep -q "STOP" $L && exit 0; sleep ${DT:-60}
  done
  w=$(grep -h "# exit" ${WDD:-exp081d_results}/e84c_$T.wd.log 2>/dev/null | tail -1 | sed -E 's/.*wall ([0-9]+) s.*/\1/')
  echo "=== TIMING e84c_$T: wall ${w:-?} s vs projection ${PROJ[$T]} s (ratio $( [ -n "$w" ] && printf '%.2f' $(( w * 1.0 / PROJ[$T] )) || echo '?'))" >> $L
done
