"""Design test for EXP-081b (free side only; known answer 0.0396481): kappa from a PAIR of strips in the same box (no
edge configurations): kappa_lat = -[s(W1) - s(W2)] / (1/W1 - 1/W2), s = S/L at L = infinity, strips centred in a
Dirichlet box of half-width P (Lx = 2P + Wmax, Lt = 2P). Box ladder P. [model: Opus 5.5]"""
import time, numpy as np, sigma3d as S3
def s_strip(W, P, Wmax):
    Lx, Lt = 2 * P + Wmax, 2 * P; x0 = P + (Wmax - W) // 2
    return S3.FreeStripK(Lx, Lt, list(range(x0, x0 + W)), P - 1).S_per_L().real
for (W1, W2) in ((2, 4), (2, 3), (3, 6)):
    for P in (8, 16, 32, 64):
        t0 = time.time(); Wm = max(W1, W2)
        k = -(s_strip(W1, P, Wm) - s_strip(W2, P, Wm)) / (1 / W1 - 1 / W2)
        print(f"W1={W1} W2={W2} P={P} (P/W2={P/W2:.1f}): kappa_lat = {k:.6f}  ratio {k/0.0396481:.4f}  [{time.time()-t0:.0f}s]", flush=True)
