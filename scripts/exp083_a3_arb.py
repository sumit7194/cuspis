"""EXP-083 R2 A3 (ac1e325): Arb honest Q(n) on the EXP-082 family at eps = 1, arms (a) no saddle and (b) replica saddle.
Sector decomposition: G_q(j/n) = direct Arb inverse of the single-sheet operator L0 + q^2 W with each unique cut link's FULL L0 weight
twisted (H[it,ib] = L0[it,ib] z, H[ib,it] = L0[ib,it]/z, z = e^{2 pi i j/n}); B^(Q) = sum_pairs w (2/n) sum_j G_q1(j/n) o G_q2((Q-j)/n)
via a replica DFT per pair; Q(n) = sum_Q log det B^(Q) - n log det B_1. Saddle: sigma on all sheets, gap
sum_{q in q0} (dq/pi) (1/n) sum_j G_q(j/n)(x,x) = same at n = 1, quasi-Newton (float64 Jacobian, Arb residual, |F| <= 1e-100).
First: check vs float64 EXP-082 (arm a) / EXP-082b (arm b) at n = 2..6 (<= 1e-10). Usage: python exp083_a3_arb.py arm nmax T46d_dir
[model: Opus 5.5]"""
import sys, os, json, time, numpy as np
from flint import acb_mat, acb, arb, ctx
ctx.prec = 400; T0 = time.time()
def log(*a): print(f"[{time.time()-T0:7.0f}s]", *a, flush=True)
arm, NMAX = sys.argv[1], int(sys.argv[2]); sys.argv = [sys.argv[0], sys.argv[3]]
import exp082_honest_eps as H0                                    # (re-runs its deterministic EXP-082 loop on import)
op = H0.model(1.0); N = op.N; L = op.L0.toarray(); Wt = op.weights
links = sorted({(it, ib) for it, ib in zip(op.cut_top, op.cut_bot)})
dq = 0.5; q0 = [(m + 0.5) * dq for m in range(8)]; pairs = H0.pairs; w = arb(1) / (4 * arb.pi())      # w = dq/(2 pi)
qs = sorted({q for p in pairs for q in p} | set(q0))
def Hq(q, j, n, sig):
    rows = [[acb(float(L[i, k])) for k in range(N)] for i in range(N)]
    for i in range(N): rows[i][i] = acb(float(L[i, i])) + arb(q) ** 2 * arb(float(Wt[i])) + (sig[i] if sig is not None else 0)
    z = acb.exp_pi_i(acb(2 * j) / n)
    for it, ib in links: rows[it][ib] = acb(float(L[it, ib])) * z; rows[ib][it] = acb(float(L[ib, it])) / z
    return acb_mat(rows)
def Gs(n, sig=None): return {q: [Hq(q, j, n, sig).inv() for j in range(n)] for q in qs}
def had(A, B): return acb_mat([[A[i, k] * B[i, k] for k in range(N)] for i in range(N)])
def logdetB(n, G):
    wn = [acb.exp_pi_i(acb(2 * b) / n) for b in range(n)]; tot = arb(0)
    hat = {q: [sum((G[q][j] * wn[(b * j) % n] for j in range(n)), acb_mat(N, N)) for b in range(n)] for q in qs}
    C = [acb_mat(N, N) for _ in range(n)]
    for q1, q2 in pairs:
        for b in range(n): C[b] += had(hat[q1][b], hat[q2][b])
    for Qs in range(n):
        B = sum((C[b] * wn[(-b * Qs) % n] for b in range(n)), acb_mat(N, N)) * (w * 2 / (n * n))
        tot += B.det().log().real
    return tot
def gapdiag(n, G): return [sum((G[q][j][x, x] for q in q0 for j in range(n)), acb(0)).real * arb(dq) / (arb.pi() * n) for x in range(N)]
G1 = Gs(1); ld1 = logdetB(1, G1); target = gapdiag(1, G1)
def saddle(n, sig0):
    # float64 Jacobian from the n-sheet manifold (exp082b form)
    Hs = {q: np.linalg.inv(H0.Hn(op, n, q) + np.diag(np.tile(np.array([float(s.mid()) for s in sig0]) if sig0 else np.zeros(N), n))) for q in q0}
    J = np.zeros((N, N))
    for q in q0:
        for s in range(n): J -= (dq / np.pi) * Hs[q][:N, s*N:(s+1)*N] ** 2
    Ji = np.linalg.inv(J); sig = sig0 if sig0 else [arb(0)] * N
    for it in range(14):
        G = Gs(n, sig); F = [a - b for a, b in zip(gapdiag(n, G), target)]
        fm = max(abs(float(f.mid())) + float(f.rad()) for f in F)
        if fm < 1e-100: return sig, G, it, fm
        sig = [sig[x] - sum((arb(float(Ji[x, y])) * F[y] for y in range(N)), arb(0)) for x in range(N)]
    raise SystemExit(f"Arb saddle not converged n={n} |F|={fm:.1e} -> STOP")
out = {"arm": arm, "Q": {}, "rad": {}}; ref = json.load(open("exp082_results.json" if arm == "a" else "exp082b_results.json"))
sig = None
for n in range(2, NMAX + 1):
    if arm == "b": sig, G, it, fm = saddle(n, sig)
    else: G = Gs(n)
    Qn = logdetB(n, G) - n * ld1; out["Q"][n] = Qn.mid().str(110, radius=False); out["rad"][n] = float(Qn.rad())
    if n <= 6:
        fl = ref["1.0"]["Q"][str(n)] if arm == "a" else ref["1.0"][str(n)]
        d = abs(float(Qn.mid()) - fl); log(f"   check vs float64 n={n}: |Arb - float| = {d:.1e}")
        if d > 1e-10: raise SystemExit("decomposition check vs float64 FAILED -> STOP")
    if out["rad"][n] > 1e-60: raise SystemExit(f"radius {out['rad'][n]:.1e} > 1e-60 -> STOP")
    log(f"eps=1 arm {arm} n={n}: Q = {Qn.mid().str(25, radius=False)} (rad {out['rad'][n]:.1e})" + (f" saddle it {it} |F| {fm:.1e}" if arm == "b" else ""))
    json.dump(out, open(f"exp083_r2/a3_eps1_{arm}.json", "w"), indent=1)
