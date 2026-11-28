#!/bin/zsh
# EXP-098 stage 0, re-run of the analysis after the STOP (amendment 2, eeb0279). A COPY of run_098s0.sh's machinery, not an edit. [model: Opus 5.5]
# Steps: interpreter PREFLIGHT -> free(3,4,b4), free(6,8,b8) on the venv -> PREFLIGHT again -> exp098_3w.py S0 (unchanged) on PYA.
# 1 BLAS thread, nice 10, gate free >= 50% + pgate, freepct_guard (pause-only), no-kill watchdog. No hard caps. Flags unset.
# Usage: run_098s0b.sh            (real)
#        run_098s0b.sh --preflight-only   (test; PREFLIGHT_PLANT=1 adds a non-existent cache, so the preflight MUST stop)
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
unset CUSPIS_081E CUSPIS_087; source tools/pgate.sh
PY=../.venv/bin/python; PYA=/opt/homebrew/bin/python3; D=exp081d_results; FB=exp081b_results
L=$D/run_098s0b.txt; DONE=$D/run_098s0b.done; [ "$1" = "--preflight-only" ] && { L=$D/run_098s0b_preflight_test.txt; DONE=/dev/null; }
stop() { echo "=== STOP $(date '+%F %T'): $1 -> tell the Bridge" >> $L; [ "$DONE" != /dev/null ] && touch $DONE; exit 1; }
FREES=($FB/free_W2_P4_box4_c2.json $FB/free_W3_P4_box4_c2.json $FB/free_W4_P4_box4_c2.json $FB/free_W4_P8_box8_c2.json $FB/free_W6_P8_box8_c2.json $FB/free_W8_P8_box8_c2.json)
[ "$PREFLIGHT_PLANT" = 1 ] && FREES+=($FB/free_W99_P4_box4_c2_PLANT.json)
# PREFLIGHT (mechanism, amendment 2): $1 = stage name; $2 = "pre" (new-width caches may be absent: only the venv compute path is needed) or "ana"
preflight() {
  [ "$(cd "$(dirname $PY)" && pwd -P)" = "$(cd ../.venv/bin && pwd -P)" ] || stop "PREFLIGHT $1: PY is not the project venv"
  $PY -I -c "import numpy, scipy" 2>/dev/null || stop "PREFLIGHT $1: venv cannot import numpy+scipy"
  $PYA -I -c "import numpy" 2>/dev/null || stop "PREFLIGHT $1: analysis interpreter cannot import numpy"
  if ! $PYA -I -c "import scipy" 2>/dev/null; then
    local miss=() f; for f in $FREES; do [ -e $f ] || miss+=($f); done
    if [ "$2" = ana ] && (( ${#miss} )); then stop "PREFLIGHT $1: analysis interpreter has no scipy and free caches are missing: $miss"; fi
    if [ "$2" = pre ]; then for f in $miss; do case $f in *W3_P4_box4*|*W6_P8_box8*) ;; *) stop "PREFLIGHT $1: no scipy on the analysis interpreter and a STORED free cache is missing: $f";; esac; done; fi
  fi
  echo "=== PREFLIGHT $1 PASS $(date '+%F %T'): venv $($PY -c 'import sys,numpy,scipy;print(sys.version.split()[0],numpy.__version__,scipy.__version__)'); analysis $($PYA -c 'import sys,numpy;print(sys.version.split()[0],numpy.__version__)') (scipy: $($PYA -I -c 'import scipy' 2>/dev/null && echo yes || echo no; true)); free caches checked ${#FREES}" >> $L; }
if [ "$1" = "--preflight-only" ]; then preflight test ana; echo "=== preflight-only: PASS (no stop)" >> $L; exit 0; fi
for f in $FB/free_W3_P4_box4_c2.json $FB/free_W6_P8_box8_c2.json $D/exp098_stage0.json; do [ -e $f ] && stop "target $f already exists (stale-file guard)"; done
rm -f $DONE; DONE_FILE=$DONE nohup zsh tools/freepct_guard.sh $$ $L 'exp098_free3|exp098_3w|watchdog\.py' > /dev/null 2>&1 &
echo "=== run_098s0b start $(date '+%F %T') PID $$; freepct_guard $!" >> $L
gate() { while true; do f=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}')
  (( f >= 50 )) && { echo "=== GATE $1 $(date '+%F %T'): free ${f}% -> LAUNCH (pgate next)" >> $L; break; }; echo "=== GATE $1 $(date '+%F %T'): WAIT free ${f}%" >> $L; sleep 300; done; }
run() { local T=$1 P_=$2; shift 2; [ -e $D/$T.wd.log ] && stop "log tag $T already used"; gate $T; echo "=== $T start $(date '+%F %T') args: $*" >> $L
  pgate_run $D/$T.wd.log "nice -n 10 $P_ tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $P_ -u -W ignore $*"
  local rc=$?; echo "=== $T rc $rc $(date '+%F %T') $(grep -h '# exit' $D/$T.wd.log | tail -1)" >> $L; return $rc; }
preflight start pre
run e98_free3 $PY exp098_free3.py || stop "free(3,4)/free(6,8) on the venv rc != 0"
for f in $FB/free_W3_P4_box4_c2.json $FB/free_W6_P8_box8_c2.json; do echo "=== free cache $f ($(shasum -a 256 $f | cut -c1-16)): $(cat $f)" >> $L; done
preflight analysis ana
run e98_stage0_r2 $PYA exp098_3w.py S0 || stop "exp098_3w S0 rc != 0 (control FAIL or KA FAIL)"
echo "=== run_098s0b complete $(date '+%F %T')" >> $L; touch $DONE
