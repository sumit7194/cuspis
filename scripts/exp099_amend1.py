"""EXP-099 amendment 1: B(g = 8P, hT in {P, 2P, 4P}, Ny = 4P), one variable from B_g8P. [model: Opus 5.5]"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.argv = ["x"]; import importlib.util
spec = importlib.util.spec_from_file_location("e99", os.path.join(HERE, "exp099_free.py"))   # NOT executed; only the S() definition is copied below
def S(W, gL, gR, hT, Ny):
    import sigma3d as S3
    return float(S3.FreeStrip(gL + W + gR, 2 * hT, Ny, list(range(gL, gL + W)), hT - 1).S(cpts=12).real)
J = json.load(open(os.path.join(HERE, "exp081d_results", "exp099_free.json"))); out = {}; bad = 0
def kap(a, b, Sa, Sb, Ny): return -(Sa - Sb) / Ny / (1 / a - 1 / b)
for k in (1, 2, 3):
    P = 4 * k; W1, W3, W2 = P // 2, 3 * P // 4, P; out[str(k)] = {}
    for m in (1, 2, 4):
        s = {W: S(W, 8 * P, 8 * P, m * P, 4 * P) for W in (W1, W3, W2)}
        k13, k32, k12 = kap(W1, W3, s[W1], s[W3], 4 * P), kap(W3, W2, s[W3], s[W2], 4 * P), kap(W1, W2, s[W1], s[W2], 4 * P)
        df = (k13 - k32) / k12; out[str(k)][f"hT{m}P"] = dict(kappa13=k13, kappa32=k32, kappa12=k12, df=df)
        if m == 1:
            ref = J["readings"][str(k)]["B_g8P"]; ok = (k13, k32, k12) == (ref["kappa13"], ref["kappa32"], ref["kappa12"]); bad += not ok
            print(f"control k={k}: B(8P, hT=P) == stored B_g8P bitwise: {'PASS' if ok else 'FAIL'}")
        print(f"k={k} B(g=8P, hT={m}P, Ny=4P): df {df:+.4f}  [{k13:.6f} / {k32:.6f} / {k12:.6f}]   (E: {J['readings'][str(k)]['E']['df']:+.4f})")
pred = all(abs(abs(out[str(k)]["hT4P"]["df"]) - J["E_absdf"][k - 1]) <= 0.01 for k in (1, 2, 3))
mono = all(abs(out[str(k)]["hT1P"]["df"]) >= abs(out[str(k)]["hT2P"]["df"]) >= abs(out[str(k)]["hT4P"]["df"]) for k in (1, 2, 3))
print(f"prediction |df(hT=4P)| == |df_E| within 0.01 at every k: {'HELD' if pred else 'FAILED'}; monotone in hT: {mono}")
json.dump(dict(amendment=1, readings=out, prediction_held=pred, monotone=mono), open(os.path.join(HERE, "exp081d_results", "exp099_amend1.json"), "w"), indent=1)
sys.exit(1 if bad else 0)
