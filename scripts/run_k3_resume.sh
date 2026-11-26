#!/bin/zsh
# RESUME of run_k3.sh after the 2026-11-26 06:52 power cut (Bridge: jobs that resume from a VERIFIED checkpoint may relaunch in their old slot).
# The W12 route checkpoint was verified at 08:5x (complete JSON, atomic writes, 47/48 nodes + t0 + tsad, all finite; 47 'done' lines in the log)
# and its sha256 is pinned below: if the file differs, STOP (no launch). Same command/env as run_k3 (CUSPIS_081E=1; exp081d_route.py 12 12 12),
# NEW log names (e_route_W12_r2.*) so the 33-h run's logs are kept. After the route: the run_k3 stale-file guard (mtime >= resume start, tsad,
# 48 nodes, n1c), then C1 W12 as registered. Logs to run_k3.txt (lineage) and touches run_k3.done (downstream runners unchanged). [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 CUSPIS_081E=1; unset CUSPIS_087; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; L=$D/run_k3.txt; CK=$D/sigma_W12_P12_box12_c2_cp12_sc3.0_dd0_ckpt.json
SHA=8359d46798d0062055abc7ac1d3fe574427b9b8b80ab08bc960bbbc1fd5e3af4
stop() { echo "=== STOP (resume): $1 $(date '+%F %T')" >> $L; touch $D/run_k3.done; exit 1; }
echo "=== RESUME after the 06:52 power cut $(date '+%F %T'): runner PID $$" >> $L
[ "$(shasum -a 256 $CK | awk '{print $1}')" = "$SHA" ] || stop "checkpoint sha256 differs from the verified one"
echo "=== checkpoint sha256 verified ($SHA)" >> $L; rm -f $D/run_k3.done
gate() { local f; while true; do f=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}')
  (( f >= 50 )) && { echo "=== GATE $1 $(date '+%F %T'): free ${f}% -> LAUNCH (pgate next)" >> $L; return; }; echo "=== GATE $1: WAIT free ${f}%" >> $L; sleep 300; done; }
peak() { grep -h "# exit" $1 | tail -1 | sed -E 's/.*= ([0-9.]+) GB.*/\1/'; }
job() { local T=$1; shift; gate $T; echo "=== $T start $(date '+%F %T')" >> $L
  pgate_run $D/$T.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore $*"
  local rc=$?; echo "=== $T rc $rc peak $(peak $D/$T.wd.log) GB $(date '+%F %T')" >> $L; return $rc; }
DONE_FILE=$D/run_k3.done nohup zsh tools/freepct_guard.sh $$ $L 'exp08[0-9]|exp09[0-9]|watchdog\.py' > /dev/null 2>&1 &
T_ROUTE=$(date +%s)
job e_route_W12_r2 exp081d_route.py 12 12 12 || stop "route W12 resume (rc != 0)"
[ -e $CK ] && [ $(stat -f %m $CK) -ge $T_ROUTE ] && grep -q '"tsad"' $CK && grep -q '"n1c"' $CK || stop "W12 checkpoint stale, or without tsad/n1c after the resume"
$PY -I -c "import json,sys; sys.path.insert(0,'.'); import exp081d_analyze as A; st=json.load(open('$CK')); m=[s for s,_ in A.nodes48() if f'g|{s:.15f}' not in st]; sys.exit(1 if m else 0)" || stop "not all 48 nodes in the checkpoint"
echo "=== stale-file guard PASS (resume): $CK" >> $L
job e_c1_W12 exp083_armb_c1.py 12 12 12 2 || stop "C1 W12"
echo "=== k = 3 window complete $(date '+%F %T') (W6 rerun stays on HOLD)" >> $L; touch $D/run_k3.done
