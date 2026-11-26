#!/bin/zsh
# Pause keeper (Bridge - claude personal 2026-11-26: pause exp087_t0 PID 31961 for Sumit's office work; no guard may auto-resume it). [model: Opus 5.5]
# Usage: pause_keeper.sh PID ARGV_REGEX LOG RELEASE_FILE. Verifies PID is alive and its command line matches ARGV_REGEX, then SIGSTOPs it.
# Every DT s (default 10): if RELEASE_FILE exists -> log and exit WITHOUT signalling (the resume SIGCONT is done by hand, by PID).
# If the PID is gone or its command line no longer matches -> log and exit (never signals a different process).
# If the process is no longer stopped (state not T, e.g. a guard sent SIGCONT) -> SIGSTOP it again and log RE-PAUSE.
# Signals ONLY the one given PID. Never kills. Pause-only.
PID=$1; RX=$2; LOG=$3; REL=$4; DT=${DT:-10}
ok() { local c=$(ps -o command= -p $PID 2>/dev/null); [[ -n "$c" && "$c" =~ $RX ]]; }
ok || { echo "=== PAUSE-KEEPER $(date '+%F %T'): PID $PID missing or argv mismatch at start -> nothing signalled, exit" >> $LOG; exit 1; }
kill -STOP $PID && echo "=== PAUSE-OFFICE $(date '+%F %T'): SIGSTOP PID $PID (argv matches '$RX'); keeper PID $$ re-pauses it if anything resumes it; release file $REL (Bridge - claude personal; resume only on Sumit's word)" >> $LOG
while true; do sleep $DT
  [ -e "$REL" ] && { echo "=== PAUSE-KEEPER $(date '+%F %T'): release file seen -> keeper exits (no signal sent)" >> $LOG; exit 0; }
  ok || { echo "=== PAUSE-KEEPER $(date '+%F %T'): PID $PID gone or argv changed -> keeper exits (no signal sent)" >> $LOG; exit 0; }
  st=$(ps -o stat= -p $PID 2>/dev/null)
  [[ "$st" == T* ]] || { kill -STOP $PID && echo "=== RE-PAUSE $(date '+%F %T'): PID $PID was running (state $st; a guard resumed it?) -> SIGSTOP again" >> $LOG; }
done
