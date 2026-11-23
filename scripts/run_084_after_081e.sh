#!/bin/zsh
# EXP-084 k = 2.5 (registered 6e3ecfa): attempt 1 was killed by the registered 0.8 GB cap at 1.10 GB (still rising) beside the W6 route,
# so per MEM it queues after 081e. Waits for the 081e runner to exit, then runs ALONE (cap 3.0 GB, soft 2.0, pressure-stop). [model: Opus 5.5]
cd "$(dirname "$0")"; export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1; source tools/pgate.sh; D=exp081d_results
while ps -p ${RUNNER_081E:-66664} >/dev/null; do sleep 300; done; echo "=== 081e runner ended $(date '+%F %T')"
pgate_run $D/exp084_k25.wd.log "nice -n 12 ../.venv/bin/python tools/watchdog.py --min-disk-gb 5 --stop-on-pressure-warn --cap-gb 3.0 --soft-cap-gb 2.0 --log $D/exp084_k25.wd.log --stdout $D/exp084_k25.out -- ../.venv/bin/python -u -W ignore exp084_run.py 2.5"
echo "=== EXP-084 k2.5 + reading complete rc $? $(date)"
