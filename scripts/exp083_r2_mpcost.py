"""EXP-083 R2 cost dry run (mpmath, 50 digits): time one twisted N x N inverse, one N x N Hadamard multiply-accumulate, one N x N
determinant, at P = 2 (N = 32) and P = 4 (N = 96); extrapolate the cost per n of the sector Q(n) (arm a; arm b adds ~3 inverse sweeps
with a float64 Jacobian). Peak RSS from the watchdog. [model: Opus 5.5]"""
import time, resource, numpy as np, mpmath as mp
from exp083_honest import Geom
import exp083_sector as SEC
mp.mp.dps = 50
for P in (2, 4):
    g = Geom(2, P); N, Ny = g.N, g.Ny
    H = (np.diag(np.full(N, 4.0 + g.m2(1))) - g.A).astype(complex); z = np.exp(2j * np.pi * 0.3)
    for (l, u) in g.links: H[u, l] = -z; H[l, u] = -1 / z
    Hm = mp.matrix(H.tolist()); t0 = time.time(); G = mp.inverse(Hm); ti = time.time() - t0
    acc = mp.matrix(N, N); t0 = time.time()
    for i in range(N):
        for j in range(N): acc[i, j] += G[i, j] * G[i, j]
    th = time.time() - t0; t0 = time.time(); d = mp.det(G); td = time.time() - t0
    for n in ((8, 16) if P == 2 else (6, 12)):
        inv = (Ny // 2 + 1) * n; had = n * Ny * Ny * n; dets = n * Ny
        tot = inv * ti + had * th + dets * td
        print(f"P={P} (N={N}, Ny={Ny}): inverse {ti:.2f}s, Hadamard-acc {th:.3f}s, det {td:.2f}s -> per n={n}: {inv} inv + {had} Had + {dets} det "
              f"= {tot/60:.1f} min (arm a); arm b ~ +{3*inv*ti/60:.1f} min", flush=True)
print(f"maxrss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB", flush=True)
