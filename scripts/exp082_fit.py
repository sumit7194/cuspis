"""EXP-082 fits: Q'(1; eps) from the honest integer data (Q(1) = 0 included), models Q(n) = A n + B + sum_j C_j b_j^n with
1 or 2 bases b_j found by a log-grid search (coefficients linear); fit on n = 1..7, n = 8 held out. Q'(1) = A + sum C_j b_j ln b_j.
[model: Opus 5.5]"""
import json, itertools, numpy as np
d = json.load(open("exp082_results.json"))
grid = np.exp(np.linspace(np.log(1e-12), np.log(0.9), 400))
for eps in ("1.0", "0.1", "0.01", "0.001", "0.0001"):
    Q = {1: 0.0, **{int(k): v for k, v in d[eps]["Q"].items()}}; n_tr = np.arange(1, 8); y = np.array([Q[n] for n in n_tr]); res = []
    for nb in (1, 2):
        best = None
        for bs in (itertools.combinations(grid[::4], 2) if nb == 2 else ((b,) for b in grid)):
            X = np.column_stack([n_tr, np.ones_like(n_tr, float)] + [np.power(b, n_tr) for b in bs])
            c, *_ = np.linalg.lstsq(X, y, rcond=None); rms = np.sqrt(np.mean((X @ c - y) ** 2))
            if best is None or rms < best[0]: best = (rms, bs, c)
        rms, bs, c = best; qp = c[0] + sum(cj * b * np.log(b) for cj, b in zip(c[2:], bs))
        pred8 = c[0] * 8 + c[1] + sum(cj * b ** 8 for cj, b in zip(c[2:], bs))
        res.append(f"{nb} base(s) {[f'{b:.2e}' for b in bs]}: Q'(1) = {qp:+.5e} (rms {rms:.1e}, held-out n=8 err {abs(pred8 - Q[8]):.1e})")
    print(f"eps={eps}: continuation (threshold) T1+T2 = {d[eps]['cont_T1_plus_T2']:+.4e} | honest-data fits: " + " ; ".join(res), flush=True)
