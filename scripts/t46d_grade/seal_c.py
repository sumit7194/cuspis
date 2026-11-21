"""Sealed-derivation check (c), perturbed pure gauge: T46d 'closed_loop_broken' (one theta=0 link at the outer ring left
untwisted) with that link's hopping scaled by eps. eps -> 0 restores an exact closed cocycle (pure gauge, Q'(1) = 0). Q'(1) at
k = 1 (N_th 12, mu_max 3, dq 0.5, Q_max 4, s_max 2.5, as T46d item 1) vs eps, delivered threshold code vs P1+P2."""
import sys, os, runpy, numpy as np
g = runpy.run_path(os.path.join(os.path.dirname(__file__), "seal_b_lib.py"), init_globals={"ARGV": sys.argv})
P, D0 = g["P"], g["D0"]
def build(M, eps):
    op = M.ConformalEllipticModel(N_th=12, mu_max=3.0, cut_mode="closed_loop_broken"); j = op.N_mu - 1
    i1, i2 = j * op.N_th + op.N_th // 2, j * op.N_th + op.N_th // 2 - 1; L = op.L0.tolil(); L[i1, i2] = -eps; L[i2, i1] = -eps; op.L0 = L.tocsc(); return op
for name, M in (("delivered threshold", D0), ("P1+P2", P)):
    row = []
    for eps in (1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-6, 1e-8, 0.0):
        try:
            eng = M.CenteredQEngine(build(M, eps), dq=0.5, Q_max=4.0, K_max=2, act_tol=0.0); k, T1, Ts, T0, T2, Qp = eng.eval_K(2, s_max=2.5, n_s1=6, n_s2=4)
            row.append(f"eps={eps:g}: Q'={Qp:+.3e} (T0 {T0:+.2e}, T2 {T2:+.2e})")
        except Exception as e: row.append(f"eps={eps:g}: FAILED {type(e).__name__}")
    print(f"  {name}:\n    " + "\n    ".join(row), flush=True)
