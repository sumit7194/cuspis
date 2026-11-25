#!/bin/zsh
# DEPRECATED 2026-11-25 (Sumit's standing rule: NO job-ending caps): this runner passes kill-mode watchdog flags
# (--stop-on-pressure-warn / --pressure-stop-level). Convert to the no-kill watchdog before any reuse. Body kept for the record.
echo "DEPRECATED: $0 uses kill-mode flags; refusing to run (see header)" >&2; exit 2
# EXP-081e production runner (registration 6686454 + amendment 1; Bridge GO 2026-11-23). SERIAL, detached (PPID 1), nice 12, pgate,
# pressure-stop; soft caps WARN only. Every job runs with CUSPIS_081E=1 (patched pole selection).
# Waits for the 081d Stage-2 runner (W6 HELD route, then C1 W6) to end; the 081d guard stops it before its W12 route.
# Gate -> runner mapping (one row per line):
#   E plants P1-P7m + F.1/F.2      -> job precheck: exp081e_precheck.py exit 1 -> STOP
#   CEN' (W12, patched lists)       -> job census: any flagged slice with NO touch (a resolved MISS) -> STOP; TOUCH slices -> covered by WIND
#   F.3 bitwise W10                 -> job e_bw_W10 (alone, after the 081d runner) -> not identical -> STOP
#   F.3 bitwise W6                  -> job bw_W6 vs HELD checkpoint; FAIL -> W6 rerun under 081e queued after W12 (Bridge ruling), not a STOP
#   PB, WIND (production)           -> raised inside sigma3d._poles -> the route exits non-zero -> STOP
#   081d rows (planted eps, B2b, N1'''c, t0, residue, R1 cap) -> inside exp081d_route.py (as in 081d); C1 -> job c1_W12
#   check-in bound                  -> 90 h per route (report.md entry gives the start time)
# W12 route writes the UNSUFFIXED tag sigma_W12_P12_box12_c2_cp12_sc3.0_dd0 (exp083_armb_c1 looks it up by that name); no 081d file
# has that name (081d W12 files were _probe / _081e_bw only). [model: Opus 5.5]
setopt PIPE_FAIL   # without it, "check | tee ... || stop" takes tee's status and the F.3 STOP can never fire (found 2026-11-23 before launch)
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 CUSPIS_081E=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results
job() { local name=$1 cap=$2 soft=${SOFT:-}; shift 2; echo "=== $name start $(date '+%H:%M:%S')"
  pgate_run $D/$name.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --stop-on-pressure-warn --cap-gb $cap ${soft:+--soft-cap-gb $soft} --log $D/$name.wd.log --stdout $D/$name.out -- $PY -u -W ignore $*"; local rc=$?
  echo "=== $name end $(date '+%H:%M:%S') rc $rc"; tail -1 $D/$name.wd.log; return $rc; }
stop() { echo "=== 081e STOP: $1 $(date '+%F %T')"; exit 1; }
while ps -p ${RUNNER_081D:-46956} >/dev/null; do sleep 120; done; echo "=== 081d runner ended $(date '+%F %T')"
# F.3 W10 moved here (2026-11-23 16:22): run beside the 7 GB W6 route it caused yellow pressure and both were killed. Nothing runs beside a route.
SOFT=3.5 job e_bw_W10 5.0 exp081d_route.py 10 10 10 --production-only --nodes 47:48 --tag-suffix _081e_bw || stop "bw W10 run failed"
$PY exp081e_bitwise.py 10 10 10 $D/sigma_W10_P10_box10_c2_cp12_sc3.0_dd0_ckpt.json | tee $D/exp081e_bw_W10_result.txt || stop "F.3 W10 not bitwise identical"
SOFT=2.0 job e_precheck 3.0 exp081e_precheck.py || stop "pre-check (plants/invariance)"
SOFT=2.0 job e_census_W12 4.0 exp081d_census.py 12:12:12 || stop "census job failed"
$PY -c "import json,sys; d=json.load(open('$D/census_12-12-12.json'))['W12P12b12']; miss=[x['p'] for x in d['flagged'] if not x['touch']]; print('CEN prime: resolved MISS slices', miss, '; TOUCH slices', [x['p'] for x in d['flagged'] if x['touch']]); sys.exit(1 if miss else 0)" || stop "CEN' resolved MISS at W12"
W6BW=ok
SOFT=8.0 job e_bw_W6 11.0 exp081d_route.py 6 12 12 --production-only --nodes 47:48 --tag-suffix _081e_bw || stop "bw W6 run failed"
$PY exp081e_bitwise.py 6 12 12 $D/sigma_W6_P12_box12_c2_cp12_sc3.0_dd0_ckpt.json | tee $D/exp081e_bw_W6_result.txt || { W6BW=fail; echo "=== F.3 W6 FAIL -> W6 rerun under 081e after W12"; }
CK=$D/sigma_W12_P12_box12_c2_cp12_sc3.0_dd0_ckpt.json            # stale-file guard (Bridge, amendment 1b): C1 may only grade THIS run's file
[ -e $CK ] && stop "unsuffixed W12 checkpoint already exists before the 081e route ($CK)"
T_ROUTE=$(date +%s); echo "=== 081e route W12 start epoch $T_ROUTE"
SOFT=8.0 job e_route_W12 11.0 exp081d_route.py 12 12 12 || stop "route W12 (gate fired or crash)"
[ -e $CK ] && [ $(stat -f %m $CK) -ge $T_ROUTE ] && grep -q '"tsad"' $CK || stop "W12 checkpoint missing, stale (mtime < route start) or without tsad"
echo "=== stale-file guard PASS: $CK mtime $(stat -f %m $CK) >= route start $T_ROUTE"
SOFT=4.0 job e_c1_W12 8.0 exp083_armb_c1.py 12 12 12 2 || stop "C1 W12"
if [ $W6BW = fail ]; then SOFT=8.0 job e_route_W6 11.0 exp081d_route.py 6 12 12 --tag-suffix _081e || stop "route W6 rerun"; fi
echo "=== 081e production complete $(date)"
