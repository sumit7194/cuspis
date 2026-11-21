"""EXP-066 check of Neon T25 (blind BIE; unverified) against the CH05 route (own code).
(1) Shape: Delta C_BIE(w) / Int_w^inf bhat u  must be constant in w (CH05 fixes the shape, scale beta free).
(2) Absolute, cross channel: e(w) = (1/(16 pi a(1-a))) Int_w^inf (h + u^2) dt (no free scale) vs E_BIE(w).
BIE numbers transcribed from neon_work/dkappa/T25_summary.md (a = 0.3, 0.2, 0.4). [model: Opus 5.5]"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exp063_precheck_ratio as RR
BIE = {0.3: {3.0: (-0.0000462, 3.17e-5), 1.0: (-0.006392, 0.005125), 0.3: (-0.064878, 0.071568), 0.1: (-0.207750, 0.34842),
             0.03: (-0.510839, 1.48534), 0.01: (-1.00630, 5.0449)},
       0.2: {0.3: (-0.045439, 0.058770), 0.1: (-0.136563, 0.29817), 0.03: (-0.304101, 1.31041), 0.01: (-0.535003, 4.5374)},
       0.4: {0.3: (-0.085564, 0.078401), 0.1: (-0.30115, 0.37362), 0.03: (-0.84638, 1.56916), 0.01: (-1.92856, 5.2813)}}
for a, tab in BIE.items():
    sol = RR.run(a, False, t0=16.0, t1=5e-3)
    ss = np.geomspace(5e-3, 16.0, 40001); bu = []; hu = []
    for s in ss:
        u, v, H, lbr, lbi, _, _ = sol.sol(s); b = np.exp(lbr + 1j * lbi) * np.exp(-s) * s ** -1.5
        bu.append((b * u).real); hu.append(H / s ** 2 + u * u)
    bu, hu = np.array(bu), np.array(hu)
    cb = np.concatenate([[0], np.cumsum(0.5 * (bu[1:] + bu[:-1]) * np.diff(ss))]); tb = cb[-1] - cb
    ch = np.concatenate([[0], np.cumsum(0.5 * (hu[1:] + hu[:-1]) * np.diff(ss))]); th = ch[-1] - ch
    ks = []
    for w, (dC, E) in sorted(tab.items()):
        i = np.argmin(abs(ss - w)); k = dC / tb[i]; ks.append(k)
        e = th[i] / (16 * np.pi * a * (1 - a))
        print(f"a={a} w={w}: k = DeltaC_BIE/Int bhat u = {k:+.6f}   |  e_CH05 {e:.6f}  E_BIE {E:.6f}  rel {e/E-1:+.1e}")
    ks = np.array(ks); print(f"  a={a}: k spread (max-min)/mean = {(ks.max()-ks.min())/abs(ks.mean()):.1e}")
