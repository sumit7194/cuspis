#!/bin/zsh
# Bridge 2026-11-24: second TIMING line if W8P8 passes 1.5x its REVISED estimate (~10 h -> 15 h = 54000 s). Informational, not a stop. [model: Opus 5.5]
L=${1:-exp081d_results/run_queue8.txt}; LIM=${LIM:-54000}; DT=${DT:-60}
until grep -q "=== e84c_W8P8 start" $L 2>/dev/null; do grep -q "STOP" $L 2>/dev/null && exit 0; sleep $DT; done; s=$(date +%s)
until grep -q "=== e84c_W8P8 end" $L; do
  if [ $(( $(date +%s) - s )) -gt $LIM ]; then echo "=== TIMING OVERRUN (revised): e84c_W8P8 still running after $(( ($(date +%s) - s) / 60 )) min > 1.5x revised estimate (15 h); informational $(date '+%F %T')" >> $L; exit 0; fi
  grep -q "STOP" $L && exit 0; sleep $DT
done
