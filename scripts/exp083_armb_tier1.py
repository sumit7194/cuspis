"""EXP-083 R3' arm (b) Tier-1 build controls (no comparison with production T_sad): (i) continued single-factor average at integer n
vs the direct (1/n) sum_j G(j/n) diagonal, sigma = 0 and a seeded random sigma, s_cut = inf and 3; (ii) sigma_1; (iii) sigma_n at
n = 2, 3, 4 from the continued gap (target 'direct') vs the honest n-sheet saddle (exp083_honest.Geom.saddle). Usage: W P [model: Opus 5.5]"""
import sys, time, numpy as np
from exp083_honest import Geom
import exp083_armb as AB
W, P = int(sys.argv[1]), int(sys.argv[2]); g = Geom(W, P); T0 = time.time(); rng = np.random.default_rng(83)
def log(*a): print(f"[{time.time()-T0:6.0f}s]", *a, flush=True)
for lab, sig in (("sigma=0", None), ("sigma=rand(1e-2)", 1e-2 * rng.standard_normal(g.N))):
    S = AB.strip_sigma(g, sig); ns = sorted({len(sl.s) for sl in S.sl}); smin = min(min(sl.s) for sl in S.sl if sl.s)
    for sc in (np.inf, 3.0):
        worst = []
        for n in range(1, 7):
            d = max(np.abs(AB.avg_diag(S.sl[p], n, s_cut=sc) - AB.direct_avg_diag(S.sl[p], n)).max() for p in range(g.Ny // 2 + 1))
            worst.append(d)
        log(f"(i) W{W}P{P} {lab} poles/slice {ns} s_min {smin:.3f} s_cut {sc}: max|A_n cont - direct| n=1..6: " + " ".join(f"{x:.1e}" for x in worst))
for tg in ("self", "direct"):
    gp = AB.Gap(g, target=tg); F0, im = gp.F(np.zeros(g.N), 1.0); log(f"(ii) target {tg}: |F(sigma=0; n=1)| = {np.abs(F0).max():.1e}")
gp = AB.Gap(g, target="direct"); J = None
for n in (2, 3, 4):
    sc, info = gp.solve(float(n), J=J); J = info["J"]
    sh, it = g.saddle(n)
    log(f"(iii) n={n}: continued gap |F| {info['F']:.1e} in {info['it']} it (imag {info['imag']:.1e}); honest saddle it {it}; "
        f"max|sigma_cont - sigma_honest| = {np.abs(sc - sh).max():.1e} (|sigma| {np.abs(sh).max():.2e}); nfev {gp.nfev}")
