"""EXP-082 add-on: does T46d's continued sector formula hit the honest integer data? Q_cont(n) = sum_{Q=0}^{n-1}
[log det(B1 + sum_pairs w pair_delta_B_exact(n, Q/n)) - log det B1] at n = 2, 3 vs honest Q(n), eps = 1 and 0.01. [model: Opus 5.5]"""
import sys, json, numpy as np, runpy
g = runpy.run_path("exp082_honest_eps.py", run_name="lib") if False else None
import importlib.util, os
spec = importlib.util.spec_from_file_location("t46d", os.path.join(sys.argv[1], "brief_p2_t46d.py")); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
d = json.load(open("exp082_results.json")); dq, Qmax, K = 0.5, 4.0, 2
for eps in (1.0, 0.01):
    op = D.ConformalEllipticModel(N_th=12, mu_max=3.0, cut_mode="closed_loop_broken"); j = op.N_mu - 1
    i1, i2 = j * op.N_th + op.N_th // 2, j * op.N_th + op.N_th // 2 - 1; L = op.L0.tolil(); L[i1, i2] = -eps; L[i2, i1] = -eps; op.L0 = L.tocsc()
    eng = D.CenteredQEngine(op, dq=dq, Q_max=Qmax, K_max=K, act_tol=0.0); w = dq / (2 * np.pi); m_lo = K // 2 - eng.M_q
    prs = [(eng._get_qd(m), eng._get_qd(K - 1 - m)) for m in range(m_lo, m_lo + 2 * eng.M_q)]
    B1 = sum(w * 2.0 * (a['G0'] * b['G0']) for a, b in prs); s1, l1 = np.linalg.slogdet(B1); row = []
    for n in (2, 3):
        tot = 0.0
        for Qs in range(n):
            beta = Qs / n if Qs else 0.0
            B = B1 + sum(w * D.pair_delta_B_exact(a, b, float(n), beta) for a, b in prs); s, l = np.linalg.slogdet(B); tot += (l - l1)
        row.append(f"n={n}: Q_cont {tot:+.8e} vs honest {d[str(eps)]['Q'][str(n)]:+.8e}")
    print(f"eps={eps}: " + " | ".join(row), flush=True)
