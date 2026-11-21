"""EXP-082 (registered e09178d): honest integer-n Q(n; eps) on T46d's broken cocycle with the untwisted outer link's hopping
-eps. The geometry (L0, weights, cut link list) is taken from T46d's ConformalEllipticModel (UNVERIFIED code, read in full),
loaded from a path given on the command line; the replica gluing, Green's functions, bubble and determinants are mine.
Also prints T1 + T2 from the delivered threshold continuation at the same slice for comparison. [model: Opus 5.5]"""
import sys, os, json, importlib.util, numpy as np
spec = importlib.util.spec_from_file_location("t46d", os.path.join(sys.argv[1], "brief_p2_t46d.py")); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
dq, Qmax, K = 0.5, 4.0, 2
def model(eps):
    op = D.ConformalEllipticModel(N_th=12, mu_max=3.0, cut_mode="closed_loop_broken"); j = op.N_mu - 1
    i1, i2 = j * op.N_th + op.N_th // 2, j * op.N_th + op.N_th // 2 - 1; L = op.L0.tolil(); L[i1, i2] = -eps; L[i2, i1] = -eps
    op.L0 = L.tocsc(); return op
def Hn(op, n, q):
    """n-sheet manifold: every cut link (top it, bottom ib) joins it on sheet s to ib on sheet s+1 (mod n)."""
    N = op.N; L = op.L0.toarray(); base = L + np.diag(q * q * op.weights); H = np.zeros((n * N, n * N))
    for s in range(n): H[s*N:(s+1)*N, s*N:(s+1)*N] = base
    seen = set()
    for it, ib in zip(op.cut_top, op.cut_bot):
        if (it, ib) in seen: continue                           # run 1 bug: T46d lists some j=0 links twice (L0 = -2 there)
        seen.add((it, ib))
        for s in range(n):
            a, b = s * N + it, s * N + ib
            H[a, b] = 0.0; H[b, a] = 0.0                       # remove in-sheet link (it, ib), full weight
        for s in range(n):
            a = s * N + it; t = ((s + 1) % n) * N + ib
            H[a, t] += L[it, ib]; H[t, a] += L[ib, it]          # glue it(s) <-> ib(s+1) with the full link weight
    return H
M_q = int(round(Qmax / dq)); qpos = (np.arange(M_q + K + 2) + 0.5) * dq
idx = lambda m: m if m >= 0 else -1 - m; m_lo = K // 2 - M_q
pairs = [(qpos[idx(m)], qpos[idx(K - 1 - m)]) for m in range(m_lo, m_lo + 2 * M_q)]; w = dq / (2 * np.pi)
def logdetB(op, n):
    Gs = {}
    for q1, q2 in pairs:
        for q in (q1, q2):
            if q not in Gs: Gs[q] = np.linalg.inv(Hn(op, n, q))
    B = sum(w * 2.0 * Gs[q1] * Gs[q2] for q1, q2 in pairs); s, ld = np.linalg.slogdet(B); return ld, s
out = {}
for eps in (1.0, 1e-1, 1e-2, 1e-3, 1e-4, 1e-6, 1e-8, 0.0):
    op = model(eps); ld1, _ = logdetB(op, 1); Q = {n: logdetB(op, n)[0] - n * ld1 for n in range(2, 9)}
    eng = D.CenteredQEngine(op, dq=dq, Q_max=Qmax, K_max=K, act_tol=0.0); k, T1, Ts, T0, T2, Qp = eng.eval_K(K, s_max=2.5, n_s1=6, n_s2=4)
    out[eps] = dict(Q=Q, cont_T1_plus_T2=T1 + T2, cont_Tsad=Ts)
    print(f"eps={eps:g}: honest Q(n) n=2..8: " + " ".join(f"{Q[n]:+.6e}" for n in range(2, 9)) + f" | threshold cont. T1+T2 = {T1+T2:+.4e} (Tsad {Ts:+.2e})", flush=True)
json.dump({str(k): v for k, v in out.items()}, open("exp082_results.json", "w"), indent=1)
