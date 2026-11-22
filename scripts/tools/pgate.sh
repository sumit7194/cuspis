#!/bin/zsh
# Pressure gate + retry for chain runners (2026-11-22, after the 06:29 cascade: one transient yellow-pressure episode caused by a
# foreign 2.1 GB process killed the 081c W8P8 target and then 1-second-killed every later arm-(a) P4 job in its chain).
# Mechanism, not promise:
#   pgate_wait          block until kern.memorystatus_vm_pressure_level == 1 for PGATE_STABLE seconds (default 300), polling 30 s
#   pgate_run LOG CMD.. run CMD (a watchdog invocation whose --log is LOG) after pgate_wait; if the watchdog log's last line says it was
#                       killed by memory pressure, wait again and retry, at most PGATE_TRIES times (default 3). Other failures: no retry.
# Retries are only safe for checkpointed or deterministic, side-effect-free jobs (all current users are). Each attempt's wd log is kept
# as LOG.tryK before the retry overwrites it.   [model: Opus 5.5]
pgate_wait() {
  local stable=${PGATE_STABLE:-300} ok=0
  while [ $ok -lt $stable ]; do
    if [ "$(sysctl -n kern.memorystatus_vm_pressure_level)" = "1" ]; then ok=$((ok + 30)); else ok=0; fi
    [ $ok -lt $stable ] && sleep 30
  done
}
pgate_run() {
  local log=$1; shift; local k=1 rc
  while true; do
    pgate_wait; echo "# pgate: attempt $k at $(date '+%H:%M:%S') (pressure normal >= ${PGATE_STABLE:-300} s)"
    eval "$@"; rc=$?
    if [ $rc -ne 0 ] && tail -1 "$log" 2>/dev/null | grep -q "KILLED: memory pressure" && [ $k -lt ${PGATE_TRIES:-3} ]; then
      cp "$log" "$log.try$k"; echo "# pgate: attempt $k killed by memory pressure; retrying"; k=$((k + 1)); continue
    fi
    return $rc
  done
}
