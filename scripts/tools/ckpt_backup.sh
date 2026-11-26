#!/bin/zsh
# Local checkpoint backup for a long route (Bridge 2026-11-26, W6P12 power-cut plan). [model: Opus 5.5]
# Usage: ckpt_backup.sh CKPT BACKUP_DIR LOG ROOT_PID. Every INTERVAL s (default 1800): copy CKPT to BACKUP_DIR/<name>.tmp; the copy must equal
# the source's sha256, parse as JSON, and have a key count >= the last good copy's. Only then it replaces BACKUP_DIR/<name> (the last good copy).
# Otherwise it logs "BACKUP FAIL ..." and keeps the last good copy. It never opens values (key counts only), never writes CKPT, never signals.
# Exits after one final round when ROOT_PID is gone, or when DONE_FILE exists. Test hooks: INTERVAL, ONCE=1.
CK=$1; BK=$2; LOG=$3; ROOT=$4; INTERVAL=${INTERVAL:-1800}; PY=${PY:-python3}; mkdir -p $BK; N=$(basename $CK)
nkeys() { $PY -I -c "import json,sys; print(len(json.load(open(sys.argv[1]))))" "$1" 2>/dev/null; }
round() {
  [ -e $CK ] || { echo "=== BACKUP none $(date '+%F %T'): no checkpoint yet" >> $LOG; return 0; }
  local tmp=$BK/$N.tmp; cp -p $CK $tmp || { echo "=== BACKUP FAIL $(date '+%F %T'): copy failed (last good kept)" >> $LOG; return 1; }
  local a=$(shasum -a 256 $CK | cut -d' ' -f1) b=$(shasum -a 256 $tmp | cut -d' ' -f1)
  [ "$a" = "$b" ] || { echo "=== BACKUP FAIL $(date '+%F %T'): sha differs (rewritten mid-copy? last good kept)" >> $LOG; rm -f $tmp; return 1; }
  local n=$(nkeys $tmp); [ -z "$n" ] && { echo "=== BACKUP FAIL $(date '+%F %T'): does not parse (last good kept)" >> $LOG; rm -f $tmp; return 1; }
  local o=0; [ -e $BK/$N ] && o=$(nkeys $BK/$N); o=${o:-0}
  (( n >= o )) || { echo "=== BACKUP FAIL $(date '+%F %T'): key count fell $o -> $n (last good kept)" >> $LOG; rm -f $tmp; return 1; }
  mv $tmp $BK/$N; echo "=== BACKUP ok $(date '+%F %T'): sha ${b:0:12}, keys $o -> $n" >> $LOG; return 0; }
echo "=== ckpt_backup start $(date '+%F %T') PID $$ CK $CK INTERVAL $INTERVAL" >> $LOG
while true; do round
  [ "$ONCE" = 1 ] && exit 0
  if ! kill -0 $ROOT 2>/dev/null || { [ -n "$DONE_FILE" ] && [ -e "$DONE_FILE" ]; }; then round; echo "=== ckpt_backup end $(date '+%F %T')" >> $LOG; exit 0; fi
  sleep $INTERVAL; done
