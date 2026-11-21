"""EXP-081 pre-check: engine vs honest integer-n (n = 2, 3) for the EDGE-to-wall cut geometry (few poles found by the solver)
and for the strip, at W=2 r=2 Ny=8. [model: Opus 5.5]"""
import numpy as np, sigma3d as S3
W, r = 2, 2; P = r * W; Lx, Lt = W + 2 * P, 2 * P
for name, cut in (("strip", list(range(P, P + W))), ("edge", list(range(P, Lx)))):
    S = S3.Strip3D(Lx, Lt, 8, cut, P - 1)
    for n in (2, 3):
        Gs = [[s.G(kk / n) for kk in range(n)] for s in S.sl]; worst = 0
        for q in range(n):
            F = {}
            for kk in range(n):
                c = S.conv([Gs[p][kk] for p in range(8)], [Gs[p][(q - kk) % n] for p in range(8)])
                for k in range(8): F[k] = F.get(k, 0) + c[k]
            Bh = [(2.0 / (n * 8)) * F[k] for k in range(8)]
            Be = S.inner_beta0(n) if q == 0 else S.inner(n, q / n)
            worst = max(worst, max(np.abs(Be[k] - Bh[k]).max() / np.abs(Bh[k]).max() for k in range(8)))
        print(f"{name}: poles/slice {[len(s.s) for s in S.sl]}  n={n}: max rel |engine - honest| = {worst:.1e}", flush=True)
