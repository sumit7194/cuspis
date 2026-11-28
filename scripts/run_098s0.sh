#!/bin/zsh
# EXP-098 stage 0 runner (registration notes/EXP-098_registration.md, 243b079 + amendment 1). Mac mini. [model: Opus 5.5]
# 1 BLAS thread, nice 10, gate free >= 50% + pgate, freepct_guard (pause-only), no-kill watchdog. No hard caps.
# Flags as for the stored k <= 2.5 routes: CUSPIS_081E and CUSPIS_087 unset. Routes and exp087_t0 on the project venv (as the stored routes);
# the analysis on the same python3 that ran its DRY. New checkpoints carry _098 / _098ka: no stored file can be overwritten.
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
unset CUSPIS_081E CUSPIS_087; source tools/pgate.sh
PY=../.venv/bin/python; PYA=/opt/homebrew/bin/python3; D=exp081d_results; L=$D/run_098s0.txt; DONE=$D/run_098s0.done
CKN() { echo $D/sigma_W$1_P$2_box$2_c2_cp12_sc3.0_dd0$3_ckpt.json; }
stop() { echo "=== STOP $(date '+%F %T'): $1 -> tell the Bridge" >> $L; touch $DONE; exit 1; }
for f in $(CKN 2 4 _098ka) $(CKN 3 4 _098) $(CKN 6 8 _098) $D/exp087_t0_W3P4.json $D/exp087_t0_W6P8.json $D/exp098_stage0.json; do
  [ -e $f ] && stop "target $f already exists (stale-file guard)"; done
rm -f $DONE; DONE_FILE=$DONE nohup zsh tools/freepct_guard.sh $$ $L 'exp081d_route|exp087_t0|exp098_3w|watchdog\.py' > /dev/null 2>&1 &
echo "=== run_098s0 start $(date '+%F %T') PID $$; freepct_guard $!; venv $($PY -c 'import sys,numpy;print(sys.version.split()[0],numpy.__version__)'); analysis $($PYA -c 'import sys,numpy;print(sys.version.split()[0],numpy.__version__)')" >> $L
gate() { while true; do f=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}')
  (( f >= 50 )) && { echo "=== GATE $1 $(date '+%F %T'): free ${f}% -> LAUNCH (pgate next)" >> $L; break; }; echo "=== GATE $1 $(date '+%F %T'): WAIT free ${f}%" >> $L; sleep 300; done; }
run() { local T=$1 P_=$2; shift 2; [ -e $D/$T.wd.log ] && stop "log tag $T already used"; gate $T; local t1=$(date +%s); echo "=== $T start $(date '+%F %T') args: $*" >> $L
  pgate_run $D/$T.wd.log "nice -n 10 $P_ tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $P_ -u -W ignore $*"
  local rc=$?; echo "=== $T rc $rc $(date '+%F %T') $(grep -h '# exit' $D/$T.wd.log | tail -1)" >> $L; return $rc; }
guard() { local ck=$1 t1=$2
  [ -e $ck ] && [ $(stat -f %m $ck) -ge $t1 ] && grep -q '"tsad"' $ck && grep -q '"n1c"' $ck && grep -q '"summary"' $ck || stop "checkpoint $ck stale or without tsad/n1c/summary"
  $PY -I -c "import json,sys; sys.path.insert(0,'.'); import exp081d_analyze as A; st=json.load(open('$ck')); m=[s for s,_ in A.nodes48() if f'g|{s:.15f}' not in st]; sys.exit(1 if (m or 't0' not in st) else 0)" || stop "not all 48 nodes (or no t0) in $ck"
  echo "=== stale-file guard PASS: $ck ($(shasum -a 256 $ck | cut -c1-16))" >> $L; }
t0of() { $PY -I -c "import json; print(repr(json.load(open('$1'))['t0']))"; }
# 1. KA-0: fresh W2P4 route vs the stored checkpoint, bitwise (t0, tsad, 48 g nodes, n1c arms)
T1=$(date +%s); run e98_ka_W2P4 $PY exp081d_route.py 2 4 4 --tag-suffix _098ka || stop "KA-0 route rc != 0"; guard $(CKN 2 4 _098ka) $T1
$PY -I - $(CKN 2 4 _098ka) $(CKN 2 4) >> $L 2>&1 <<'PYEOF' || stop "KA-0 NOT bitwise (find out why before anything else)"
import json, sys
a, b = json.load(open(sys.argv[1])), json.load(open(sys.argv[2])); keys = ["t0", "tsad"] + sorted(k for k in b if k.startswith("g|"))
bad = [k for k in keys if a.get(k) != b[k]] + ([] if a["n1c"]["arms"] == b["n1c"]["arms"] else ["n1c.arms"])
print(f"=== KA-0: {len(keys)} keys + n1c arms compared; mismatches {len(bad)} {bad[:5]} -> {'PASS (bitwise)' if not bad else 'FAIL'}"); sys.exit(1 if bad else 0)
PYEOF
# 2. W3P4 route + t0 fix
T1=$(date +%s); run e98_W3P4 $PY exp081d_route.py 3 4 4 --tag-suffix _098 || stop "route W3P4 rc != 0"; guard $(CKN 3 4 _098) $T1
run e98_t0_W3P4 $PY exp087_t0.py 3 4 $(t0of $(CKN 3 4 _098)) || stop "exp087_t0 W3P4 rc != 0"
# 3. W6P8 route + t0 fix
T1=$(date +%s); run e98_W6P8 $PY exp081d_route.py 6 8 8 --tag-suffix _098 || stop "route W6P8 rc != 0"; guard $(CKN 6 8 _098) $T1
run e98_t0_W6P8 $PY exp087_t0.py 6 8 $(t0of $(CKN 6 8 _098)) || stop "exp087_t0 W6P8 rc != 0"
# 4. analysis
run e98_stage0 $PYA exp098_3w.py S0 || stop "exp098_3w S0 rc != 0 (control FAIL or KA FAIL)"
echo "=== run_098s0 complete $(date '+%F %T')" >> $L; touch $DONE
