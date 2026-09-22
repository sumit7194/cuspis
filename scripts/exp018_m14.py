"""EXP-018: one-node diagnosis of the M >= 14 failure (TODO: 'garbage at 120-125 digits, not precision').
Node: M = 14.0189302751, t = 0.0287 (eehp grid), stored value is wrong (F(5 deg) negative).
One variable per variant, everything else at the production values (dps = 50 + 5M = 120, N = 1.6M + 8 -> 30, delta0 = 0.01/M).
Variants: baseline (must reproduce the stored node), N = 40, delta0 = 0.004/M, dps = 170.  Referee: agreement between
variants plus smoothness against the good neighbours M = 13.58 and 14.38 at the same t."""
import sys, math, time, io, contextlib
sys.path.insert(0, __file__.rsplit('/',1)[0])
import mpmath as mp
import exp004_mp as em
from exp004_prod import XG, branch_by_continuation
from multiprocessing import Pool
M = 14.018930275131; T = 0.028696208617
import glob, json
f = glob.glob('exp004_nodes/eehp_M14.0189*_t0.0287*.json')[0]; node = json.load(open(f)); M, T = node['M'], node['t']
N0 = int(2*round((1.6*M + 8)/2)); D0 = 0.01/M; P0 = int(50 + 5*M)
def run(v):
    name, N, d0, dps = v
    em.set_prec = (lambda MM, _p=dps: setattr(mp.mp, 'dps', _p)); mp.mp.dps = dps
    a = complex(0.5, -T)
    with contextlib.redirect_stdout(io.StringIO()):
        sign, guess, flips = branch_by_continuation(M, T, N, 0.5, 'ee')
    err = io.StringIO(); t0 = time.time()
    try:
        with contextlib.redirect_stderr(err):
            out, d = em.integrate_mp(M, a, math.radians(4), XG, N=N, delta0=d0, branch=sign, guess=guess, verbose=True)
        F = [complex(out[XG[i]]).real for i in (0, 2, 7, 13)]
        return name, time.time()-t0, F, complex(d['H'][1]).real, err.getvalue().strip()[-160:]
    except Exception as e:
        return name, time.time()-t0, None, None, repr(e)[:160]
if __name__ == '__main__':
    print(f"node M={M:.6f} t={T:.6f}; production N={N0} delta0={D0:.2e} dps={P0}; stored F5={node['F_re'][0]:+.4e} F15={node['F_re'][2]:+.4e} F45={node['F_re'][7]:+.4e} F90={node['F_re'][13]:+.4e} H1={node['H1']:+.3e}", flush=True)
    V = [("baseline", N0, D0, P0), ("N=40", 40, D0, P0), ("delta0/2.5", N0, 0.004/M, P0), ("dps=170", N0, D0, 170)]
    with Pool(4) as pool:
        for name, secs, F, H1, diag in pool.imap_unordered(run, V):
            if F is None: print(f"{name:12s} {secs:6.0f}s FAILED: {diag}", flush=True)
            else: print(f"{name:12s} {secs:6.0f}s F5={F[0]:+.4e} F15={F[1]:+.4e} F45={F[2]:+.4e} F90={F[3]:+.4e} H1={H1:+.3e} | {diag}", flush=True)
    print("DIAG DONE", flush=True)
