"""EXP-039 V3 diagnostic (after the V3 FAIL at 2.0e-6 vs 1e-6, run 2, 13:05 IST 2026-11-18).
Question: is the 2e-6 discrepancy between the 35-digit i_G and the EXP-038 double i_G (Delta = 0.6, eta = 1e-4, n_p = 32,
96 nodes) on the mp side or on the double side?  Per-node comparison of I_s (double vs dps 35 vs dps 50), weighted
contributions w*jac*I_s/pi, and the double noise floor estimate eps * S(G1 u G2) per node.  No gate or threshold is changed here."""
import numpy as np
from numpy.polynomial.legendre import leggauss
import exp035_cylinder_mi as e35
import exp039_mp_mi as e39

al, eta, n_p, nodes = 0.8, 1e-4, 32, 96
M, _ = e35.geometry(eta, n_p)
t, w = leggauss(nodes); t = 0.5 * (t + 1); w = 0.5 * w; S = t / (1 - t); J = 1 / (1 - t) ** 2
acc_d = np.zeros(2); acc_m = np.zeros(2); acc_50 = np.zeros(2)
print(f"M = {M}")
print(" k        s       w*jac/pi   I90_double     I90_mp35       I90_mp50     dcontrib90(d-m)  noise90   dcontrib180(d-m)")
for k, (s, wi, ji) in enumerate(zip(S, w, J)):
    x, p = e35.rows(al, s, M)
    d = e35.mi_both(x, p, n_p, M)
    m = np.array(e39.mi_mp(al, s, n_p, M, 35))
    m50 = np.array(e39.mi_mp(al, s, n_p, M, 50)) if k % 8 == 0 or s > 20 else m
    u = np.concatenate([np.arange(n_p), np.arange(n_p) + M // 4])
    blk = lambda row, idx: row[np.minimum(np.abs(idx[:, None] - idx[None, :]), M - np.abs(idx[:, None] - idx[None, :]))]
    Sab = e35.entropy(blk(x, u), blk(p, u))
    c = wi * ji / np.pi
    acc_d += c * d; acc_m += c * m; acc_50 += c * m50
    print(f"{k:2d} {s:10.4g} {c:11.4e} {d[0]:14.6e} {m[0]:14.6e} {m50[0]:14.6e} {c * (d[0] - m[0]):14.3e} {c * 2.2e-16 * Sab:10.2e} {c * (d[1] - m[1]):14.3e}")
print(f"sum double {acc_d}  mp35 {acc_m}  mp50(where computed, else mp35) {acc_50}")
print(f"rel (double/mp35 - 1): {acc_d / acc_m - 1}")
