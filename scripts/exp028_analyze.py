"""EXP-028 analysis (pre-registered in report.md; sealed toward quantum).
s(a, theta) = single-sector corner function from diracA<a> runs (normalisation s_A = (1/pi) Int dm m^2 Psi_reg, fixed for all a).
Per angle: s(a) = A2 a^2 + A4 a^4 [+ A6 a^6].  Cumulant corner functions: a_m relates as A2 = -c (2pi)^2 a2 / 2, A4 = +c (2pi)^4 a4 / 24,
so P1 (a4 has the sign of a2) <=> A4/A2 < 0, and P2 (kappa4/sigma4 < 3 pi) is read on A4's shape (normalisation-free).
GATE (must pass before A4 is read): A2's shape equals EMI to <= 1e-3 across the grid, and kappa2/sigma2 = 3 pi to <= 1e-3 (absolute,
primary extractor, which reproduces exact EMI to 2e-5)."""
import json, glob, os, sys, numpy as np
from math import pi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp028_extract import DEG, TH, kappa, sigma, K_VARIANTS, S_VARIANTS
D = os.path.dirname(os.path.abspath(__file__))
EMI = 1 + (pi - TH)/np.tan(TH)
PRIMARY = ("quartic 5-26.6", "eps^4 150-170")

def load():
    runs = {}
    for f in sorted(glob.glob(f"{D}/exp004_diracA*_result_n24_24_p15.0_t1.json")):
        r = json.load(open(f)); a = float(r["mode"][6:])
        if abs(a - 0.25) < 1e-12: continue            # the probe's a is not in the registered set
        runs[a] = (np.array(r["s"]), r["failures"], r["nodes"])
    return runs

def ratio_stats(A):
    vals = {(kv, sv): kappa(A, kv)/sigma(A, sv) for kv in K_VARIANTS for sv in S_VARIANTS}
    prim = vals[PRIMARY]; good = [v for (kv, sv), v in vals.items() if kv != "quad 5-15"]
    return prim, min(good), max(good)

def fit(runs, alist, powers):
    a = np.array(alist); X = np.vstack([a**p for p in powers]).T
    S = np.vstack([runs[x][0] for x in alist])            # (n_a, n_theta)
    coef, *_ = np.linalg.lstsq(X, S, rcond=None)
    return {p: coef[i] for i, p in enumerate(powers)}

if __name__ == "__main__":
    runs = load()
    alist = sorted(runs)
    print("runs:", ", ".join(f"a={a} (nodes {runs[a][2]}, failures {runs[a][1]})" for a in alist))
    print("\nTIER-2 (per run, not a verdict): shape of s(a,.)/s(a,90) vs EMI, and kappa/sigma of s(a,.)")
    for a in alist:
        s = runs[a][0]; shape = s/s[DEG.index(90)]
        prim, lo, hi = ratio_stats(s)
        print(f"   a={a}: max|shape/EMI - 1| = {np.max(np.abs(shape/EMI - 1)):.2e};  kappa/sigma = {prim:.6f} [{lo:.6f}, {hi:.6f}] vs 3pi = {3*pi:.6f}")
    if len(alist) < 2:
        print("\nfewer than two twists: a^2 and a^4 cannot be separated yet"); sys.exit(0)
    fits = {"A2,A4 all a": fit(runs, alist, [2, 4])}
    if len(alist) >= 3:
        fits["A2,A4 drop largest a"] = fit(runs, alist[:-1], [2, 4])
        fits["A2,A4,A6 all a"] = fit(runs, alist, [2, 4, 6])
    print("\nGATE on A2 (shape vs EMI <= 1e-3; kappa2/sigma2 = 3pi to <= 1e-3 absolute, primary extractor)")
    gate = True
    for name, c in fits.items():
        A2 = c[2]; shape = A2/A2[DEG.index(90)]; dev = np.max(np.abs(shape/EMI - 1)); prim, lo, hi = ratio_stats(A2)
        ok = dev <= 1e-3 and abs(prim - 3*pi) <= 1e-3
        gate &= ok if name == "A2,A4 all a" else True
        print(f"   {name:22s}: max|A2 shape/EMI - 1| = {dev:.2e};  kappa2/sigma2 = {prim:.6f} (variants {lo:.6f}..{hi:.6f}); |d| = {abs(prim-3*pi):.2e} -> {'PASS' if ok else 'FAIL'}")
    if not gate:
        print("\nGATE FAILED: nothing about A4 is read (as registered)."); sys.exit(0)
    print("\nA4 (read only because the gate passed)")
    for name, c in fits.items():
        A2, A4 = c[2], c[4]; rel = A4/A2
        prim, lo, hi = ratio_stats(A4)
        print(f"   {name:22s}: A4/A2 range over angles [{rel.min():+.4f}, {rel.max():+.4f}] -> P1 (A4/A2 < 0 everywhere) {'HOLDS' if np.all(rel < 0) else 'FAILS'};"
              f"  kappa4/sigma4 = {prim:.5f} (variants {lo:.5f}..{hi:.5f}) vs 3pi -> P2 {'HOLDS' if hi < 3*pi else ('FAILS' if lo > 3*pi else 'INCONCLUSIVE (straddles)')}")
        print(f"      A4 shape / EMI at 5,20,45,90,135,170 deg: {np.round((A4/A4[DEG.index(90)]/EMI)[[DEG.index(d) for d in (5,20,45,90,135,170)]], 4)}")
