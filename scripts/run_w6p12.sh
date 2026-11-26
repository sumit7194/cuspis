#!/bin/zsh
# EXP-081e / EXP-090 k = 3 input: the W6P12 route RERUN, exactly as registered in run_081e.sh line 42
#   exp081d_route.py 6 12 12 --tag-suffix _081e   (CUSPIS_081E=1, CUSPIS_087 unset; same env as the W12 route, run_k3.sh / run_k3_resume.sh)
# Sumit YES via the Bridge 2026-11-26; launch only after the Bridge's OK on the launch note. [model: Opus 5.5]
# Gates (2026-11-24 list): >= 50 % free at launch, no other job of mine, fleet cores <= ncpu - 2, nice 12, inform-only watchdog (fixed TREE = MEM),
# pgate (pressure normal >= 300 s), freepct_guard v3 (PAUSE below 30 % free, resume at >= 40 %), pause-only peak hold COL=3 (TRUE) at HOLD_GB,
# no auto-resume (a hold firing = the memory model is wrong -> Bridge). 30-min verified checkpoint backup (tools/ckpt_backup.sh).
# Fresh start: STOP if the _081e checkpoint already exists. Power-cut resume: RESUME=1 SHA=<verified sha256 of the checkpoint> TAG=<new log tag>;
# the route skips every key already in the checkpoint. After the route: stale-file guard (mtime >= this start, t0, tsad, 48 nodes, n1c, summary).
# Blind rule (Bridge): k = 3 stays sealed. This runner logs rc, peak, wall and key counts only; it never prints a value from the checkpoint or .out.
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 CUSPIS_081E=1; unset CUSPIS_087; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results; L=$D/run_w6p12.txt; DONE=$D/run_w6p12.done; HOLD_GB=${HOLD_GB:-6.9}
CK=$D/sigma_W6_P12_box12_c2_cp12_sc3.0_dd0_081e_ckpt.json; T=${TAG:-e_route_W6_081e}; RX='exp081d_route\.py 6 12 12'
stop() { echo "=== STOP: $1 $(date '+%F %T')" >> $L; touch $DONE; exit 1; }
gate() { local name=$1 f o nc q m fl
  while true; do
    f=$(memory_pressure | awk -F': ' '/free percentage/{gsub("%","",$2); print int($2)}')
    o=$(pgrep -fl 'exp08[0-9][a-z0-9_]*\.py|exp09[0-9]|run_queue|run_e85' | grep -v "$$" | grep -vE 'run_w6p12|watchdog\.py|freepct_guard|peak_hold|ckpt_backup' | head -3 | tr '\n' ';')
    nc=$(sysctl -n hw.ncpu); q=$(pgrep -f 'hs_cover|mn_so_erep' | wc -l | tr -d ' ')
    m=$(pgrep -fl 'exp08[0-9][a-z0-9_]*\.py|exp09[0-9]' | grep -vE 'watchdog.py|freepct_guard|peak_hold|ckpt_backup' | wc -l | tr -d ' '); fl=$((q + m))
    if (( f >= 50 )) && [ -z "$o" ] && (( fl + 1 <= nc - ${RESERVE:-2} )); then
      echo "=== GATE $name $(date '+%F %T'): free ${f}% (>= 50), other jobs of mine: none, fleet ${fl} + 1 <= ${nc}-${RESERVE:-2} -> LAUNCH (pgate next)" >> $L; return 0; fi
    echo "=== GATE $name $(date '+%F %T'): WAIT free ${f}% others '${o}' fleet ${fl}+1 vs ${nc}-${RESERVE:-2}" >> $L; sleep 300
  done; }
peak() { grep -h "# exit" $1 | tail -1 | sed -E 's/.*PEAK tree footprint ([0-9.]+) GB.*/\1/'; }
wall() { grep -h "# exit" $1 | tail -1 | sed -E 's/.*wall ([0-9]+) s.*/\1/'; }
echo "=== run_w6p12 start $(date '+%F %T') PID $$ (RESUME=${RESUME:-0}, tag $T, hold ${HOLD_GB} GB true)" >> $L; rm -f $DONE
if [ "${RESUME:-0}" = 1 ]; then
  [ -n "$SHA" ] && [ "$(shasum -a 256 $CK | awk '{print $1}')" = "$SHA" ] || stop "RESUME: checkpoint sha256 differs from the verified one (or SHA not given)"
  echo "=== RESUME: checkpoint sha256 verified ($SHA)" >> $L
else
  [ -e $CK ] && stop "fresh start but the _081e W6 checkpoint already exists ($CK)"
fi
[ -e $D/$T.wd.log ] && stop "log tag $T already used (logs are never overwritten)"
DONE_FILE=$DONE nohup zsh tools/freepct_guard.sh $$ $L 'exp08[0-9]|exp09[0-9]|watchdog\.py' > /dev/null 2>&1 &
gate $T
COL=3 DT=10 DONE_FILE=$DONE nohup zsh tools/peak_hold.sh $$ $D/$T.wd.log $HOLD_GB $L "$RX" > /dev/null 2>&1 &
echo "=== PEAK HOLD armed $(date '+%F %T'): peak_hold PID $!, COL=3 (MEM = TRUE phys_footprint), ${HOLD_GB} GB, DT 10 s, argv '$RX'; pause-only, no auto-resume (Bridge)" >> $L
DONE_FILE=$DONE PY=$PY nohup zsh tools/ckpt_backup.sh $CK $D/ckpt_backup $L $$ > /dev/null 2>&1 &
echo "=== CKPT BACKUP armed $(date '+%F %T'): PID $! every 1800 s -> $D/ckpt_backup/ (sha + parse + key count)" >> $L
T_ROUTE=$(date +%s); echo "=== $T start $(date '+%F %T')" >> $L
pgate_run $D/$T.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore exp081d_route.py 6 12 12 --tag-suffix _081e"
rc=$?; echo "=== $T rc $rc wall $(wall $D/$T.wd.log) s peak $(peak $D/$T.wd.log) GB true $(date '+%F %T')" >> $L
(( rc == 0 )) || stop "route W6P12 rc $rc"
[ -e $CK ] && [ $(stat -f %m $CK) -ge $T_ROUTE ] && grep -q '"tsad"' $CK && grep -q '"n1c"' $CK && grep -q '"summary"' $CK || stop "W6 checkpoint stale, or without tsad/n1c/summary"
$PY -I -c "import json,sys; sys.path.insert(0,'.'); import exp081d_analyze as A; st=json.load(open('$CK')); m=[s for s,_ in A.nodes48() if f'g|{s:.15f}' not in st]; sys.exit(1 if (m or 't0' not in st) else 0)" || stop "not all 48 nodes (or no t0) in the W6 checkpoint"
echo "=== stale-file guard PASS: $CK ($(shasum -a 256 $CK | cut -c1-16)…); k = 3 stays SEALED until the Bridge says read" >> $L
touch $DONE
