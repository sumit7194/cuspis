import sys, math, time
sys.path.insert(0, '.')
import mpmath as mp, exp004_mp as em
def stages(M, a=0.25, iters=8):
    mp.mp.dps = int(30 + 9*M); N = int(2*round((1.6*M + 8)/2)); g = None; Ncur = 4; out = []
    while True:
        d, nr = em.series_start_mp(M, a, Ncur, g, iters=iters, verbose=False, branch=-1)
        out.append((Ncur, float(abs(nr))))
        if Ncur >= N: break
        Ncur = min(N, Ncur + 4); g = tuple(d[k] for k in ['H','X1','X2','b','c','u','be1','be2','B1','B2','B12'])
    return out
import numpy as np
Mprod = float(np.sqrt(0.25 + (4 + 0.5*11*(np.polynomial.legendre.leggauss(24)[0][20]+1))**2))
for M in (13.5798909621 - 1e-4, Mprod):
    t0 = time.time(); st = stages(M); sig = math.exp(-2*math.pi*M)
    print(f"M={M:.10f}: " + "  ".join(f"N{n}:{r:.0e}" for n, r in st) + f"   final/signal {st[-1][1]/sig:.0e}  [{time.time()-t0:.0f}s]", flush=True)
