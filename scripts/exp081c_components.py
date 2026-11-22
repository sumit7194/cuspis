"""EXP-081c POST HOC, descriptive (Bridge 2026-11-22): decomposition of R by component (t0, T_sad, C) for the refinement pair
(4,8)@P8 b8 vs (2,4)@P4 b4, and the (2,4)@P8 b8 / (2,4)@P8 b4 pairs; free side alongside. No new runs: 081b checkpoints
(W2/W4 geometries) and the 081c W8P8 checkpoint. R_X = -(X_W1 - X_W2)/2 / Ny / (1/W1 - 1/W2) / kappa, X in {t0, tsad, C}
(S = (t0 + tsad + C)/2), so R = R_t0 + R_tsad + R_C. [model: Opus 5.5]"""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import exp081b_run as R
x, w = np.polynomial.legendre.leggauss(12); NODES = []
for lo, hi in zip((0.0, 0.5, 1.5, 3.0), (0.5, 1.5, 3.0, 6.0)):
    for xi, wi in zip(x, w):
        s = 0.5 * (hi - lo) * (xi + 1) + lo; NODES.append((s, 0.5 * (hi - lo) * wi * np.pi / np.cosh(np.pi * s) ** 2))
def comps(W, P, B):
    tag = f"sigma_W{W}_P{P}_box{B}_c2_cp12_sc3.0_dd0_ckpt.json"
    f = os.path.join(HERE, "exp081c_results" if W == 8 else "exp081b_results", tag); d = json.load(open(f))
    gv = lambda s: d[f"g|{s:.15f}"][0] if isinstance(d[f"g|{s:.15f}"], list) else d[f"g|{s:.15f}"]
    return dict(t0=d["t0"], tsad=d["tsad"], C=sum(wt * gv(s) for s, wt in NODES))
out = {}
for lab, (W1, W2, P, B) in {"(2,4)@P4b4": (2, 4, 4, 4), "(2,4)@P8b4": (2, 4, 8, 4), "(2,4)@P8b8": (2, 4, 8, 8), "(4,8)@P8b8": (4, 8, 8, 8),
                            "(2,8)@P8b8": (2, 8, 8, 8)}.items():
    Ny = 4 * P; kap = R.pair(lambda W, P_, **kw: R.free(W, P_, **kw), P, W1=W1, W2=W2, Wbox=B)
    a, b = comps(W1, P, B), comps(W2, P, B)
    r = {k: -(a[k] - b[k]) / 2 / Ny / (1 / W1 - 1 / W2) / kap for k in a}; r["R"] = sum(r.values()); r["kappa"] = kap
    r["raw"] = dict(W1=a, W2=b); out[lab] = r
    print(f"{lab}: R {r['R']:+.4f} = t0 {r['t0']:+.4f} + T_sad {r['tsad']:+.4f} + C {r['C']:+.4f}   (kappa {kap:.6f})")
d = {k: out["(4,8)@P8b8"][k] - out["(2,4)@P4b4"][k] for k in ("t0", "tsad", "C", "R")}
print("refinement shift (4,8)@P8b8 - (2,4)@P4b4: " + ", ".join(f"{k} {v:+.4f}" for k, v in d.items()))
d2 = {k: out["(4,8)@P8b8"][k] - out["(2,4)@P8b8"][k] for k in ("t0", "tsad", "C", "R")}
print("width shift at fixed lattice (4,8) - (2,4) @P8b8: " + ", ".join(f"{k} {v:+.4f}" for k, v in d2.items()))
out["shift_refinement"] = d; out["shift_width_fixed_lattice"] = d2
json.dump(out, open(os.path.join(HERE, "exp081c_components.json"), "w"), indent=1)
