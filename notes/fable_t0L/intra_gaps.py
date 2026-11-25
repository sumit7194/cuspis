"""Fable side check (UNVERIFIED): pole pairs of the SAME y-slice closer than the inner_beta0 contour radius (rad = 1e-5) but not
merged (merge tolerance 1e-7).  In inner_beta0's two-tag branch the contour of radius rad around one of them encloses the other
too, and the other has its own entry: both residues would be counted twice.  Poles from sigma3d.Slice (QEP), s <= 3.  [model: Fable 5.2]"""
import sys, os, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import sigma3d as S3
w = lambda s: 2 * np.pi * s * np.exp(-2 * np.pi * s) / (1 - np.exp(-2 * np.pi * s)) ** 2
for W, P in [(2, 4), (4, 4), (5, 5), (3, 6), (6, 6), (7, 7), (4, 8), (8, 8), (9, 9), (5, 10), (10, 10), (6, 12), (12, 12)]:
    Lx, Lt = 3 * P, 2 * P; x0 = P + (P - W) // 2; Ny = 4 * P; idx = lambda x, t: x * Lt + t; out = []; gmin = 1.0
    for p in range(Ny // 2 + 1):
        sl = S3.Slice(Lx, Lt, 2 - 2 * np.cos(2 * np.pi * p / Ny), list(range(x0, x0 + W)), P - 1, idx)
        s = np.array(sorted(v for v in sl.s if v <= 3.0))
        if len(s) > 1:
            g = np.diff(s); gmin = min(gmin, float(g.min()))
            for i in np.where(g < 1e-4)[0]: out.append((float(g[i]), float(s[i]), p, float(w(s[i]))))
    print(f"W{W:<2d}P{P:<2d} min intra-slice pole gap {gmin:.2e};  pairs with gap < 1e-4 (gap, s, slice p, dn-weight w(s)): "
          f"{[(f'{g:.1e}', round(s, 4), p, f'{ww:.1e}') for g, s, p, ww in sorted(out)]}", flush=True)
