"""EXP-092 amendment b (P = 24; Bridge GO after the W6P12 landing): out-of-sample predictions at P = 24 from STORED centre values only,
computed and committed BEFORE the P = 24 run. [model: Opus 5.5]
Inputs: P = 8, 10, 12 from the office G files (exp085c/G_W{P}P{P}.json, key cA, centre sites), P = 14, 16, 20 from exp092_cA_P{P}.json.
KA (must reproduce before anything is predicted): the registered 3-parameter forms fitted to P = 8-14 give, at P = 16 / 20,
  H-log (gL = 0.0611 fixed) -0.0991561 / -0.1022378 and no-log -0.0991277 / -0.1021242 (EXP-092 §2, 1e-7 abs).
Predictions at P = 24 from P = 8-20 (the registered §5 forms): (i) no-log c + g1/P + g2/P^2 + g3/P^3; (ii) free log c + (g1 + gL ln P)/P + g2/P^2;
  (iii) fixed gL = 0.0611: c + (g1 + 0.0611 ln P)/P + g2/P^2. Also the two 3-parameter §2 forms from P = 8-14 (as registered).
Output: exp081d_results/exp092b_pred_P24.json"""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "exp081d_results")
def centre(P): Lx, Lt = 3 * P, 2 * P; return [x * Lt + t for x in (Lx // 2 - 1, Lx // 2) for t in (Lt // 2 - 1, Lt // 2)]
C = {}
for P in (8, 10, 12): C[P] = float(np.mean(np.array(json.load(open(os.path.join(D, "exp085c", f"G_W{P}P{P}.json")))["cA"]).real[centre(P)]))
for P in (14, 16, 20): C[P] = json.load(open(os.path.join(D, f"exp092_cA_P{P}.json")))["centre"]
GL = 0.0611
def fit(Ps, form):
    P = np.array(Ps, float); y = np.array([C[p] for p in Ps])
    if form == "i":   X = np.vstack([np.ones_like(P), 1 / P, 1 / P**2, 1 / P**3]).T; off = 0 * P
    if form == "ii":  X = np.vstack([np.ones_like(P), 1 / P, np.log(P) / P, 1 / P**2]).T; off = 0 * P
    if form == "iii": X = np.vstack([np.ones_like(P), 1 / P, 1 / P**2]).T; off = GL * np.log(P) / P
    if form == "nolog3": X = np.vstack([np.ones_like(P), 1 / P, 1 / P**2]).T; off = 0 * P
    c = np.linalg.lstsq(X, y - off, rcond=None)[0]
    def f(p):
        p = float(p)
        row = {"i": [1, 1/p, 1/p**2, 1/p**3], "ii": [1, 1/p, np.log(p)/p, 1/p**2], "iii": [1, 1/p, 1/p**2], "nolog3": [1, 1/p, 1/p**2]}[form]
        return float(np.dot(row, c) + (GL * np.log(p) / p if form == "iii" else 0.0))
    rms = float(np.sqrt(np.mean((np.array([f(p) for p in Ps]) - y) ** 2)))
    return f, c, rms
FAIL = []
fh, _, _ = fit((8, 10, 12, 14), "iii"); fn, _, _ = fit((8, 10, 12, 14), "nolog3")
for P, h, n in ((16, -0.0991561, -0.0991277), (20, -0.1022378, -0.1021242)):
    ok = abs(fh(P) - h) <= 1e-7 and abs(fn(P) - n) <= 1e-7
    print(f"KA P = {P}: H-log {fh(P):+.7f} (reg {h:+.7f}), no-log {fn(P):+.7f} (reg {n:+.7f}) -> {'PASS' if ok else 'FAIL'}")
    if not ok: FAIL.append(P)
if FAIL: raise SystemExit("KA FAILED: no prediction is made")
out = dict(KA="PASS", inputs=C, pred={})
for form in ("i", "ii", "iii"):
    f, c, rms = fit((8, 10, 12, 14, 16, 20), form); out["pred"][f"{form}_P8-20"] = dict(P24=f(24), params=list(map(float, c)), rms=rms)
    print(f"P = 8-20 ({form:3s}): rms {rms:.2e}  -> P = 24 prediction {f(24):+.10f}" + (f"  (gL {c[2]:+.4f})" if form == "ii" else ""))
out["pred"]["Hlog3_P8-14"] = dict(P24=fh(24)); out["pred"]["nolog3_P8-14"] = dict(P24=fn(24))
print(f"P = 8-14 3-parameter (registered §2 forms): H-log {fh(24):+.10f}, no-log {fn(24):+.10f}")
json.dump(out, open(os.path.join(D, "exp092b_pred_P24.json"), "w"), indent=1)
