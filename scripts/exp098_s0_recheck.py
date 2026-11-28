"""EXP-098 stage 0: an independent recomputation of the pair ratios (a second implementation of the pair formula) and the
sigma/free decomposition of D. Descriptive; not a registered reading. [model: Opus 5.5]
It shares only exp081d_analyze.S_T (checkpoint -> S) and the stored JSON inputs with exp098_3w.py."""
import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); os.chdir(HERE)
import exp081d_analyze as A
def ckp(W, P, suf=""):
    for d in ("exp081d_results", "exp081c_results"):
        f = f"{d}/sigma_W{W}_P{P}_box{P}_c2_cp12_sc3.0_dd0{suf}_ckpt.json"
        if os.path.exists(f) and "n1c" in json.load(open(f)): return f
def S(W, P, suf=""): return A.S_T(json.load(open(ckp(W, P, suf))), None)["S_T0"]
def F(W, P): return json.load(open(f"exp081b_results/free_W{W}_P{P}_box{P}_c2.json"))["S"]
r = json.load(open("exp081d_results/exp087_referee_W8P8.json")); d8 = r["on_1e-5"] - r["off_1e-5"]
J = json.load(open("exp081d_results/exp098_stage0.json"))["readings"]; bad = 0
for k, (a, c, b) in {1: (2, 3, 4), 2: (4, 6, 8)}.items():
    P = 4 * k; Ny = 4 * P; X = {a: S(a, P), c: S(c, P, "_098"), b: S(b, P)}; Fs = {W: F(W, P) for W in (a, c, b)}
    if k == 2: X[8] += 0.5 * d8                                   # Delta(W3) = Delta(W1) = 0; Delta(8) = d8 (as registered)
    sl = lambda Z, x, y: -(Z[x] - Z[y]) / Ny / (1 / x - 1 / y)
    R13, R32 = sl(X, a, c) / sl(Fs, a, c), sl(X, c, b) / sl(Fs, c, b); Dk = R13 - R32
    ok = abs(Dk - J[str(k)]["D_T0"]) <= 1e-12 * abs(Dk); bad += not ok
    ds = (sl(X, a, c) - sl(X, c, b)) / sl(X, a, b); df = (sl(Fs, a, c) - sl(Fs, c, b)) / sl(Fs, a, b)
    print(f"k={k}: R13 {R13:.9f} R32 {R32:.9f} D {Dk:+.9f} vs exp098_3w {J[str(k)]['D_T0']:+.9f} -> {'MATCH' if ok else 'MISMATCH'}")
    print(f"      sigma slope (W1,W3) {sl(X,a,c):.6f} (W3,W2) {sl(X,c,b):.6f} (W1,W2) {sl(X,a,b):.6f}: relative drift {ds:+.3f}")
    print(f"      free  slope (W1,W3) {sl(Fs,a,c):.6f} (W3,W2) {sl(Fs,c,b):.6f} (W1,W2) {sl(Fs,a,b):.6f}: relative drift {df:+.3f}")
print("recheck:", "PASS" if bad == 0 else "FAIL"); sys.exit(1 if bad else 0)
