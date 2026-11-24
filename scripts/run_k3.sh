#!/bin/zsh
# k = 3 window (Sumit's GO via the Bridge 2026-11-24): 085c GEOM W6P12, W12P12 (measure peaks), then 081e route W12 (registered 6686454 + am. 1/1b)
# and C1 W12. One job at a time; nice 12; inform-only watchdog (no kill; NOT run_081e.sh's --stop-on-pressure-warn); CUSPIS_081E=1 throughout.
# Gate before EVERY launch: free >= 50% AND nothing else of mine running AND fleet compute (quantum hs_cover/mn_so_erep + mine) + 1 <= ncpu - 2
# (Bridge rule: fleet jobs <= 8; the 2 free cores are Sumit's; a load gate would double-count him); pgate adds pressure-normal >= 300 s.
# Free-memory guard v2 (tested) pauses the job if free < 30% (60 s), resumes at >= 40% (120 s). Route timing line at the P^7 bracket 49 h (informational).
# 2 cores stay free (one job = one core). [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 CUSPIS_081E=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; L=$D/run_k3.txt
PAT='exp085c_run.py GEOM|exp081d_route.py 12 12 12|exp083_armb_c1.py 12 12 12'
gate() { local name=$1 f o
  while true; do
    f=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}')
    o=$(pgrep -fl 'exp08[0-9][a-z0-9_]*\.py|exp09[0-9]|run_queue|run_e85' | grep -v "$$" | grep -vE "run_k3" | head -3 | tr '\n' ';')
    nc=$(sysctl -n hw.ncpu); q=$(pgrep -f 'hs_cover|mn_so_erep' | wc -l | tr -d ' ')
    m=$(pgrep -fl 'exp08[0-9][a-z0-9_]*\.py|exp09[0-9]' | grep -v watchdog.py | wc -l | tr -d ' '); fl=$((q + m))
    if (( f >= 50 )) && [ -z "$o" ] && (( fl + 1 <= nc - 2 )); then echo "=== GATE $name $(date '+%F %T'): free ${f}% (>= 50), other jobs of mine: none, fleet ${fl} (quantum ${q} + mine ${m}) + 1 <= ${nc}-2 -> LAUNCH (pgate next)" >> $L; return 0; fi
    echo "=== GATE $name $(date '+%F %T'): WAIT free ${f}% others '${o}' fleet ${fl}+1 vs ${nc}-2" >> $L; sleep 300
  done; }
peak() { grep -h "# exit" $1 | tail -1 | sed -E 's/.*= ([0-9.]+) GB.*/\1/'; }
wall() { grep -h "# exit" $1 | tail -1 | sed -E 's/.*wall ([0-9]+) s.*/\1/'; }
job() { local T=$1; shift; gate $T; echo "=== $T start $(date '+%F %T')" >> $L
  pgate_run $D/$T.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore $*"
  local rc=$?; echo "=== $T rc $rc wall $(wall $D/$T.wd.log) s peak $(peak $D/$T.wd.log) GB $(date '+%F %T')" >> $L; return $rc; }
stop() { echo "=== STOP: $1 $(date '+%F %T')" >> $L; touch $D/run_k3.done; exit 1; }
rm -f $D/run_k3.done; DONE_FILE=$D/run_k3.done nohup zsh tools/freepct_guard.sh "$PAT" $L > /dev/null 2>&1 &
job e85c_G_W6P12 exp085c_run.py GEOM 6 12 || stop "GEOM W6P12"
job e85c_G_W12P12 exp085c_run.py GEOM 12 12 || stop "GEOM W12P12"
CK=$D/sigma_W12_P12_box12_c2_cp12_sc3.0_dd0_ckpt.json; [ -e $CK ] && stop "unsuffixed W12 checkpoint exists before the route ($CK)"
T_ROUTE=$(date +%s); echo "=== 081e route W12: start epoch $T_ROUTE; estimate ~39 h, P^7 bracket 49 h (176400 s)" >> $L
( while [ ! -e $D/run_k3.done ]; do sleep 600; grep -q "=== e_route_W12 rc" $L && exit 0
    (( $(date +%s) - T_ROUTE > 176400 )) && { echo "=== TIMING (bracket): route W12 still running after $(( ($(date +%s) - T_ROUTE)/3600 )) h > P^7 bracket 49 h; informational $(date '+%F %T')" >> $L; exit 0; }; done ) &
job e_route_W12 exp081d_route.py 12 12 12 || stop "route W12 (gate fired or crash)"
[ -e $CK ] && [ $(stat -f %m $CK) -ge $T_ROUTE ] && grep -q '"tsad"' $CK || stop "W12 checkpoint missing, stale or without tsad"
echo "=== stale-file guard PASS: $CK" >> $L
job e_c1_W12 exp083_armb_c1.py 12 12 12 2 || stop "C1 W12"
echo "=== k = 3 window complete $(date '+%F %T') (W6 rerun stays on HOLD)" >> $L; touch $D/run_k3.done
