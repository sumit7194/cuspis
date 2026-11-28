#!/bin/zsh
# EXP-100 part B runner (registration notes/EXP-100_registration.md 4dbbf5a + am. 1 d9edfa5 + am. 2; Bridge ruling (a), 2026-11-28). [model: Opus 5.5]
# A new file modelled on run_098s0.sh (that file is not edited). Mac mini, 1 BLAS thread per process, nice 10, gate free >= 50% + pgate per phase,
# freepct_guard (pause-only), no-kill watchdog per process. No hard caps. Node split 0:6 | 6:20 | 20:34 | 34:48 (part 0 also does t0 and tsad);
# each part has its OWN checkpoint (--tag-suffix), merged by exp100_merge.py, then the unsplit route runs the check stage on the merged file.
# Phases: 0 preflight | 1 KA split-vs-whole at W2P4 (STOP if not bitwise) | 2 B0 W4 + W2 whole, then their exp100_t0 |
#         3 B1 W4 parts x4 | 4 B1 W2 parts x4 + exp100_t0 B1 W4 | 5 merges; B1 W4 checks + B1 W2 checks + exp100_t0 B1 W2 | 6 exp100_B.py READ
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1
unset CUSPIS_081E CUSPIS_087; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; L=$D/run_100b.txt; DONE=$D/run_100b.done
SPLIT=(0:6 6:20 20:34 34:48)
GKA="--gL 5 --gR 5 --hT 4 --Ny 16"; GB0="--gL 8 --gR 8 --hT 4 --Ny 16"; GB1="--gL 16 --gR 16 --hT 8 --Ny 32"
CK() { echo $D/sigma_W$1_P4_box4_c2_cp12_sc3.0_dd0_gL$2_gR$2_hT$3_Ny$4$5_ckpt.json; }      # W g hT Ny suffix
stop() { echo "=== STOP $(date '+%F %T'): $1 -> tell the Bridge" >> $L; touch $DONE; exit 1; }
TAGS=(e100b_ka_p1 e100b_ka_p2 e100b_ka_p3 e100b_ka_p4 e100b_ka_chk e100b_B0W4 e100b_B0W2 e100b_t0_B0W4 e100b_t0_B0W2
      e100b_B1W4_p1 e100b_B1W4_p2 e100b_B1W4_p3 e100b_B1W4_p4 e100b_B1W2_p1 e100b_B1W2_p2 e100b_B1W2_p3 e100b_B1W2_p4
      e100b_t0_B1W4 e100b_t0_B1W2 e100b_B1W4_chk e100b_B1W2_chk e100b_read)
for t in $TAGS; do [ -e $D/$t.wd.log ] || [ -e $D/$t.out ] && stop "log tag $t already used (stale-file guard)"; done
for f in $D/sigma_W2_P4_box4_*_gL5_gR5_hT4_Ny16*_ckpt.json(N) $D/sigma_W[24]_P4_box4_*_gL8_gR8_hT4_Ny16*_ckpt.json(N) \
         $D/sigma_W[24]_P4_box4_*_gL16_gR16_hT8_Ny32*_ckpt.json(N) $D/exp100_t0_*.json(N) $D/exp100_B.json(N); do
  stop "target $f already exists (stale-file guard)"; done
rm -f $DONE; DONE_FILE=$DONE nohup zsh tools/freepct_guard.sh $$ $L 'exp100_route|exp100_t0|watchdog\.py' > /dev/null 2>&1 &
echo "=== run_100b start $(date '+%F %T') PID $$; freepct_guard $!; venv $($PY -c 'import sys,numpy,scipy;print(sys.version.split()[0],numpy.__version__,scipy.__version__)')" >> $L
gate() { while true; do f=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}')
  (( f >= 50 )) && { echo "=== GATE $1 $(date '+%F %T'): free ${f}% -> LAUNCH (pgate next)" >> $L; break; }; echo "=== GATE $1 $(date '+%F %T'): WAIT free ${f}%" >> $L; sleep 300; done; }
job() { local T=$1; shift; echo "=== $T start $(date '+%F %T') args: $*" >> $L
  pgate_run $D/$T.wd.log "nice -n 10 $PY tools/watchdog.py --interval 10 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore $*"
  local rc=$?; echo "=== $T rc $rc $(date '+%F %T') $(grep -h '# exit' $D/$T.wd.log | tail -1)" >> $L; return $rc; }
