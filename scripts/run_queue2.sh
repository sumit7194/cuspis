#!/bin/zsh
# Queue part 2 (2026-11-23 ~17:35; no-kill policy). EXP-084b n = 4 FIRST (Bridge: before the routes), then the route-free 081e pre-steps
# (F.3 W10, pre-check, CEN', F.3 W6 reference check), then HOLD: no route starts until the Bridge rules on the EXP-085 post-firing
# amendment and gives the route go. 081e commands as in run_081e.sh; watchdog --pause-on-red --inform-pressure (no memory kill). [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results
job() { local name=$1 soft=$2; shift 2; echo "=== $name start $(date '+%H:%M:%S')"
  pgate_run $D/$name.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --soft-cap-gb $soft --log $D/$name.wd.log --stdout $D/$name.out -- $PY -u -W ignore $*"; local rc=$?
  echo "=== $name end $(date '+%H:%M:%S') rc $rc"; tail -1 $D/$name.wd.log; return $rc; }
stop() { echo "=== STOP: $1 $(date '+%F %T')"; exit 1; }
unset CUSPIS_081E
job exp084b_n4 6.0 exp084b_run.py 4; echo "=== EXP-084b rc $?"
export CUSPIS_081E=1
job e_bw_W10 3.5 exp081d_route.py 10 10 10 --production-only --nodes 47:48 --tag-suffix _081e_bw || stop "bw W10 run failed"
$PY exp081e_bitwise.py 10 10 10 $D/sigma_W10_P10_box10_c2_cp12_sc3.0_dd0_ckpt.json | tee $D/exp081e_bw_W10_result.txt || stop "F.3 W10 not bitwise identical"
job e_precheck 2.0 exp081e_precheck.py || stop "pre-check (plants/invariance)"
job e_census_W12 2.0 exp081d_census.py 12:12:12 || stop "census job failed"
$PY -c "import json,sys; d=json.load(open('$D/census_12-12-12.json'))['W12P12b12']; miss=[x['p'] for x in d['flagged'] if not x['touch']]; print('CEN prime: resolved MISS slices', miss, '; TOUCH slices', [x['p'] for x in d['flagged'] if x['touch']]); sys.exit(1 if miss else 0)" || stop "CEN' resolved MISS at W12"
REF6=$D/sigma_W6_P12_box12_c2_cp12_sc3.0_dd0_ckpt.json
$PY -c "import json,sys; sys.exit(0 if any(k.startswith('g|5.97') for k in json.load(open('$REF6'))) else 1)" && echo "=== F.3 W6 reference present (bitwise step to run in the route runner)" || echo "=== F.3 W6 FAIL (HELD reference has no g; not run) -> W6 rerun under 081e" | tee $D/exp081e_bw_W6_result.txt
echo "=== HOLD before routes (awaiting Bridge: EXP-085 amendment ruling + route go) $(date '+%F %T')"
