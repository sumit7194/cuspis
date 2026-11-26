#!/bin/zsh
# EXP-093 (P-1) periodic pull-back of the Air's W2P8 route checkpoint (Bridge - claude personal, 2026-11-26 ~12:35). [model: Opus 5.5]
# Every INTERVAL s: remote sha256 -> scp into a staging file -> local sha256 must equal the remote one -> JSON must parse ->
# the number of 'g|' nodes must be >= the last good copy's. Only then the staging file replaces the last good copy
# (exp081d_results/air_pull/<NAME>). On any failure: log 'PULL FAIL ...' and keep the last good copy. READ-ONLY on the Air:
# it never writes, moves or deletes anything there. Report-only: never signals any process. No caps.
# Ends after one final pull once the Air log shows the W2P8 route done or a STOP (or air_run_093.done exists).
# Test hooks: NAME (checkpoint file name), INTERVAL, ONCE=1 (one round then exit), LOG, PDIR (local pull directory).
setopt PIPE_FAIL
cd "$(dirname "$0")/.."; D=exp081d_results; P=${PDIR:-$D/air_pull}; mkdir -p $P/staging
NAME=${NAME:-sigma_W2_P8_box8_c2_cp12_sc3.0_dd0_ckpt.json}; INTERVAL=${INTERVAL:-1800}; L=${LOG:-$D/air_pull_093.txt}
R=GitHub/fleet-air/corner_function/scripts/exp081d_results; SSH=(ssh -o BatchMode=yes -o ConnectTimeout=15 air)
PY=../.venv/bin/python
nodes() { $PY -I -c "import json,sys; j=json.load(open(sys.argv[1])); print(sum(1 for k in j if k.startswith('g|')))" "$1" 2>/dev/null; }
round() {
  local rs=$($SSH "shasum -a 256 $R/$NAME 2>/dev/null | cut -d' ' -f1")
  [ -z "$rs" ] && { echo "=== PULL none $(date '+%F %T'): no $NAME on the Air yet" >> $L; return 0; }
  local tmp=$P/staging/$NAME.tmp; rm -f $tmp
  scp -q -o BatchMode=yes -o ConnectTimeout=15 air:$R/$NAME $tmp 2>/dev/null || { echo "=== PULL FAIL $(date '+%F %T'): scp failed (last good kept)" >> $L; return 1; }
  local ls=$(shasum -a 256 $tmp | cut -d' ' -f1)
  [ "$ls" = "$rs" ] || { echo "=== PULL FAIL $(date '+%F %T'): sha mismatch remote ${rs:0:12} local ${ls:0:12} (rewritten mid-copy? last good kept)" >> $L; return 1; }
  local n=$(nodes $tmp); [ -z "$n" ] && { echo "=== PULL FAIL $(date '+%F %T'): does not parse as JSON (last good kept)" >> $L; return 1; }
  local o=0; [ -e $P/$NAME ] && o=$(nodes $P/$NAME); o=${o:-0}
  (( n >= o )) || { echo "=== PULL FAIL $(date '+%F %T'): node count fell $o -> $n (last good kept)" >> $L; return 1; }
  [ -e $P/$NAME ] && [ "$(shasum -a 256 $P/$NAME | cut -d' ' -f1)" = "$ls" ] && { echo "=== PULL same $(date '+%F %T'): ${ls:0:12}, $n nodes (unchanged)" >> $L; rm -f $tmp; return 0; }
  mv $tmp $P/$NAME; echo "=== PULL ok $(date '+%F %T'): sha ${ls:0:12} both ends, parses, nodes $o -> $n; last good updated" >> $L; return 0; }
echo "=== pull_air_093 start $(date '+%F %T') PID $$ NAME $NAME INTERVAL $INTERVAL" >> $L
while true; do round
  [ "$ONCE" = 1 ] && exit 0
  fin=$($SSH "grep -c -E 'W2P8 route done|=== STOP' $R/air_run_093.txt 2>/dev/null; ls $R/air_run_093.done 2>/dev/null | wc -l" | tr '\n' ' ')
  nd=$(echo "$fin" | awk '{print $1 + $2}')
  if [ "${nd:-0}" -gt 0 ]; then round; echo "=== pull_air_093 end $(date '+%F %T'): Air run finished or stopped; final pull done" >> $L; exit 0; fi
  sleep $INTERVAL; done
