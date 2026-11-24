#!/bin/zsh
# DEPRECATED 2026-11-24 (Bridge fleet rule): this guard KILLS BY PATTERN (pkill -f), which can hit other sessions' processes and, for
# guard_081d_w12.sh, the 081e W12 route itself. Never re-arm. Use PID-scoped signalling (see freepct_guard.sh v3). Body kept for the record.
echo "DEPRECATED: $0 kills by pattern; refusing to run (see header)" >&2; exit 2
# Generic stop-guard: when LOG shows MARK, kill RUNNER and any process matching PKILLPAT (repeated, to catch pgate's delayed launch).
# Usage: guard_stop_at.sh <log> <runner pid> <mark> <pkill pattern>   [model: Opus 5.5]
LOG=$1; RP=$2; MARK=$3; PAT=$4
until grep -qF -- "$MARK" $LOG 2>/dev/null; do sleep 10; ps -p $RP >/dev/null || { echo "runner $RP gone before mark; guard exits $(date)"; exit 0; }; done
echo "GUARD FIRED $(date '+%F %T'): '$MARK' seen; stopping runner $RP and '$PAT'"
kill $RP 2>/dev/null; for i in 1 2 3 4 5 6; do pkill -f -- "$PAT" 2>/dev/null; sleep 10; done
echo "=== STOPPED by guard_stop_at ('$MARK'): held for Sumit's route-pressure decision $(date '+%F %T')" >> $LOG
