#!/bin/zsh
# DEPRECATED 2026-11-24 (Bridge fleet rule): this guard KILLS BY PATTERN (pkill -f), which can hit other sessions' processes and, for
# guard_081d_w12.sh, the 081e W12 route itself. Never re-arm. Use PID-scoped signalling (see freepct_guard.sh v3). Body kept for the record.
echo "DEPRECATED: $0 kills by pattern; refusing to run (see header)" >&2; exit 2
# EXP-081d: k = 3 is VOID (CEN flagged W12P12b12). Stop run_081d_stage2.sh before route W12 computes anything (Bridge ruling 2026-11-23).
# Usage: guard_081d_w12.sh <stage2 log> <runner pid>   (fires when the log shows "=== route_W12P12b12 start") [model: Opus 5.5]
LOG=$1; RP=$2
until grep -q "=== route_W12P12b12 start" $LOG; do sleep 20; ps -p $RP >/dev/null || { echo "runner $RP gone; guard exits $(date)"; exit 0; }; done
echo "GUARD FIRED $(date '+%F %T'): stopping runner $RP and any W12 route"
kill $RP; pkill -f "exp081d_route.py 12 12 12"; sleep 2; pkill -f "exp081d_route.py 12 12 12"; echo "=== route_W12P12b12 STOPPED by guard (k = 3 VOID, CEN)" >> $LOG
