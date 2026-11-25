"""EXP-087 check (b): at production geometries, (i) every cluster's nearest non-member / rc (must be > 1.5, else the fix refuses);
(ii) singleton poles whose nearest same-slice neighbour lies in [rad, 3 rad) (outside-contour leakage on the ORIGINAL radius-rad path). [model: Opus 5.5]"""
import sys, numpy as np
sys.path.insert(0, "/Users/sumit/Github/corner_function/scripts")
import sigma3d as S3
rad = 1e-5
for W, P in ((4, 8), (8, 8), (5, 10), (10, 10), (6, 12), (12, 12), (6, 6)):
    Wb, Ny = P, 4 * P; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; idx = lambda x, t: x * Lt + t
    worst_cl, near_single, ncl = np.inf, [], 0
    for p in range(Ny // 2 + 1):
        sl = S3.Slice(Lx, Lt, 2 - 2 * np.cos(2 * np.pi * p / Ny), list(range(x0, x0 + W)), P - 1, idx)
        s = sorted(v for v in sl.s if v <= 3.0); allv = sorted(sl.s)
        for c in S3.clusters_087(sl.s, rad, 3.0):
            ncl += 1; rc = 0.5 * (c[-1] - c[0]) + rad; cen = 0.5 * (c[0] + c[-1])
            others = [v for v in allv if v not in c]; d = min(abs(v - cen) for v in others) if others else np.inf; worst_cl = min(worst_cl, d / rc)
        cm = {v for c in S3.clusters_087(sl.s, rad, 3.0) for v in c}
        for v in s:
            if v in cm: continue
            nb = min([abs(v - u) for u in allv if u != v] + [np.inf])
            if nb < 3 * rad: near_single.append((p, round(v, 4), f"{nb/rad:.2f} rad"))
    print(f"W{W}P{P}: clusters {ncl}; min (nearest non-member / rc) = {worst_cl:.1f} (refusal if <= 1.5); singletons with a neighbour in [rad, 3 rad): {near_single if near_single else 'none'}")
