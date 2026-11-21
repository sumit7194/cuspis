"""EXP-083 R2 cost dry run with Arb (python-flint 0.9.0), prec 400 bits (~120 digits): twisted N x N inverse, Hadamard
multiply-accumulate, determinant at P = 2 (N 32) and P = 4 (N 96); per-n extrapolation of the sector Q(n). [model: Opus 5.5]"""
import time, resource, numpy as np
from flint import acb_mat, acb, arb, ctx
from exp083_honest import Geom
ctx.prec = 400
def Htw(g, p, q, n):
    N = g.N; m2 = 2 - 2 * arb.cos_pi(arb(2 * p) / g.Ny); z = acb.exp_pi_i(acb(2 * q) / n)
    rows = [[acb(0)] * N for _ in range(N)]
    for i in range(N): rows[i][i] = acb(4) + m2
    for i, j in zip(*np.nonzero(g.A)): rows[i][j] = acb(-1)
    for (l, u) in g.links: rows[u][l] = -z; rows[l][u] = -1 / z
    return acb_mat(rows)
for P in (2, 4):
    g = Geom(2, P); N, Ny = g.N, g.Ny; H = Htw(g, 1, 1, 3)
    t0 = time.time(); G = H.inv(); ti = time.time() - t0
    t0 = time.time(); acc = [[G[i, j] * G[i, j] for j in range(N)] for i in range(N)]; th = time.time() - t0
    t0 = time.time(); d = G.det(); td = time.time() - t0
    rad = max(float(G[i, j].rad()) for i in range(N) for j in range(N)) if N <= 40 else float(G[0, 0].rad())
    for n in ((16, 40) if P == 2 else (12, 24)):
        inv = (Ny // 2 + 1) * n; had = n * Ny * Ny * n; dets = n * Ny; tot = inv * ti + had * th + dets * td
        print(f"P={P} (N={N}): inv {ti:.3f}s, Hadamard {th:.4f}s, det {td:.3f}s (ball radius {rad:.1e}) -> per n={n}: {tot/60:.2f} min (arm a)", flush=True)
print(f"maxrss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB")
