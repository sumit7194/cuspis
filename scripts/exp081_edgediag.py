"""EXP-081a edge-configuration diagnosis (anomalies: non-monotonic edge t0 at r=4; edge g(s) breakdown at s >~ 2).
(1) integer-n engine vs honest for the EDGE config at r=4 (Ny=32), n=2,3. (2) G(alpha) accuracy at large Im alpha: Woodbury
vs direct dense inverse, edge slice p=0, alpha = 1/2 + i s for s = 1, 2, 3, 4. (3) pole sets of the edge slices at r=3,4,5
(look for close pairs that were merged/missed). [model: Opus 5.5]"""
import numpy as np, sigma3d as S3
def geom(W, r):
    P = int(round(r * W)); Lx, Lt = W + 2 * P, 2 * P; return P, Lx, Lt, P - 1, list(range(P, Lx))
P, Lx, Lt, tc, cut = geom(2, 4); S = S3.Strip3D(Lx, Lt, 4 * P, cut, tc); Ny = 4 * P
for n in (2, 3):
    Gs = [[s.G(kk / n) for kk in range(n)] for s in S.sl]; worst = {}
    for q in range(n):
        F = {}
        for kk in range(n):
            c = S.conv([Gs[p][kk] for p in range(Ny)], [Gs[p][(q - kk) % n] for p in range(Ny)])
            for k in range(Ny): F[k] = F.get(k, 0) + c[k]
        Bh = [(2.0 / (n * Ny)) * F[k] for k in range(Ny)]
        Be = S.inner_beta0(n) if q == 0 else S.inner(n, q / n)
        worst[q] = max(np.abs(Be[k] - Bh[k]).max() / np.abs(Bh[k]).max() for k in range(Ny))
    print(f"(1) edge r=4 n={n}: max rel |engine - honest| by q: {{{', '.join(f'{q}: {v:.1e}' for q, v in worst.items())}}}", flush=True)
sl = S.sl[0]
for s in (1, 2, 3, 4):
    a = 0.5 + 1j * s; z = np.exp(2j * np.pi * a)
    Gw = sl.G(a)
    H = np.linalg.inv(sl.G0).astype(complex)                          # H0
    for (l, u) in sl.links: H[u, l] += -(z - 1); H[l, u] += -(1 / z - 1)
    Gd = np.linalg.inv(H)
    print(f"(2) edge slice p=0, alpha=1/2+{s}i: |z|={abs(z):.1e}  max|G_woodbury - G_direct|/max|G_direct| = {np.abs(Gw-Gd).max()/np.abs(Gd).max():.1e}  max|G| = {np.abs(Gd).max():.2e}", flush=True)
for r in (3, 4, 5):
    P, Lx, Lt, tc, cut = geom(2, r); S2 = S3.Strip3D(Lx, Lt, 4 * P, cut, tc)
    print(f"(3) edge r={r}: poles (slices 0,1,mid): {[np.round(S2.sl[p].s, 5).tolist() for p in (0, 1, 2 * P)]}", flush=True)
