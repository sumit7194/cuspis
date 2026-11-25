"""EXP-086b (notes/EXP-086b_registration.md): DESCRIPTIVE. EXP-086 with box c_A(x) vs bulk c, stored data only. [model: Opus 5.5]"""
import os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, "exp081d_results")
JD = json.load(open(os.path.join(HERE, "exp081d_results.json"))); KS = [1, 1.5, 2]
def norm(k): W1, W2, P = int(2 * k), int(4 * k), int(4 * k); return 1.0 / (4 * P) / (1 / W1 - 1 / W2) / JD[str(k)]["kappa"]
R2 = json.load(open(os.path.join(D, "exp084", "result.json")))["Rn"]["2"]; ends = json.load(open(os.path.join(D, "exp085", "E.json")))["ends"]
sig = {}; cA = {}
for k in KS:
    for W in (int(2 * k), int(4 * k)):
        P = int(4 * k); sig[(W, P)] = np.array(json.load(open(os.path.join(D, "exp084c", f"c84_W{W}P{P}_n2.json")))["sigma"])
        cA[(W, P)] = np.array(json.load(open(os.path.join(D, "exp085c", f"G_W{W}P{P}.json")))["cA"]); assert len(cA[(W, P)]) == len(sig[(W, P)])
print("per geometry: sum sigma2, sum cA*sigma2, effective cA/c = sum(cA sigma2)/(c sum sigma2)   [c = each bracket end]")
for (W, P), s in sorted(sig.items(), key=lambda t: (t[0][1], t[0][0])):
    print(f"  W{W:2d}P{P:2d}: Sum s2 {s.sum():+.6f}  Sum cA s2 {np.dot(cA[(W, P)], s):+.6f}  " + "  ".join(f"cA/c[{t}] {np.dot(cA[(W, P)], s) / (c * s.sum()):.4f}" for t, c in ends.items()))
def dR(k, weight):
    W1, W2, P = int(2 * k), int(4 * k), int(4 * k); Ny = 4 * P
    return Ny * (weight(W1, P) - weight(W2, P)) * norm(k)          # n = 2: prefactor n/(2(n-1)) = 1
out = {}
for t, c in ends.items():
    bulk = {k: dR(k, lambda W, P: c * sig[(W, P)].sum()) for k in KS}; A = {k: dR(k, lambda W, P: np.dot(cA[(W, P)], sig[(W, P)])) for k in KS}
    gR = R2["2"] - R2["1"]; rb = -(bulk[2] - bulk[1]) / gR; ra = -(A[2] - A[1]) / gR
    print(f"[{t}] dR2 bulk {[round(bulk[k], 5) for k in KS]}  A {[round(A[k], 5) for k in KS]}")
    print(f"[{t}] parity-matched k = 1 -> 2: R2 grows {gR:+.5f}; counterterm/R2-growth ratio  bulk {rb:.4f}   A {ra:.4f}")
    out[t] = dict(bulk=bulk, A=A, ratio_bulk=rb, ratio_A=ra)
json.dump(out, open(os.path.join(D, "exp086b_result.json"), "w"), indent=1, default=float)
print("\nDESCRIPTIVE ONLY (EXP-086b): c_A at n = 2 is the assumption Fable question (2) asks about; this sharpens, does not settle.")
