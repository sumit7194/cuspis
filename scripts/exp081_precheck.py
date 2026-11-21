"""EXP-081 pre-checks (before registration; free side and memory only, no sigma S_conn computed):
(1) Ny choice: free kappa_lat at Ny = c * (2P) for c in {1, 2, 4} vs L = infinity, W in {2, 3}, r in {2..6}.
(2) edge reflection: free S(e1) == S(e2) (mirror geometry).
(3) sigma memory/time: one beta at W=2, r=6, Ny = 4*(2P) = 96, measured peak. [model: Opus 5.5]"""
import time, resource, numpy as np, sigma3d as S3
def geom(W, r):
    P = int(round(r * W)); Lx, Lt = W + 2 * P, 2 * P
    return P, Lx, Lt, P - 1, {"strip": list(range(P, P + W)), "e1": list(range(P, Lx)), "e2": list(range(0, P + W))}
for W, rs in ((2, (2, 3, 4, 5, 6)), (3, (2, 3, 4))):
    for r in rs:
        P, Lx, Lt, tc, cuts = geom(W, r)
        kinf = -W * (lambda s: s["strip"] - s["e1"] - s["e2"])({k: S3.FreeStripK(Lx, Lt, c, tc).S_per_L().real for k, c in cuts.items()})
        row = []
        for c in (1, 2, 4):
            Ny = int(c * 2 * P); s = {k: S3.FreeStrip(Lx, Lt, Ny, cc, tc).S().real / Ny for k, cc in cuts.items()}
            row.append((c, -W * (s["strip"] - s["e1"] - s["e2"]), abs(s["e1"] - s["e2"])))
        print(f"W={W} r={r} (2P={2*P}): L=inf kappa_lat {kinf:.6f} | " + "  ".join(f"c={c}: {k:.6f} ({k/kinf-1:+.2%}), |e1-e2|/L {d:.0e}" for c, k, d in row), flush=True)
t0 = time.time(); P, Lx, Lt, tc, cuts = geom(2, 6); S = S3.Strip3D(Lx, Lt, 96, cuts["strip"], tc); tb = time.time() - t0
t0 = time.time(); B = S.inner(1.0, 0.5 + 0.5j); del B
print(f"sigma W=2 r=6 Ny=96 (N2D={Lx*Lt}): build {tb:.0f}s, one beta {time.time()-t0:.0f}s, maxrss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB", flush=True)
