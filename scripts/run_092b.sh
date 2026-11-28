#!/bin/zsh
# EXP-092 amendment b: KA controls, then centre c_A at P = 24. Mac mini, beside the EXP-096 A6 rerun (Bridge 2026-11-28). [model: Opus 5.5]
# 1 BLAS thread (as registered), nice 10, gate free >= 50% + pgate, freepct_guard (pause-only), no-kill watchdog. No hard caps.
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; L=$D/run_092b.txt
stop() { echo "=== STOP $(date '+%F %T'): $1 -> tell the Bridge" >> $L; touch $D/run_092b.done; exit 1; }
[ -e $D/exp092_cA_P24.json ] && stop "exp092_cA_P24.json already exists (stale-file guard)"
rm -f $D/run_092b.done; DONE_FILE=$D/run_092b.done nohup zsh tools/freepct_guard.sh $$ $L 'exp092_cA_centre|watchdog\.py' > /dev/null 2>&1 &
echo "=== run_092b start $(date '+%F %T') PID $$; freepct_guard $!" >> $L
gate() { while true; do f=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}')
  (( f >= 50 )) && { echo "=== GATE $1 $(date '+%F %T'): free ${f}% -> LAUNCH (pgate next)" >> $L; break; }; echo "=== GATE $1 $(date '+%F %T'): WAIT free ${f}%" >> $L; sleep 300; done; }
run() { local T=$1; shift; [ -e $D/$T.wd.log ] && stop "log tag $T already used"; gate $T; echo "=== $T start $(date '+%F %T') args: $*" >> $L
  pgate_run $D/$T.wd.log "nice -n 10 $PY tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore exp092_cA_centre.py $*"
  local rc=$?; echo "=== $T rc $rc $(date '+%F %T')" >> $L; return $rc; }
run e92b_KA KA || stop "KA controls FAILED"
run e92b_P24 P 24 || stop "P = 24 rc != 0 (or symmetry FAIL)"
echo "=== run_092b complete $(date '+%F %T')" >> $L; touch $D/run_092b.done
