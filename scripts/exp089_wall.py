"""EXP-089 (ii) wall test (registration notes/EXP-089_registration.md): fixed strips (2, 4), walls P = 4 -> P' = 6.
R via exp081d_analyze.S_T (the registered R(k) path) and exp081b_run.pair (free kappa); Y_A, Sigma3D from 085c GEOM files. [model: Opus 5.5]"""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); D = os.path.join(HERE, "exp081d_results")
import exp081d_analyze as AN, exp081b_run as Rn
c = -0.11410550636913405; FAIL = []
def check(nm, ok, det=""):
    print(f"{nm:60s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
def ck(W, P):
    for d in (D, os.path.join(HERE, "exp081c_results")):
        f = os.path.join(d, f"sigma_W{W}_P{P}_box{P}_c2_cp12_sc3.0_dd0_ckpt.json")
        if os.path.exists(f):
            st = json.load(open(f))
            if "n1c" in st: return st
    raise FileNotFoundError(f"no n1c checkpoint for W{W}P{P}")
def row(P):
    Ny = 4 * P; kap = Rn.pair(lambda W, P_, **kw: Rn.free(W, P_, **kw), P, W1=2, W2=4, Wbox=P); nm = 1.0 / (Ny * (1 / 2 - 1 / 4) * kap)
    s2, s4 = AN.S_T(ck(2, P)), AN.S_T(ck(4, P)); g2, g4 = (json.load(open(os.path.join(D, "exp085c", f"G_W{W}P{P}.json"))) for W in (2, 4))
    R = -(s2["S_T0"] - s4["S_T0"]) * nm; YA = -(g2["X_cA"] - g4["X_cA"]) * nm; YB = -(c / 2) * (g2["Sigma3D"] - g4["Sigma3D"]) * nm
    return dict(P=P, kappa=kap, norm=nm, R=R, YA=YA, YB=YB, rhoA=R - YA, Gb=YB - YA)
r4 = row(4)
print(f"P=4: R {r4['R']:.4f} Y_A {r4['YA']:.4f} Y_bulk {r4['YB']:.4f} rho_A {r4['rhoA']:.4f} G_b {r4['Gb']:.4f} (kappa {r4['kappa']:.6f})")
check("KA P=4 reproduces Fable's stored-number values to 1e-4", all(abs(r4[k] - v) <= 1e-4 for k, v in (("R", 2.2552), ("YA", 1.9817), ("YB", 4.4737), ("rhoA", 0.2735), ("Gb", 2.4920))))
r6 = row(6)
print(f"P=6: R {r6['R']:.4f} Y_A {r6['YA']:.4f} Y_bulk {r6['YB']:.4f} rho_A {r6['rhoA']:.4f} G_b {r6['Gb']:.4f} (kappa {r6['kappa']:.6f})")
dG = r4["Gb"] - r6["Gb"]; f = -(r6["rhoA"] - r4["rhoA"]) / dG if dG != 0 else float("nan")
print(f"\nG_b(4) - G_b(6) = {dG:+.4f}  (INCONCLUSIVE if < 0.5);  f = {f:+.4f}")
if dG < 0.5: lab = "INCONCLUSIVE (G_b(4) - G_b(6) < 0.5)"
elif f > 0.5: lab = "A WRONG (f > 0.5)" + ("; bulk better (f in [0.7, 1.3])" if 0.7 <= f <= 1.3 else "")
elif 0.3 < f <= 0.5: lab = "neither (f in (0.3, 0.7)); P-extrapolation needed"
else: lab = "A not wrong"
print(f"EXP-089 (ii) READING: {lab};  PRIMARY band [-0.3, 0.3]: {'inside' if -0.3 <= f <= 0.3 else 'outside'};  OUTER [-0.5, 0.5]: {'inside' if -0.5 <= f <= 0.5 else 'outside'};  controls {'PASS' if not FAIL else FAIL}")
json.dump(dict(r4=r4, r6=r6, f=f, dG=dG, reading=lab, failed=FAIL), open(os.path.join(D, "exp089_wall.json"), "w"), indent=1, default=float)
sys.exit(1 if FAIL else 0)
