"""EXP-062 piece (II)' table: dB~'(k, q) = MF[dB'_q](k) for q = 0..Qmax on a k-grid, and D~'(k,q) = -D~_1(k,q)^2 dB~'(k,q).
alpha-independent; saved to exp062_piece2_table.npz. dB'_q from exp062_precheck_bubble (Richardson over steps 1e-3, 2e-3).
[model: Opus 5.5]"""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, mpc, legenp, re
from exp062_precheck_bubble import dBp
from exp059_stageA import Dt

def rho_nodes(rmax, nper=16):
    edges = [0.0, 0.05, 0.2, 0.5, 1.0] + list(np.arange(2.0, rmax + 1e-9, 1.0))
    xs, ws = np.polynomial.legendre.leggauss(nper); R = []; W = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        R.append(0.5 * (hi - lo) * xs + 0.5 * (hi + lo)); W.append(0.5 * (hi - lo) * ws)
    return np.concatenate(R), np.concatenate(W)

def k_nodes(K=40.0, width=2.0, nper=12):
    xs, ws = np.polynomial.legendre.leggauss(nper); kk = []; ww = []
    for lo in np.arange(0, K, width):
        kk.append(0.5 * width * xs + lo + 0.5 * width); ww.append(0.5 * width * ws)
    return np.concatenate(kk), np.concatenate(ww)

if __name__ == "__main__":
    Qmax = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    kk, wk = k_nodes(); out = {"k": kk, "wk": wk}
    for q in range(0, Qmax + 1):
        t0 = time.time(); rmax = float(min(16, max(6, int(36 / (q + 1)))))
        R, W = rho_nodes(rmax)
        vals = np.array([(lambda v1, v2: v1 + (v1 - v2) / 3)(dBp(q, r, 1e-3), dBp(q, r, 2e-3)) for r in R])
        Pm = np.array([[float(re(legenp(mpc(-0.5, k), 0, mp.cosh(mpf(r)), type=3))) for r in R] for k in kk])
        Bt = Pm @ (W * 2 * np.pi * np.sinh(R) * vals)
        Dt1 = np.array([float(re(Dt(mpf(k), mpf(q)))) for k in kk])
        out[f"dBt_{q}"] = Bt; out[f"Dp_{q}"] = -Dt1 ** 2 * Bt; out[f"dBrho_{q}"] = np.stack([R, vals])
        print(f"q={q}: rmax {rmax}, {len(R)} rho nodes; dB'~(k) at k=0,5,20,40: {Bt[0]:+.4e} {Bt[np.argmin(abs(kk-5))]:+.4e} "
              f"{Bt[np.argmin(abs(kk-20))]:+.4e} {Bt[-1]:+.4e};  D~' at same k: {out[f'Dp_{q}'][0]:+.4e} "
              f"{out[f'Dp_{q}'][np.argmin(abs(kk-5))]:+.4e} {out[f'Dp_{q}'][np.argmin(abs(kk-20))]:+.4e} {out[f'Dp_{q}'][-1]:+.4e}  [{time.time()-t0:.0f}s]", flush=True)
        np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp062_piece2_table.npz"), **out)