typeset -a PIDS NAMES
bgjob() { job "$@" & PIDS+=$!; NAMES+=$1; }
waitall() { local i rc bad=""; for i in {1..${#PIDS}}; do wait ${PIDS[$i]}; rc=$?; (( rc )) && bad="$bad ${NAMES[$i]}(rc $rc)"; done
  PIDS=(); NAMES=(); [ -z "$bad" ] || stop "$1:$bad"; }
guard() { local ck=$1 t1=$2
  [ -e $ck ] && [ $(stat -f %m $ck) -ge $t1 ] && grep -q '"tsad"' $ck && grep -q '"n1c"' $ck && grep -q '"summary"' $ck || stop "checkpoint $ck stale or without tsad/n1c/summary"
  $PY -I -c "import json,sys; sys.path.insert(0,'.'); import exp081d_analyze as A; st=json.load(open('$ck')); m=[s for s,_ in A.nodes48() if f'g|{s:.15f}' not in st]; sys.exit(1 if (m or 't0' not in st) else 0)" || stop "not all 48 nodes (or no t0) in $ck"
  echo "=== stale-file guard PASS: $ck ($(shasum -a 256 $ck | cut -c1-16))" >> $L; }
t0of() { $PY -I -c "import json; print(repr(json.load(open('$1'))['t0']))"; }
splitrun() { local W=$1 G=$2 pfx=$3 sfx=$4 i=1; for r in $SPLIT; do bgjob ${pfx}_p$i exp100_route.py $W 4 4 ${=G} --production-only --nodes $r --tag-suffix ${sfx}$((i-1)); i=$((i+1)); done; }
merge() { local out=$1; shift; $PY -I exp100_merge.py $out $* >> $L 2>&1 || stop "merge refused for $out"; }
# 0. preflight
$PY -I exp100_merge.py --selftest >> $L 2>&1 || stop "merge selftest FAILED"
$PY -I exp100_B.py DRY > $D/e100b_DRY_preflight.out 2>&1 || stop "exp100_B DRY FAILED"; echo "=== preflight PASS (merge selftest, exp100_B DRY)" >> $L
# 1. KA: split W2P4 at the convention-A geometry vs the stored whole checkpoint, bitwise
gate KA; T1=$(date +%s); splitrun 2 "$GKA" e100b_ka _kap; waitall "KA parts"
merge $(CK 2 5 4 16 _ka100) $(CK 2 5 4 16 _kap0) $(CK 2 5 4 16 _kap1) $(CK 2 5 4 16 _kap2) $(CK 2 5 4 16 _kap3)
job e100b_ka_chk exp100_route.py 2 4 4 ${=GKA} --tag-suffix _ka100 || stop "KA check stage rc != 0"; guard $(CK 2 5 4 16 _ka100) $T1
$PY -I exp100_B.py KA $(CK 2 5 4 16 _ka100) $D/sigma_W2_P4_box4_c2_cp12_sc3.0_dd0_ckpt.json >> $L 2>&1 || stop "KA split-vs-whole NOT bitwise (find out why before anything else)"
echo "=== KA PASS $(date '+%F %T')" >> $L
# 2. B0 (whole routes), then exp100_t0 at B0
gate B0; T1=$(date +%s); bgjob e100b_B0W4 exp100_route.py 4 4 4 ${=GB0}; bgjob e100b_B0W2 exp100_route.py 2 4 4 ${=GB0}; waitall "B0 routes"
guard $(CK 4 8 4 16) $T1; guard $(CK 2 8 4 16) $T1
bgjob e100b_t0_B0W4 exp100_t0.py 4 4 $(t0of $(CK 4 8 4 16)) 8 8 4 16; bgjob e100b_t0_B0W2 exp100_t0.py 2 4 $(t0of $(CK 2 8 4 16)) 8 8 4 16; waitall "B0 exp100_t0"
# 3. B1 W4 production parts
gate B1W4; T1=$(date +%s); splitrun 4 "$GB1" e100b_B1W4 _bp; waitall "B1 W4 parts"
# 4. B1 W2 production parts + exp100_t0 at B1 W4 (the route t0 is in part 0)
gate B1W2; splitrun 2 "$GB1" e100b_B1W2 _bp; bgjob e100b_t0_B1W4 exp100_t0.py 4 4 $(t0of $(CK 4 16 8 32 _bp0)) 16 16 8 32; waitall "B1 W2 parts / t0 B1 W4"
# 5. merges; check stages; exp100_t0 at B1 W2
merge $(CK 4 16 8 32 _100B) $(CK 4 16 8 32 _bp0) $(CK 4 16 8 32 _bp1) $(CK 4 16 8 32 _bp2) $(CK 4 16 8 32 _bp3)
merge $(CK 2 16 8 32 _100B) $(CK 2 16 8 32 _bp0) $(CK 2 16 8 32 _bp1) $(CK 2 16 8 32 _bp2) $(CK 2 16 8 32 _bp3)
gate checks; bgjob e100b_B1W4_chk exp100_route.py 4 4 4 ${=GB1} --tag-suffix _100B; bgjob e100b_B1W2_chk exp100_route.py 2 4 4 ${=GB1} --tag-suffix _100B
bgjob e100b_t0_B1W2 exp100_t0.py 2 4 $(t0of $(CK 2 16 8 32 _bp0)) 16 16 8 32; waitall "B1 checks / t0 B1 W2"
guard $(CK 4 16 8 32 _100B) $T1; guard $(CK 2 16 8 32 _100B) $T1
# 6. reading
job e100b_read exp100_B.py READ || stop "exp100_B READ rc != 0 (control FAIL)"
echo "=== run_100b complete $(date '+%F %T')" >> $L; touch $DONE
