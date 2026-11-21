"""EXP-081c pre-registration: condition number of H(alpha) at the largest |Im alpha| used by each N1'''c checkpoint node of
W8P8 box8 (matrix property only; no g, S or R). Sets which nodes the Step-0 1e-12 tolerance can apply to. [model: Opus 5.5]"""
import numpy as np, sigma3d as S3
P, W, Wb = 8, 8, 8; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = 4 * P
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0)
smax_pole = max(s for p in range(Ny) for s in S.sl[p].s if s <= 3.0)
for s in (0.937383295744266, 1.974126375751365, 2.986170475685039, 3.94825275150273, 5.05174724849727):
    a = 0.5 + 1j * (s + smax_pole); worst = 0
    for p in (0, Ny // 4, Ny // 2):
        sl = S.sl[p]; H = np.linalg.inv(sl.G0).astype(complex); z = np.exp(2j * np.pi * a)
        for (l, u) in sl.links: H[u, l] += -(z - 1); H[l, u] += -(1 / z - 1)
        worst = max(worst, np.linalg.cond(H))
    print(f"node s={s:.3f}: max Im alpha = {s + smax_pole:.3f}; cond(H) over p in (0, Ny/4, Ny/2) = {worst:.1e}; cond*eps = {worst*1.1e-16:.1e}", flush=True)
