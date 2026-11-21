"""EXP-083 R1 (i): P = 2 completeness gate. W2P2, W4P2; arms (a) no saddle and (b) honest replica saddle; n <= 60.
Gate: |Q'(M1, fixed own-pole + confluent) - Q'(many-base pencil)| <= 1e-3 per geometry and arm, else STOP. Also M1-M4 x hold-outs
(last n; interior n = 20, 21), and the 40-digit spot-check of honest Q(n) at n = 3, 6 (W2P2, arm a). [model: Opus 5.5]"""
import json, time, numpy as np, mpmath as mp
from exp083_honest import Geom
from exp083_models import fit, models, pencil
T0 = time.time(); out = {}
def log(*a): print(f"[{time.time()-T0:6.0f}s]", *a, flush=True)
NMAX = 60
for W in (2, 4):
    g = Geom(W, 2); own = {p: g.own_poles(p) for p in range(g.Ny // 2 + 1)}; ld1 = g.logdetB(g.Gn(1))
    for arm in ("a", "b"):
        Qs = [0.0]; sig = None
        for n in range(2, NMAX + 1):
            if arm == "b":
                # warm-started saddle
                N, Ny = g.N, g.Ny; G1 = g.Gn(1); target = sum(np.diag(x) for x in G1) / Ny; sig = np.zeros(N) if sig is None else sig
                for it in range(40):
                    G = g.Gn(n, sig); F = sum(np.diag(x)[:N] for x in G) / Ny - target
                    if np.abs(F).max() < 1e-13: break
                    J = np.zeros((N, N))
                    for x in G:
                        for s in range(n): J -= x[:N, s*N:(s+1)*N] ** 2
                    sig = sig - np.linalg.solve(J / Ny, F)
                else: raise RuntimeError("saddle not converged")
                Qs.append(g.logdetB(G) - n * ld1)
            else: Qs.append(g.logdetB(g.Gn(n)) - n * ld1)
        ns = list(range(1, NMAX + 1)); res = {}
        for floor in (1e-4, 1e-6):
            for name, kw in models(own, g.Ny, floor).items():
                for hn, hold in (("last", {NMAX}), ("interior", {20, 21})):
                    res[f"{name} floor{floor:g} hold-{hn}"] = fit(ns, Qs, hold, **kw)
        pq, pres, pnb = pencil(ns, Qs, hold={NMAX})
        m1 = res["M1 floor1e-06 hold-last"][0]; gate = abs(m1 - pq) <= 1e-3
        log(f"W{W}P2 arm ({arm}): Q(2..5) " + " ".join(f"{q:+.10f}" for q in Qs[1:5]) + f" ... Q({NMAX}) {Qs[-1]:+.6f}")
        for k, (qp, r) in res.items(): log(f"     {k:30s}: Q'(1) {qp:+.8f}  held-out rel {r:.1e}  {'ADEQUATE' if r <= 1e-9 else ''}")
        log(f"     pencil ({pnb} bases): Q'(1) {pq:+.8f} held-out rel {pres:.1e} | GATE |M1 - pencil| = {abs(m1-pq):.2e} -> {'PASS' if gate else 'FAIL -> STOP'}")
        out[f"W{W}P2_{arm}"] = dict(Q=Qs, fits={k: list(v) for k, v in res.items()}, pencil=[pq, pres, pnb], gate=bool(gate))
json.dump(out, open("exp083_p2gate_results.json", "w"), indent=1)
# 40-digit spot-check (W2P2, arm a, n = 3, 6)
mp.mp.dps = 40; g = Geom(2, 2)
def mpQ(n):
    Gs = {}
    for p in range(g.Ny // 2 + 1):
        H1 = g.Hn(p, 1); Hn = g.Hn(p, n); Gs[p] = (mp.inverse(mp.matrix(H1.tolist())), mp.inverse(mp.matrix(Hn.tolist())))
    tot = mp.mpf(0)
    for k in range(g.Ny):
        for which, nn in ((1, n), (0, 1)):
            G = [Gs[p if p <= g.Ny // 2 else g.Ny - p][which] for p in range(g.Ny)]; M = G[0].rows
            B = mp.matrix(M, M)
            for p in range(g.Ny):
                A, C = G[p], G[(k - p) % g.Ny]
                for i in range(M):
                    for j in range(M): B[i, j] += 2 * A[i, j] * C[i, j] / g.Ny
            tot += (mp.log(mp.det(B)) if which == 1 else -nn * 0) if which == 1 else 0
            if which == 0: tot -= n * mp.log(mp.det(B))
    return tot
for n in (3, 6):
    qm = mpQ(n); log(f"40-digit spot-check W2P2 arm (a) n={n}: mp {mp.nstr(qm, 15)} vs float64 {out['W2P2_a']['Q'][n-1]:+.12f}  rel diff {abs(float(qm) - out['W2P2_a']['Q'][n-1]) / abs(float(qm)):.1e}")
