#!/bin/zsh
# Remaining queue under Sumit's no-kill policy (2026-11-23 17:1x, in this chat): soft caps and yellow/red pressure only INFORM;
# a job is SIGSTOPped only after 5 min of continuous red and resumed after 60 s green (watchdog --pause-on-red); disk floor still kills.
# Order: EXP-084 k=2.5 + reading -> EXP-085 (all stages) -> 081e: F.3 W10, pre-check, CEN', F.3 W6 (reference check), route W12, C1 W12,
# W6 rerun + C1 W6 if F.3 W6 fails. 081e commands as in run_081e.sh; only the watchdog mode differs (environment, not an amendment).
# F.3 W6: the HELD 081d W6 checkpoint has no g (route killed 3x), so the step is marked FAIL without running a 7 GB job that cannot pass.
# [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results
job() { local name=$1 soft=$2; shift 2; echo "=== $name start $(date '+%H:%M:%S')"
  pgate_run $D/$name.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --soft-cap-gb $soft --log $D/$name.wd.log --stdout $D/$name.out -- $PY -u -W ignore $*"; local rc=$?
  echo "=== $name end $(date '+%H:%M:%S') rc $rc"; tail -1 $D/$name.wd.log; return $rc; }
stop() { echo "=== STOP: $1 $(date '+%F %T')"; exit 1; }
while ps -p ${RUNNER_OLD:-75214} >/dev/null; do sleep 10; done; echo "=== old runner gone $(date '+%F %T')"
unset CUSPIS_081E
for f in exp084_k25.out exp084_k25.wd.log; do [ -e $D/$f ] && mv $D/$f $D/${f%.*}_attempt3_superseded.${f##*.}; done
job exp084_k25 4.0 exp084_run.py 2.5; echo "=== EXP-084 k2.5 + reading rc $?"
job exp085 3.0 exp085_run.py all; echo "=== EXP-085 rc $?"
export CUSPIS_081E=1
job e_bw_W10 3.5 exp081d_route.py 10 10 10 --production-only --nodes 47:48 --tag-suffix _081e_bw || stop "bw W10 run failed"
$PY exp081e_bitwise.py 10 10 10 $D/sigma_W10_P10_box10_c2_cp12_sc3.0_dd0_ckpt.json | tee $D/exp081e_bw_W10_result.txt || stop "F.3 W10 not bitwise identical"
job e_precheck 2.0 exp081e_precheck.py || stop "pre-check (plants/invariance)"
job e_census_W12 2.0 exp081d_census.py 12:12:12 || stop "census job failed"
$PY -c "import json,sys; d=json.load(open('$D/census_12-12-12.json'))['W12P12b12']; miss=[x['p'] for x in d['flagged'] if not x['touch']]; print('CEN prime: resolved MISS slices', miss, '; TOUCH slices', [x['p'] for x in d['flagged'] if x['touch']]); sys.exit(1 if miss else 0)" || stop "CEN' resolved MISS at W12"
REF6=$D/sigma_W6_P12_box12_c2_cp12_sc3.0_dd0_ckpt.json
if $PY -c "import json,sys; sys.exit(0 if any(k.startswith('g|5.97') for k in json.load(open('$REF6'))) else 1)"; then
  W6BW=ok; job e_bw_W6 8.0 exp081d_route.py 6 12 12 --production-only --nodes 47:48 --tag-suffix _081e_bw || stop "bw W6 run failed"
  $PY exp081e_bitwise.py 6 12 12 $REF6 | tee $D/exp081e_bw_W6_result.txt || W6BW=fail
else W6BW=fail; echo "=== F.3 W6 FAIL (HELD reference has no g; not run) -> W6 rerun under 081e after W12" | tee $D/exp081e_bw_W6_result.txt; fi
CK=$D/sigma_W12_P12_box12_c2_cp12_sc3.0_dd0_ckpt.json
[ -e $CK ] && stop "unsuffixed W12 checkpoint already exists before the 081e route ($CK)"
T_ROUTE=$(date +%s); echo "=== 081e route W12 start epoch $T_ROUTE"
job e_route_W12 8.0 exp081d_route.py 12 12 12 || stop "route W12 (gate fired or crash)"
[ -e $CK ] && [ $(stat -f %m $CK) -ge $T_ROUTE ] && grep -q '"tsad"' $CK || stop "W12 checkpoint missing, stale or without tsad"
echo "=== stale-file guard PASS: $CK"
job e_c1_W12 4.0 exp083_armb_c1.py 12 12 12 2 || stop "C1 W12"
if [ $W6BW = fail ]; then
  [ -e $REF6 ] && mv $REF6 ${REF6%.json}_HELD081d_dead.json
  T6=$(date +%s); job e_route_W6 8.0 exp081d_route.py 6 12 12 || stop "route W6 rerun"
  [ -e $REF6 ] && [ $(stat -f %m $REF6) -ge $T6 ] && grep -q '"tsad"' $REF6 || stop "W6 checkpoint missing, stale or without tsad"
  job e_c1_W6 4.0 exp083_armb_c1.py 6 12 12 2 || stop "C1 W6"
fi
echo "=== queue complete $(date)"
