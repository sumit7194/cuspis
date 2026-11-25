#!/bin/sh
# DEPRECATED 2026-11-25 (Sumit's standing rule: NO job-ending caps): this runner passes kill-mode watchdog flags
# (--stop-on-pressure-warn / --pressure-stop-level). Convert to the no-kill watchdog before any reuse. Body kept for the record.
echo "DEPRECATED: $0 uses kill-mode flags; refusing to run (see header)" >&2; exit 2
# EXP-034a launch (bridge slot 2026-11-17): 1 core, nice 15, detached; watchdog 4 GB tree cap, 5 GB disk floor, stop on pressure yellow.
set -e
cd "$(dirname "$0")"
DISK=$(df -g . | awk 'NR==2{print $4}'); LVL=$(sysctl -n kern.memorystatus_vm_pressure_level)
echo "pre-launch: free disk ${DISK} GB, memory pressure level ${LVL}"
[ "$DISK" -ge 5 ] || { echo "STOP: disk < 5 GB"; exit 4; }
[ "$LVL" -le 1 ] || { echo "STOP: memory pressure level $LVL"; exit 5; }
export OMP_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
nohup nice -n 15 python3 tools/watchdog.py --log exp034a.wd.log --stdout exp034a_output.txt --cap-gb 4 --min-disk-gb 5 \
  --stop-on-pressure-warn --interval 5 -- ../.venv/bin/python -u exp034a_wedge_mi.py > exp034a.nohup 2>&1 &
PID=$!
sleep 1
echo "$PID $(ps -o lstart= -p $PID)" > exp034a.pid
echo "launched watchdog PID $PID: $(ps -o pid=,ni=,command= -p $PID)"
