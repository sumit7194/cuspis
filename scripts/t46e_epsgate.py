"""T46e grading gate (the Bridge): T46e's threshold-free T0 formula (pair_dB_dn_continuous) + its T2 on the EXP-082 eps-family
(T46d broken cocycle, untwisted outer link hopping -eps, k = 1, dq 0.5, Q_max 4), no saddle: Q'_cont = T1_new + T2, against the honest
integer-data Q'(1; eps) of EXP-082. r_floor in {0, 1e-10, 1e-8}. Delivered code run unchanged from a scratch copy. [model: Opus 5.5]"""
import sys, os, json, importlib.util, numpy as np
from scipy import linalg
def load(name):
    s = importlib.util.spec_from_file_location(name, os.path.join(sys.argv[1], name + ".py")); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
D, E = load("brief_p2_t46d"), load("brief_p2_t46e")
honest = {1.0: (-0.339, -0.316), 0.1: (-0.0457, -0.0436), 0.01: (-0.00587, -0.00585), 1e-3: (-7.2e-4, -6.9e-4), 1e-4: (-8.6e-5, -7.4e-5)}
dq, Qmax, K = 0.5, 4.0, 2; out = {}
for eps, (h1, h2) in honest.items():
    op = D.ConformalEllipticModel(N_th=12, mu_max=3.0, cut_mode="closed_loop_broken"); j = op.N_mu - 1
    i1, i2 = j * op.N_th + op.N_th // 2, j * op.N_th + op.N_th // 2 - 1; L = op.L0.tolil(); L[i1, i2] = -eps; L[i2, i1] = -eps; op.L0 = L.tocsc()
    row = []
    for rf in (0.0, 1e-10, 1e-8):
        eng = E.CenteredQEngine(op, dq=dq, Q_max=Qmax, K_max=K, r_floor=rf); w = dq / (2 * np.pi); m_lo = K // 2 - eng.M_q
        prs = [(eng._get_qd(m), eng._get_qd(K - 1 - m)) for m in range(m_lo, m_lo + 2 * eng.M_q)]
        B1 = sum(w * 2.0 * (a['G0'] * b['G0']) for a, b in prs); cho = linalg.cho_factor(B1)
        T1 = float(np.trace(linalg.cho_solve(cho, sum(w * E.pair_dB_dn_continuous(a, b, r_floor=rf) for a, b in prs))))
        try: _, T0, T2, _ = eng.eval_K(K, s_max=2.5, n_s1=6, n_s2=4)
        except Exception as e: T2 = float("nan")
        engd = D.CenteredQEngine(op, dq=dq, Q_max=Qmax, K_max=K, act_tol=0.0); T2d = engd.eval_K(K, s_max=2.5, n_s1=6, n_s2=4)[4]
        row.append((rf, T1 + T2, T1, T2, T1 + T2d)); out[f"{eps}|{rf}"] = [T1 + T2, T1, T2, T1 + T2d]
    print(f"eps={eps:g}: honest Q'(1) {h1:+.3e} / {h2:+.3e} | T46e T1+T2: " + " ; ".join(f"floor {rf:g}: T1+T2 {q:+.4e} (T1 {t1:+.3e}, T2 {t2:+.3e}; T1+T2[T46d] {qd:+.4e})" for rf, q, t1, t2, qd in row), flush=True)
json.dump(out, open("t46e_epsgate_results.json", "w"), indent=1)
