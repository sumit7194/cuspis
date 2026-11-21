"""EXP-080 free-side calibration at L = infinity (continuous k): kappa_lat(W, r) = -W * [s(strip) - s(e1) - s(e2)],
s = S/L. Known answer 0.0396481. [model: Opus 5.5]"""
import time, numpy as np, sigma3d as S3
def kappa(W, r, nk=48):
    P = int(round(r * W)); Lx, Lt = W + 2 * P, 2 * P; tcut = P - 1
    cuts = {"strip": list(range(P, P + W)), "e1": list(range(P, Lx)), "e2": list(range(0, P + W))}
    s = {k: S3.FreeStripK(Lx, Lt, c, tcut, nk).S_per_L().real for k, c in cuts.items()}
    return -(s["strip"] - s["e1"] - s["e2"]) * W
for W in (2, 4, 8):
    for r in (2, 4, 8, 16, 32):
        if W * r > 128: continue
        t0 = time.time(); k = kappa(W, r)
        print(f"W={W} r={r}: kappa_lat(L=inf) = {k:.6f}  ratio {k/0.0396481:.4f}  [{time.time()-t0:.0f}s]", flush=True)
print("nk check W=4 r=8:", [round(kappa(4, 8, nk), 7) for nk in (32, 48, 72)])
