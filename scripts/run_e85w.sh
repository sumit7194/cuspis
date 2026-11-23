#!/bin/zsh
# EXP-085w side job beside part 8 (registered 1272d17 + 4cc4f65): W4P4, then W2P4 with plant (c) at W4P4's argmax site.
# Continues only while measured peak < 0.5 GB (Bridge rule); else STOP. nice 12, no-kill. [model: Opus 5.5]
setopt PIPE_FAIL
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh
PY=../.venv/bin/python; D=exp081d_results
peak() { grep -h "# exit" $1 | tail -1 | sed -E 's/.*= ([0-9.]+) GB.*/\1/'; }
one() { T=e85w_W$1P$2; echo "=== $T start $(date '+%H:%M:%S')"
  pgate_run $D/$T.wd.log "nice -n 12 $PY tools/watchdog.py --min-disk-gb 5 --pause-on-red --inform-pressure --cap-gb 15 --soft-cap-gb 0.5 --log $D/$T.wd.log --stdout $D/$T.out -- $PY -u -W ignore exp085w_diag.py $*"
  rc=$?; pk=$(peak $D/$T.wd.log); echo "=== $T rc $rc peak ${pk:-?} GB $(date '+%F %T')"
  [ -n "$pk" ] && (( pk >= 0.5 )) && { echo "=== STOP: $T peak $pk GB >= 0.5 GB (beside-part-8 rule)"; exit 2; }; return 0; }
one 4 4
SITE=$($PY -c "import json; print(json.load(open('$D/exp085w/W4P4.json'))['top5'][0][0])" 2>/dev/null) || { echo "=== STOP: no W4P4.json"; exit 1; }
one 2 4 $SITE
echo "=== EXP-085w W4P4 + W2P4 done $(date '+%F %T') (W3P6/W6P6: decided after reading)"
