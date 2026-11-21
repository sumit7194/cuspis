"""EXP-080 pre-checks for Stage P1 (3D slice layer, sigma3d.py), before registration. Tiny lattice 6x4 slice, Ny=4, W=2.
(a1) slice decomposition at n=1: logdet(2 G o G) on the 3D lattice == sum_k logdet B1_k.
(a2) honest slice-sector sums == directly glued 3D replica manifold, n = 2, 3.
(a3) engine continuation at integer n: inner(n, q/n) and inner_beta0(n) == honest slice-sector matrices.
(b)  gauge: interior cut vs exterior cut (complementary links, reversed twist) give the same Q(n) and route-(i) Q'(1).
(c)  timing/memory of one beta evaluation at W=4 (20x16, Ny=16) and W=6 (30x24, Ny=32). [model: Opus 5.5]"""
import time, resource, numpy as np, sigma3d as S3
Lx, Lt, Ny, cutx, tcut = 6, 4, 4, [2, 3], 1
S = S3.Strip3D(Lx, Lt, Ny, cutx, tcut)
print("slice poles s(p):", [np.round(s.s, 6).tolist() for s in S.sl], flush=True)
# (a1)
N3 = Lx * Lt * Ny
H = np.zeros((N3, N3)); I = lambda x, t, y: (x * Lt + t) * Ny + y
for x in range(Lx):
    for t in range(Lt):
        for y in range(Ny):
            i = I(x, t, y); H[i, i] = 6.0
            if x + 1 < Lx: j = I(x + 1, t, y); H[i, j] = H[j, i] = -1.0
            if t + 1 < Lt: j = I(x, t + 1, y); H[i, j] = H[j, i] = -1.0
            j = I(x, t, (y + 1) % Ny); H[i, j] -= 1.0; H[j, i] -= 1.0
G = np.linalg.inv(H); ld3 = S3.logdet(2 * G * G).real; lds = sum(S3.logdet(b) for b in S.B1()).real
print(f"(a1) logdet 3D {ld3:.10f}  sum_k slices {lds:.10f}  diff {abs(ld3-lds):.1e}", flush=True)
# (a2)
for n in (2, 3):
    hs = S3.honest_slices(S, n).real; hd = S3.honest_3d_replica(Lx, Lt, Ny, cutx, tcut, n)
    print(f"(a2) n={n}: honest slices {hs:.10f}  direct 3D replica {hd:.10f}  diff {abs(hs-hd):.1e}", flush=True)
# (a3)
for n in (2, 3):
    Gs = [[s.G(kk / n) for kk in range(n)] for s in S.sl]
    worst = 0
    for q in range(n):
        F = {}
        for kk in range(n):
            c = S.conv([Gs[p][kk] for p in range(Ny)], [Gs[p][(q - kk) % n] for p in range(Ny)])
            for k in range(Ny): F[k] = F.get(k, 0) + c[k]
        Bh = [(2.0 / (n * Ny)) * F[k] for k in range(Ny)]
        Be = S.inner_beta0(n) if q == 0 else S.inner(n, q / n)
        worst = max(worst, max(np.abs(Be[k] - Bh[k]).max() / np.abs(Bh[k]).max() for k in range(Ny)))
    print(f"(a3) n={n}: max rel |engine - honest| over q, k = {worst:.1e}", flush=True)
# (b) gauge: exterior cut = complementary links with reversed twist; Q(2) and route-(i) Q'(1)
class Rev(S3.Strip3D):
    def __init__(self, *a):
        super().__init__(*a)
        for s in self.sl:                          # reverse twist: G(a) -> G(-a); poles s unchanged, residues swap
            g0 = s.G; s.G = (lambda g: (lambda a: g(-a)))(g0); s.Rp, s.Rm = [-r for r in s.Rm], [-r for r in s.Rp]
ext = [x for x in range(Lx) if x not in cutx]
Se = Rev(Lx, Lt, Ny, ext, tcut)
q2i, q2e = S3.honest_slices(S, 2).real, S3.honest_slices(Se, 2).real
t0 = time.time(); dqi, t0i, _ = S3.route_i(S); dqe, t0e, _ = S3.route_i(Se); el = time.time() - t0
print(f"(b) Q(2) interior {q2i:.10f} exterior {q2e:.10f} diff {abs(q2i-q2e):.1e};  Q'(1) interior {dqi.real:.10f} exterior {dqe.real:.10f} diff {abs(dqi-dqe):.1e}  [{el:.0f}s]", flush=True)
# (a4) integer-n engine check at production sizes (poles with large s may be dropped by the solver: must be negligible)
for (W, Lx2, Lt2, Ny2) in ((4, 20, 16, 16), (6, 30, 24, 8)):
    x1 = (Lx2 - W) // 2; S2 = S3.Strip3D(Lx2, Lt2, Ny2, list(range(x1, x1 + W)), Lt2 // 2 - 1)
    n = 2; Gs = [[s.G(kk / n) for kk in range(n)] for s in S2.sl]; worst = 0
    for q in range(n):
        F = {}
        for kk in range(n):
            c = S2.conv([Gs[p][kk] for p in range(Ny2)], [Gs[p][(q - kk) % n] for p in range(Ny2)])
            for k in range(Ny2): F[k] = F.get(k, 0) + c[k]
        Bh = [(2.0 / (n * Ny2)) * F[k] for k in range(Ny2)]
        Be = S2.inner_beta0(n) if q == 0 else S2.inner(n, q / n)
        worst = max(worst, max(np.abs(Be[k] - Bh[k]).max() / np.abs(Bh[k]).max() for k in range(Ny2)))
    print(f"(a4) W={W} {Lx2}x{Lt2} Ny={Ny2}: poles per slice {[len(s.s) for s in S2.sl][:6]}...; n=2 max rel |engine - honest| = {worst:.1e}", flush=True)
# (c) timing
for (W, Lx2, Lt2, Ny2) in ((4, 20, 16, 16), (6, 30, 24, 16)):
    x1 = (Lx2 - W) // 2; t0 = time.time()
    S2 = S3.Strip3D(Lx2, Lt2, Ny2, list(range(x1, x1 + W)), Lt2 // 2 - 1); tb = time.time() - t0
    t0 = time.time(); B = S2.inner(1.0, 0.5 + 0.5j); ti = time.time() - t0
    print(f"(c) W={W} slice {Lx2}x{Lt2} Ny={Ny2}: build {tb:.1f}s, one beta {ti:.1f}s, maxrss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB", flush=True)
