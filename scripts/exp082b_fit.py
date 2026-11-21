"""EXP-082b fits: Q'(1; eps) saddle ON from my honest data (Q(1) = 0 included), Q(n) = A n + B + sum_j C_j b_j^n (+ n b^n variant),
1-3 bases by log-grid search, last n (16) and interior (6, 7) held out; vs T46f saddle-ON continuation on the same family. [model: Opus 5.5]"""
import json, itertools, numpy as np
d = json.load(open("exp082b_results.json")); g = json.load(open("t46f_gate_results.json"))
grid = np.exp(np.linspace(np.log(1e-10), np.log(0.9), 220))
def fitq(ns, y, bs, conf, hold):
    tr = np.array([n not in hold for n in ns]); cols = [ns, np.ones_like(ns)] + [b ** ns for b in bs] + ([ns * b ** ns for b in bs] if conf else [])
    X = np.column_stack(cols); c, *_ = np.linalg.lstsq(X[tr], y[tr], rcond=None)
    qp = c[0] + sum(c[2 + i] * b * np.log(b) for i, b in enumerate(bs)) + (sum(c[2 + len(bs) + i] * b * (1 + np.log(b)) for i, b in enumerate(bs)) if conf else 0)
    return qp, float(np.abs(X[~tr] @ c - y[~tr]).max() / np.abs(y[~tr]).max()), float(np.sqrt(np.mean((X[tr] @ c - y[tr]) ** 2)))
for eps in ("1.0", "0.1", "0.01", "0.001", "0.0001"):
    Q = {int(k): v for k, v in d[eps].items()}; ns = np.arange(1, 17, dtype=float); y = np.array([Q[int(n)] for n in ns]); res = []
    for nb, conf in ((1, False), (1, True), (2, False), (2, True), (3, False)):
        best = None
        it = itertools.combinations(grid[::(1 if nb == 1 else 6 if nb == 2 else 20)], nb)
        for bs in it:
            try: qp, ho, rms = fitq(ns, y, bs, conf, {16})
            except Exception: continue
            if best is None or rms < best[2]: best = (qp, ho, rms, bs)
        qp, ho, rms, bs = best; qpi, hoi, _ = fitq(ns, y, bs, conf, {6, 7})
        res.append(f"{nb}b{'+conf' if conf else ''}: {qp:+.5e} (ho16 {ho:.0e}, ho6,7 {hoi:.0e}, b {[f'{b:.1e}' for b in bs]})")
    cont = g[f"{float(eps)}|1.0"][1]
    print(f"eps={eps}: T46f saddle-ON continuation {cont:+.5e} | honest fits: " + " ; ".join(res), flush=True)
