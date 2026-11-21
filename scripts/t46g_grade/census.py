# High-precision census of the n=1 cut-mode spectrum delta = lambda - 1/4 (sigma = 0), T46g eps-family; mpmath 60 digits vs float64.
import sys, os, numpy as np, mpmath as mp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "code"))
import t46g_ntf as T
mp.mp.dps = 60
for eps in (0.1, 1.0):
    op = T.CheckerEpsModel(eps_link=eps); _, uq = T.build_pairs_k(); uq = sorted(set(uq) | {round((m + 0.5) * 0.5, 8) for m in range(8)})
    L = op.L0.toarray(); N = op.N; Ps = mp.matrix(op.P_s.tolist()); Pa = mp.matrix(op.P_a.tolist())
    L[op.cut_top[-1], op.cut_bot[-1]]  # touch
    allm = []
    for q in uq:
        H = mp.matrix(N, N)
        for i in range(N):
            for j in range(N):
                if L[i, j] != 0: H[i, j] = mp.mpf(L[i, j])
            H[i, i] += mp.mpf(q) ** 2 * mp.mpf(op.weights[i])
        G = H ** -1
        Gs = Ps.T * G * Ps; Ga = Pa.T * G * Pa
        Gtb = mp.matrix([[G[a, b] for b in op.cut_bot] for a in op.cut_top])
        D = (Gtb + Gtb.T) / 2 - Gs * Ga
        E, Q = mp.eigsy(mp.eye(op.W_cut) / 2 - Ga)
        Mh = Q * mp.diag([mp.sqrt(e) for e in E]) * Q.T; Mih = Q * mp.diag([1 / mp.sqrt(e) for e in E]) * Q.T
        S = Mh * D * Mih; S = (S + S.T) / 2
        d = sorted([S_ for S_ in mp.eigsy(S, eigvals_only=True)], key=lambda x: abs(x))
        f64 = np.sort(np.abs(T.solve_q_complex(op, q, None)['deltas'].real))
        f64raw = T.DREC[-1].real; T.DREC.clear()
        small = [x for x in d if abs(x) < 1e-8]
        print(f"eps={eps} q={q:5.2f}: W_cut={op.W_cut}; hi-prec |delta|<1e-8: " + ", ".join(mp.nstr(x, 3) for x in small) +
              f" | f64 raw |delta|<1e-8: " + ", ".join(f"{x:.1e}" for x in sorted(f64raw, key=abs) if abs(x) < 1e-8), flush=True)
