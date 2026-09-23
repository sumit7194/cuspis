#!/bin/sh
# EXP-028 production run for one twist a, under the bridge's limits (2026-09-24):
#   launch only if free swap >= 1024 MB and free disk >= 8 GB; watchdog: tree <= 1.5 GB, disk >= 8 GB, free swap >= 512 MB.
set -e
A=$1; MODE=diracA$A; W=6
cd "$(dirname "$0")"
SWAP=$(sysctl vm.swapusage | sed -E 's/.*free = ([0-9.]+)M.*/\1/')
DISK=$(df -g . | awk 'NR==2{print $4}')
echo "pre-launch a=$A: free swap ${SWAP} MB, free disk ${DISK} GB"
awk -v s="$SWAP" 'BEGIN{exit !(s>=1024)}' || { echo "STOP: free swap ${SWAP} MB < 1024 MB"; exit 3; }
[ "$DISK" -ge 8 ] || { echo "STOP: free disk ${DISK} GB < 8 GB"; exit 4; }
python3 tools/watchdog.py --log exp028_${MODE}.wd.log --stdout exp028_${MODE}.out --cap-gb 1.5 --min-disk-gb 8 --min-swap-mb 512 --interval 5 \
  -- ../.venv/bin/python exp004_prod.py $MODE 24 24 15.0 1 0 $W
