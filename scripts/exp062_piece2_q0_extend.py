"""EXP-062 piece (II)' table, q = 0 redo: the first table cut rho at 16, where the weighted MF integrand of dB'_0
(~ rho^3 e^{-rho/2}) was still 1.1e-4; the cut produced a ~1e-4/k tail that mimicked a non-decaying D~' (a false
'delta-piece'). Redo with rmax = 50 and 60 (nuisance pair) and report k^2 D~'_0(k). [model: Opus 5.5]"""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, mpc, legenp, re
from exp062_precheck_bubble import dBp
from exp062_piece2_table import rho_nodes, k_nodes
from exp059_stageA import Dt
kk, wk = k_nodes(); res = {}
Dt1 = np.array([float(re(Dt(mpf(k), mpf(0)))) for k in kk])
for rmax in (50.0, 60.0):
    t0 = time.time(); R, W = rho_nodes(rmax)
    vals = np.array([(lambda v1, v2: v1 + (v1 - v2) / 3)(dBp(0, r, 1e-3), dBp(0, r, 2e-3)) for r in R])
    Pm = np.array([[float(re(legenp(mpc(-0.5, k), 0, mp.cosh(mpf(r)), type=3))) for r in R] for k in kk])
    Bt = Pm @ (W * 2 * np.pi * np.sinh(R) * vals); res[rmax] = (Bt, -Dt1 ** 2 * Bt, R, vals)
    print(f"rmax={rmax}: weighted integrand at cut {vals[-1]*np.sinh(R[-1])*np.exp(-R[-1]/2):+.2e}; "
          f"k^2 D~'_0 at k=5,10,20,30,40: " + " ".join(f"{(res[rmax][1]*kk**2)[np.argmin(abs(kk-x))]:+.4e}" for x in (5, 10, 20, 30, 40))
          + f"  [{time.time()-t0:.0f}s]", flush=True)
d = np.max(np.abs(res[60.0][1] - res[50.0][1])); print(f"max |D~'_0(rmax 60) - D~'_0(rmax 50)| over k-grid: {d:.2e}", flush=True)
out = dict(np.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp062_piece2_table.npz")))
out["dBt_0"], out["Dp_0"] = res[60.0][0], res[60.0][1]; out["dBrho_0"] = np.stack([res[60.0][2], res[60.0][3]])
np.savez(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp062_piece2_table.npz"), **out)
print("table q=0 replaced by rmax=60 version", flush=True)
