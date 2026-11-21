"""Sealed-derivation check (b2): P2 sensitivity. Under P1+P2, vary the near-floor spectrum: (i) the round-off-floor modes
(lambda-1/4 <= 0) assigned lambda-1/4 = 1e-22 / 1e-30 instead of r = 0; (ii) every mode with lambda-1/4 < 1e-14 scaled x10 and x0.1.
Reports T0, T2 at z = 4, 8 and the z-dependence of each shift (what kappa sees)."""
import sys, os, runpy, numpy as np
g = runpy.run_path(os.path.join(os.path.dirname(__file__), "seal_b_lib.py"), init_globals={"ARGV": sys.argv})
P, LamArr, base_solve = g["P"], g["LamArr"], g["solve_q"]
def run(tag, mod):
    def sq(self, q, act_tol=0.0):
        d = base_solve(self, q); lm = mod(d["lm_raw"].copy()); d["lams"] = LamArr(0.25 + np.maximum(lm, 0.0), lm); return d
    P.BaseSymmetricCutOperator.solve_q = sq
    op = P.ConformalEllipticModel(N_th=16, mu_max=4.0); eng = P.CenteredQEngine(op, dq=0.25, Q_max=16.0, K_max=16, act_tol=0.0)
    o = [eng.eval_K(K, s_max=2.5, n_s1=8, n_s2=4) for K in (8, 16)]; return (o[0][3], o[0][4], o[1][3], o[1][4])
base = run("base", lambda lm: lm); print(f"  base P1+P2: z=4 T0 {base[0]:+.6f} T2 {base[1]:+.6f} | z=8 T0 {base[2]:+.6f} T2 {base[3]:+.6f}", flush=True)
for tag, mod in (("floor modes -> 1e-22", lambda lm: np.where(lm <= 0, 1e-22, lm)), ("floor modes -> 1e-30", lambda lm: np.where(lm <= 0, 1e-30, lm)),
                 ("lm<1e-14 x10", lambda lm: np.where((lm > 0) & (lm < 1e-14), lm * 10, lm)), ("lm<1e-14 x0.1", lambda lm: np.where((lm > 0) & (lm < 1e-14), lm * 0.1, lm))):
    v = run(tag, mod); d = [v[i] - base[i] for i in range(4)]
    print(f"  {tag:22s}: dT0 z=4 {d[0]:+.2e} z=8 {d[2]:+.2e} (z-dep {d[2]-d[0]:+.1e}) | dT2 z=4 {d[1]:+.2e} z=8 {d[3]:+.2e} (z-dep {d[3]-d[1]:+.1e})", flush=True)
