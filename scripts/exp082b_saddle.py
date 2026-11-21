"""EXP-082b (arm (b) of the eps-family referee; my code, independent of T46f): honest integer-n Q(n; eps) WITH the honest replica
saddle sigma_n on the EXP-082 family (T46d broken cocycle, hopping-only weak bond -eps). n-sheet manifold gluing as exp082 (deduplicated).
sigma enters H_q^(n) as diag(sigma) on every sheet (the continuation's convention: dG = -G diag(sd) G). Gap equation (sheet 0):
sum_{q in q0} (dq/pi) G_q^(n)[sigma](x,x) = sum_{q in q0} (dq/pi) G_q^(1)(x,x), q0 = (m + 1/2) dq, m < M_q; Newton with the exact
Jacobian -(dq/pi) sum_q sum_s' G_q^(n)(x_0, y_s')^2. Q(n) = log det B_n[sigma_n] - n log det B_1, n = 2..16. [model: Opus 5.5]"""
import sys, json, importlib.util, os, numpy as np
spec = importlib.util.spec_from_file_location("t46d", os.path.join(sys.argv[1], "brief_p2_t46d.py")); D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)
import exp082_honest_eps as H0                       # reuse Hn (gluing) and the pair list
dq, Qmax, K = 0.5, 4.0, 2; M_q = int(round(Qmax / dq)); q0 = [(m + 0.5) * dq for m in range(M_q)]
pairs, w = H0.pairs, H0.w
out = {}
for eps in (1.0, 1e-1, 1e-2, 1e-3, 1e-4):
    op = H0.model(eps); N = op.N; Q = {1: 0.0}
    Gn1 = {q: np.linalg.inv(H0.Hn(op, 1, q)) for q in set(q0) | {a for p in pairs for a in p}}
    target = sum((dq / np.pi) * np.diag(Gn1[q]) for q in q0)
    B1 = sum(w * 2.0 * Gn1[a] * Gn1[b] for a, b in pairs); ld1 = np.linalg.slogdet(B1)[1]; sig = np.zeros(N)
    for n in range(2, 17):
        for it in range(30):
            Hs = {q: H0.Hn(op, n, q) + np.diag(np.tile(sig, n)) for q in set(q0) | {a for p in pairs for a in p}}
            G = {q: np.linalg.inv(h) for q, h in Hs.items()}
            F = sum((dq / np.pi) * np.diag(G[q])[:N] for q in q0) - target
            if np.abs(F).max() < 1e-14: break
            J = np.zeros((N, N))
            for q in q0:
                for s in range(n): J -= (dq / np.pi) * G[q][:N, s*N:(s+1)*N] ** 2
            sig = sig - np.linalg.solve(J, F)
        else: raise RuntimeError(f"saddle not converged eps={eps} n={n}")
        B = sum(w * 2.0 * G[a] * G[b] for a, b in pairs); Q[n] = float(np.linalg.slogdet(B)[1] - n * ld1)
    out[str(eps)] = Q
    print(f"eps={eps:g}: honest saddle-ON Q(n) n=2..16: " + " ".join(f"{Q[n]:+.10e}" for n in range(2, 17)), flush=True)
json.dump(out, open("exp082b_results.json", "w"), indent=1)
