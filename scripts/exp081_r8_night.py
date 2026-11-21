"""EXP-081a r = 8 night run (registered in report.md, cbd4278 + bf45871): W=2, r=8 (34x32 slice), Ny=64, saddle included,
sigma strip + edge via route_i_ckpt (per-beta checkpoints in exp081_ckpt/), free partner, results into exp081_cache.json.
Completion marker exp081_r8_STATUS.txt: RUNNING (start) -> FINISHED (all done) or CRASHED (python exception, with traceback).
A marker still saying RUNNING with no live process in the morning means the process was killed (e.g. by the OS).
Resume: rerun the same command; finished configurations and finished betas are skipped. [model: Opus 5.5]"""
import os, sys, time, traceback, datetime
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
MARK = os.path.join(HERE, "exp081_r8_STATUS.txt")
def mark(s):
    with open(MARK, "w") as f: f.write(f"{s}\n{datetime.datetime.now().isoformat()}\npid {os.getpid()}\n")
mark("RUNNING")
try:
    import exp081_run as R
    R.pressure_guard = lambda **kw: 100                      # night run: no pressure gating (per Sumit)
    for conf in ("strip", "edge"): R.free_S(2, 8, conf)
    for conf in ("strip", "edge"): R.sigma_S(2, 8, conf)
    kap8 = -2 * R.conn("free", 2, 8); dk8 = -2 * R.conn("sigma", 2, 8)
    with open(os.path.join(HERE, "exp081_r8_result.txt"), "w") as f:
        f.write(f"W=2 r=8 Ny=64: delta_kappa_lat = {dk8!r}\nkappa_lat = {kap8!r}\nR = {dk8 / kap8!r}\n")
    mark("FINISHED")
except BaseException:
    mark("CRASHED\n" + traceback.format_exc())
    raise
