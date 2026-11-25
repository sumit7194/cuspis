#!/bin/zsh
# EXP-087 (c): W8P8 t0 via the production route, flag OFF (KA: must reproduce stored -209.300109928361 bitwise) then flag ON (corrected t0).
# One extra core (Bridge +1 allowance, fleet <= 9), sequential, nice 12, no-kill watchdog, free >= 50% at each launch. CUSPIS_081E unset
# (the stored value is 081d-era). [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; unset CUSPIS_081E; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; L=$D/run_087c.txt
gate() { local f; while true; do f=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}')
  (( f >= 50 )) && { echo "=== GATE $1 $(date '+%F %T'): free ${f}% -> LAUNCH" >> $L; return; }; echo "=== GATE $1: WAIT free ${f}%" >> $L; sleep 300; done; }
run() { local T=$1 flag=$2; gate $T; echo "=== $T start $(date '+%F %T') CUSPIS_087=$flag" >> $L
  CUSPIS_087=$flag pgate_run $D/$T.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore exp081d_route.py 8 8 8 --production-only --nodes 0:0 --tag-suffix _087$3"
  echo "=== $T rc $? $(date '+%F %T')" >> $L; }
run e87_W8P8_off 0 off
grep -q "t0 -209.300109928361 " $D/e87_W8P8_off.out && echo "=== KA flag OFF: t0 reproduces -209.300109928361 (string-exact)" >> $L || { echo "=== STOP: KA flag OFF does NOT reproduce the stored t0" >> $L; exit 1; }
run e87_W8P8_on 1 on
echo "=== EXP-087 (c) done $(date '+%F %T')" >> $L
