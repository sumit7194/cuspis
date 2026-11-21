"""EXP-080 free-side calibration scan (known answer kappa_free = 0.0396481 per real scalar): kappa_lat(W, r = pad/W,
Ny/W) = -W/Ny * [S(strip) - S(edge1) - S(edge2)] on the Dirichlet-box 3D lattice. Explores the box/finite-L systematics
before any sigma registration. [model: Opus 5.5]"""
import time, numpy as np, sigma3d as S3
def kappa(W, r, ny):
    P = int(round(r * W)); Lx, Lt = W + 2 * P, 2 * P; tcut = P - 1; Ny = int(ny * W)
    cuts = {"strip": list(range(P, P + W)), "e1": list(range(P, Lx)), "e2": list(range(0, P + W))}
    S = {k: S3.FreeStrip(Lx, Lt, Ny, c, tcut).S().real for k, c in cuts.items()}
    return -(S["strip"] - S["e1"] - S["e2"]) * W / Ny
for W in (4, 8):
    for r in (1, 2, 4, 8):
        for ny in (4, 8):
            t0 = time.time(); k = kappa(W, r, ny)
            print(f"W={W} r={r} Ny/W={ny}: kappa_lat = {k:.6f}  (ratio to 0.0396481: {k/0.0396481:.3f})  [{time.time()-t0:.0f}s]", flush=True)
