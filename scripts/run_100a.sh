#!/bin/zsh
# EXP-100 part A runner (registration 4dbbf5a + am. 1 d9edfa5). Mac mini, 1 BLAS thread, nice 10, >= 50% free gate, no-kill watchdog, no hard caps. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
unset CUSPIS_081E CUSPIS_087
PY=../.venv/bin/python; D=exp081d_results; L=$D/run_100a.txt; DONE=$D/run_100a.done; T=e100_free
stop() { echo "=== STOP $(date '+%F %T'): $1 -> tell the Bridge" >> $L; touch $DONE; exit 1; }
[ "$(cd "$(dirname $PY)" && pwd -P)" = "$(cd ../.venv/bin && pwd -P)" ] && $PY -I -c "import numpy, scipy" 2>/dev/null || stop "PREFLIGHT: venv with numpy+scipy not available"
for f in $D/exp100_free.json $D/$T.wd.log; do [ -e $f ] && stop "target $f already exists (stale-file guard)"; done
rm -f $DONE; echo "=== run_100a start $(date '+%F %T') PID $$; venv $($PY -c 'import sys,numpy,scipy;print(sys.version.split()[0],numpy.__version__,scipy.__version__)')" >> $L
while true; do f=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}')
  (( f >= 50 )) && { echo "=== GATE $(date '+%F %T'): free ${f}% -> LAUNCH" >> $L; break; }; echo "=== GATE $(date '+%F %T'): WAIT free ${f}%" >> $L; sleep 300; done
nice -n 10 $PY tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore exp100_free.py
rc=$?; echo "=== $T rc $rc $(date '+%F %T') $(grep -h '# exit' $D/$T.wd.log | tail -1)" >> $L
(( rc == 0 )) || stop "exp100_free rc != 0 (control FAIL or crash)"
echo "=== run_100a complete $(date '+%F %T')" >> $L; touch $DONE
