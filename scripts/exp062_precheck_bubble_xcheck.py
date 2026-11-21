"""EXP-062 pre-check 6: two implementations of the physical bubble at n != 1 (input of piece (II)').
(A) tau-space: MF of B_reg^(n)(q/n; rho) + 4 (1/(2 pi n)) [g_{a_n} - g_0](rho) g_{q/n}(rho)  (nu = 0 reference + alternate zero mode;
    no a_n^2 for m != 0, i.e. linearised); (B) EXP-056 frequency-space mode-sum instrument (nu_m = sqrt(m^2/n^2 + a_n^2), alternate
    zero mode, M = 200 and 400 for its truncation tail). Expected: A - B = O(a_n^2) (scales ~ (n-1)^2), not O(n-1). [model: Opus 5.5]"""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, mpc, legenp
from exp062_precheck_bubble import Breg
from exp062_piece2_table import rho_nodes
import exp056_sigma_kernel as K
import exp053_cone_gap as G

def tau_route(n, q, ks, a_n, rmax=30.0):
    R, W = rho_nodes(rmax)
    B = np.array([Breg(q, r, n) for r in R])
    zm = 4 / (2 * np.pi * n) * (K.g(abs(a_n) if a_n >= 0 else 0.0, R) * 0)   # placeholder (overwritten below)
    ga = np.array([float(mp.re(mp.legenq(mpf(a_n) - 0.5, 0, mp.cosh(mpf(r)), type=3))) / (2 * np.pi) for r in R])
    g0 = K.g(0.0, R); gq = K.g(q / n, R)
    zm = 4 / (2 * np.pi * n) * (ga - g0) * gq
    out = []
    for k in ks:
        P = np.array([float(legenp(mpc(-0.5, k), 0, mp.cosh(mpf(r)), type=3).real) for r in R])
        out.append(np.sum(W * 2 * np.pi * np.sinh(R) * P * (B + zm)))
    return np.array(out)

def inst_route(n, q, ks, a_n, M):
    R, Wt = K.rho_grid_fine(400.0); Ws, sig, _ = K.weight_scaled(n, a_n, q, R, Wt, M=M)
    return np.array([K.Bks(R, Ws, sig, k).real for k in ks])

if __name__ == "__main__":
    ks = (0.5, 2.0, 5.0)
    for n in (1.05, 1.02):
        a_n = float(G.root(mpf(n))); t0 = time.time()
        A = tau_route(n, 1, ks, a_n); B2 = inst_route(n, 1, ks, a_n, 200); B4 = inst_route(n, 1, ks, a_n, 400)
        for k, x, y2, y4 in zip(ks, A, B2, B4):
            print(f"n={n} (a_n={a_n:+.6f}, a_n^2={a_n**2:.2e}) q=1 k={k}: tau-space {x:.10f}  instrument M=200 {y2:.10f}  M=400 {y4:.10f}  "
                  f"rel(A vs M=400) {x/y4-1:+.2e}  [{time.time()-t0:.0f}s]", flush=True)
