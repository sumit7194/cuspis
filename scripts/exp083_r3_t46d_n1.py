"""R3 Tier-1: Q_cont(1) of T46d's n-general continuation on the EXP-082 eps-family: Q0(1) = sum log det(B1 + sum_pairs w
pair_delta_B_exact(n=1, beta=1)) - log det B1 (beta = 1 == 0 by 1-periodicity; avoids the integer-alpha special case). Delivered threshold
(r > 1e-10) vs threshold removed (scratch source replace 1e-10 -> 0.0). Honest Q(1) = 0 exactly. [model: Opus 5.5]"""
import sys, os, importlib.util, numpy as np
src = open(os.path.join(sys.argv[1], "brief_p2_t46d.py")).read()
def load(name, text):
    p = os.path.join(sys.argv[1], name + ".py"); open(p, "w").write(text); s = importlib.util.spec_from_file_location(name, p)
    m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
mods = {"threshold 1e-10 (delivered)": load("t46d_d", src), "threshold removed": load("t46d_nothr", src.replace("1e-10", "0.0"))}
for eps in (1.0, 0.01):
    row = []
    for name, D in mods.items():
        op = D.ConformalEllipticModel(N_th=12, mu_max=3.0, cut_mode="closed_loop_broken"); j = op.N_mu - 1
        i1, i2 = j * op.N_th + op.N_th // 2, j * op.N_th + op.N_th // 2 - 1; L = op.L0.tolil(); L[i1, i2] = -eps; L[i2, i1] = -eps; op.L0 = L.tocsc()
        eng = D.CenteredQEngine(op, dq=0.5, Q_max=4.0, K_max=2, act_tol=0.0); w = 0.5 / (2 * np.pi); m_lo = 1 - eng.M_q
        prs = [(eng._get_qd(m), eng._get_qd(1 - m)) for m in range(m_lo, m_lo + 2 * eng.M_q)]
        B1 = sum(w * 2.0 * (a['G0'] * b['G0']) for a, b in prs)
        try:
            B = B1 + sum(w * D.pair_delta_B_exact(a, b, 1.0, 1.0) for a, b in prs); s, l = np.linalg.slogdet(B); s1, l1 = np.linalg.slogdet(B1)
            row.append(f"{name}: Q_cont(1) = {l - l1:+.4e} (phase {np.angle(s / s1):+.1e})")
        except Exception as e: row.append(f"{name}: FAIL {type(e).__name__}")
    print(f"eps={eps:g}: " + " | ".join(row), flush=True)
