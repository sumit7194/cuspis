"""EXP-093 (registered f874dac) G_b(8) item: Y_A, Y_bulk at P = 8 with exp089_wall.row's formulas (Y part only); KA: same code reproduces
G_b(4), G_b(6) of exp089_wall.json bitwise. [model: Opus 5.5]"""
import os, sys, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); D = os.path.join(HERE, "exp081d_results")
import exp081b_run as Rn
c = -0.11410550636913405; FAIL = []
def check(nm, ok, det=""):
    print(f"{nm:62s} {'PASS' if ok else 'FAIL'}  {det}", flush=True)
    if not ok: FAIL.append(nm)
def ygb(P):                                                       # verbatim from exp089_wall.row (Y part)
    Ny = 4 * P; kap = Rn.pair(lambda W, P_, **kw: Rn.free(W, P_, **kw), P, W1=2, W2=4, Wbox=P); nm = 1.0 / (Ny * (1 / 2 - 1 / 4) * kap)
    g2, g4 = (json.load(open(os.path.join(D, "exp085c", f"G_W{W}P{P}.json"))) for W in (2, 4))
    YA = -(g2["X_cA"] - g4["X_cA"]) * nm; YB = -(c / 2) * (g2["Sigma3D"] - g4["Sigma3D"]) * nm
    return dict(P=P, kappa=kap, norm=nm, YA=YA, YB=YB, Gb=YB - YA, failed=[g2.get("failed"), g4.get("failed")])
ref = json.load(open(os.path.join(D, "exp089_wall.json")))
for P, key in ((4, "r4"), (6, "r6")):
    r = ygb(P); check(f"KA: G_b({P}) reproduces exp089_wall.json bitwise", r["Gb"] == ref[key]["Gb"] and r["norm"] == ref[key]["norm"], f"{r['Gb']!r}")
r8 = ygb(8); check("G_W2P8 / G_W4P8: no failed entries", not any(r8["failed"]), str(r8["failed"]))
if FAIL: print("STOP: controls failed -> no grading"); sys.exit(1)
g = r8["Gb"]; p1, p2 = 0.91 <= g <= 1.03, 0.85 <= g <= 1.09
print(f"\nP = 8: kappa {r8['kappa']:.6f} norm {r8['norm']:.6f}  Y_A {r8['YA']:.4f}  Y_bulk {r8['YB']:.4f}  G_b(8) = {g:.4f}")
print(f"EXP-093 item G_b(8): sealed 0.97 +- 0.06 -> {'PASS' if p1 else 'FAIL'} (+-1 sigma [0.91, 1.03]); +-2 sigma [0.85, 1.09]: {'inside' if p2 else 'outside'}")
print(f"   G_b drop 6 -> 8 = {ref['r6']['Gb'] - g:+.4f} (f INCONCLUSIVE if < 0.285)")
json.dump(dict(r8=r8, Gb_pass_1s=p1, Gb_in_2s=p2, failed=FAIL), open(os.path.join(D, "exp093_gb8.json"), "w"), indent=1, default=float)
