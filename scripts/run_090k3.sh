#!/bin/zsh
# EXP-090 k = 3 readings (K3 mode) on the Bridge's "K3 go" (2026-11-28, after 038df25). Mac mini. [model: Opus 5.5]
# 1 BLAS thread, nice 10, gate free >= 50% + pgate, freepct_guard (pause-only), no-kill watchdog. No hard caps.
# Interpreter: the same python3 that ran the DRY (exp090_k3_DRY_ska.out), so the bitwise controls run on the tested path.
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1; source tools/pgate.sh
PY=/opt/homebrew/bin/python3; D=exp081d_results; L=$D/run_090k3.txt
stop() { echo "=== STOP $(date '+%F %T'): $1 -> tell the Bridge" >> $L; touch $D/run_090k3.done; exit 1; }
[ -e $D/exp090_k3.json ] && stop "exp090_k3.json already exists (stale-file guard)"
rm -f $D/run_090k3.done; DONE_FILE=$D/run_090k3.done nohup zsh tools/freepct_guard.sh $$ $L 'exp090_k3|exp090_reread|watchdog\.py' > /dev/null 2>&1 &
echo "=== run_090k3 start $(date '+%F %T') PID $$; freepct_guard $!; $($PY -c 'import sys,numpy;print(sys.version.split()[0],numpy.__version__)')" >> $L
gate() { while true; do f=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}')
  (( f >= 50 )) && { echo "=== GATE $1 $(date '+%F %T'): free ${f}% -> LAUNCH (pgate next)" >> $L; break; }; echo "=== GATE $1 $(date '+%F %T'): WAIT free ${f}%" >> $L; sleep 300; done; }
T=e90_K3; [ -e $D/$T.wd.log ] && stop "log tag $T already used"; gate $T; echo "=== $T start $(date '+%F %T')" >> $L
pgate_run $D/$T.wd.log "nice -n 10 $PY tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore exp090_k3.py K3"
rc=$?; echo "=== $T rc $rc $(date '+%F %T')" >> $L
(( rc == 0 )) || stop "K3 rc $rc (REFUSE / control FAIL / gate FAIL)"
echo "=== run_090k3 complete $(date '+%F %T')" >> $L; touch $D/run_090k3.done
