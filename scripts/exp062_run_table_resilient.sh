#!/bin/bash
# DEPRECATED 2026-11-25 (Sumit's standing rule: NO job-ending caps): this runner passes kill-mode watchdog flags
# (--stop-on-pressure-warn / --pressure-stop-level). Convert to the no-kill watchdog before any reuse. Body kept for the record.
echo "DEPRECATED: $0 uses kill-mode flags; refusing to run (see header)" >&2; exit 2
# Resume-on-pressure wrapper (policy unchanged: the watchdog still stops at memory-pressure level >= 2; this only
# waits for the level to return to 1 and resumes from the per-q checkpoint). [model: Opus 5.5]
cd "$(dirname "$0")"
PY=../.venv/bin/python
for attempt in $(seq 1 40); do
  nxt=$($PY -c "import numpy as np;d=np.load('exp062_piece2_table.npz');print(min([q for q in range(9) if f'Dp_{q}' not in d] or [99]))")
  [ "$nxt" = "99" ] && break
  while [ "$(sysctl -n kern.memorystatus_vm_pressure_level)" -ge 2 ]; do sleep 60; done
  nice -n 12 $PY tools/watchdog.py --log exp062_piece2_table_run3_a${attempt}.wd.log --cap-gb 2 --min-disk-gb 5 --stop-on-pressure-warn \
     --stdout exp062_piece2_table_run3_a${attempt}_output.txt -- $PY -u -W ignore exp062_piece2_table.py 8 $nxt
  sleep 30
done
for attempt in $(seq 1 20); do
  grep -q "replaced" exp062_piece2_q0_extend_output.txt 2>/dev/null && break
  while [ "$(sysctl -n kern.memorystatus_vm_pressure_level)" -ge 2 ]; do sleep 60; done
  nice -n 12 $PY tools/watchdog.py --log exp062_piece2_q0_extend_a${attempt}.wd.log --cap-gb 2 --min-disk-gb 5 --stop-on-pressure-warn \
     --stdout exp062_piece2_q0_extend_output.txt -- $PY -u -W ignore exp062_piece2_q0_extend.py
  sleep 30
done
echo DONE
