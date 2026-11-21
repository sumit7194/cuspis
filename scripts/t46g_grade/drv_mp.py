# Inject the 60-digit n=1 cut spectrum (Mm^{+-1/2}, delta, Y) into T46g's eval_exact_n1_slope; floor sweep. sigma=None only (n=1).
import sys, os, numpy as np, mpmath as mp
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "code"))
import t46g_mp as T
mp.mp.dps = int(os.environ.get("DPS", "60")); CACHE = {}
def mpspec(op, q):
    key = (op.eps_link, q)
    if key in CACHE: return CACHE[key]
    L = op.L0.toarray(); N = op.N; Ps = mp.matrix(op.P_s.tolist()); Pa = mp.matrix(op.P_a.tolist()); H = mp.matrix(N, N)
    for i in range(N):
        for j in range(N):
            if L[i, j] != 0: H[i, j] = mp.mpf(L[i, j])
        H[i, i] += mp.mpf(q) ** 2 * mp.mpf(op.weights[i])
    G = H ** -1; Gs = Ps.T * G * Ps; Ga = Pa.T * G * Pa
    Gtb = mp.matrix([[G[a, b] for b in op.cut_bot] for a in op.cut_top]); D = (Gtb + Gtb.T) / 2 - Gs * Ga
    E, Q = mp.eigsy(mp.eye(op.W_cut) / 2 - Ga)
    Mh = Q * mp.diag([mp.sqrt(e) for e in E]) * Q.T; Mih = Q * mp.diag([1 / mp.sqrt(e) for e in E]) * Q.T
    S = Mh * D * Mih; S = (S + S.T) / 2; d, Y = mp.eigsy(S)
    f = lambda M: np.array([[complex(float(M[i, j])) for j in range(M.cols)] for i in range(M.rows)])
    out = (f(Mh), f(Mih), np.array([complex(float(x)) for x in d]), f(Y)); CACHE[key] = out; return out
for eps in (0.0, 0.1, 1.0):
    op = T.CheckerEpsModel(eps_link=eps)
    T.MPSPEC = None; s = T.eval_exact_n1_slope(op); base = s['T1'] + s['T_sad'] + s['T2']
    print(f"eps={eps}: float64 original: slope {base:+.12e} (T1 {s['T1']:+.10e} Tsad {s['T_sad']:+.10e} T2 {s['T2']:+.10e})", flush=True)
    T.MPSPEC = mpspec
    for fl in (1e-14, 1e-16, 1e-18, 1e-20, 1e-22, 1e-40):
        T.MPFLOOR = fl; s = T.eval_exact_n1_slope(op); v = s['T1'] + s['T_sad'] + s['T2']
        print(f"eps={eps}: 60-digit spectrum, keep delta > {fl:.0e}: slope {v:+.12e} (T1 {s['T1']:+.10e} Tsad {s['T_sad']:+.10e} T2 {s['T2']:+.10e}) | minus float64 {v-base:+.2e}", flush=True)
