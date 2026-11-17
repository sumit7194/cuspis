#!/bin/sh
# Verified-PID stop: signals only if the recorded PID still has the recorded start time and runs the EXP-034a watchdog.
cd "$(dirname "$0")"
read PID START < exp034a.pid
NOW=$(ps -o lstart= -p "$PID" 2>/dev/null); CMD=$(ps -o command= -p "$PID" 2>/dev/null)
if [ "$NOW" = "$START" ] && echo "$CMD" | grep -q "watchdog.py.*exp034a_wedge_mi.py"; then
  kill -TERM "$PID" && echo "sent SIGTERM to watchdog $PID (it stops the child's process group)"
else
  echo "NOT stopping: PID $PID is not the EXP-034a watchdog (start '$NOW' vs '$START'; cmd '$CMD')"; exit 1
fi
