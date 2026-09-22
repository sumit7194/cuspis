"""EXP-019: replay only the series-start N-continuation (no ODE integration) for the failing node and nearby masses."""
import sys, math, time
sys.path.insert(0, '.')
import mpmath as mp, exp004_mp as em
def stages(M, a=0.25, N=None, iters=8):
    mp.mp.dps = int(30 + 9*M)
    N = N or int(2*round((1.6*M + 8)/2)); g = None; Ncur = 4; out = []
    while True:
        d, nr = em.series_start_mp(M, a, Ncur, g, iters=iters, verbose=False, branch=-1)
        out.append((Ncur, float(abs(nr))))
        if Ncur >= N: break
        Ncur = min(N, Ncur + 4); g = tuple(d[k] for k in ['H','X1','X2','b','c','u','be1','be2','B1','B2','B12'])
    return out
M0 = 13.5798909621
for M in (M0, M0 - 1e-4, M0 + 1e-4, 13.0740794867, 14.0189302751):
    t0 = time.time(); st = stages(M); sig = math.exp(-2*math.pi*M)
    print(f"M={M:.7f}: " + "  ".join(f"N{n}:{r:.0e}" for n, r in st) + f"   final/signal {st[-1][1]/sig:.0e}  [{time.time()-t0:.0f}s]", flush=True)
t0 = time.time(); st = stages(M0, iters=30)
print(f"M={M0:.7f} iters=30: " + "  ".join(f"N{n}:{r:.0e}" for n, r in st) + f"   final/signal {st[-1][1]/math.exp(-2*math.pi*M0):.0e}  [{time.time()-t0:.0f}s]")
