"""EXP-071 (pre-registered in report.md): K-free. The SC module's own n->1 continuation C_line, applied to the free scalar's
Fredholm w_S, with the real-scalar counting factor 1/2, must reproduce kappa_free/C_T at d = 3.
KF0: C_line = d/dn sum_{q=1}^{n-1} g(q/n)|_1 (exact for g = cos(beta(a-1/2)), beta = 1, 2) to 1e-10.
KF1: kappa/C_T in [4.17358 - 1e-3, 4.17426 + 1e-3] (EXP-040 Impl-1/Impl-2 bracket, widened by 3x its spread); secondary: kappa
     vs CHL09 0.0397 (3 figures) to 5e-5. Ladder nt in {60, 120}, (ns, smax) in {(60, 6), (90, 7)}; spread reported.
KF-must-fail: counting factor 1 instead of 1/2 must give kappa/C_T outside the KF1 window (expected ~2x). [model: Opus 5.5]"""
import sys, os, math, time, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp071_sc import C_line
import exp044_det as X
def kap(nt, ns, smax, factor=0.5):
    U = np.linspace(math.log(1e-3), math.log(6.0), nt)
    C = np.array([-factor * C_line(lambda a: complex(X.w_scalar(math.exp(u), a)[0]).real, smax=smax, ns=ns) for u in U])
    return X.ratio("S", 3.0, U, C)
if __name__ == "__main__":
    ok0 = True
    for b in (1.0, 2.0):
        cl = C_line(lambda a: complex(np.cos(b * (a - 0.5))).real); ex = b / (2 * math.sin(b / 2)); r = abs(cl / ex - 1); ok0 &= r <= 1e-10
        print(f"KF0 beta={b}: C_line {cl:.13f} exact {ex:.13f} rel {r:.1e}")
    print(f"KF0 {'PASS' if ok0 else 'FAIL'}")
    vals = [kap(60, 60, 6.0), kap(120, 60, 6.0), kap(120, 90, 7.0)]; best = vals[-1]; spread = max(vals) - min(vals)
    ok1 = 4.17358 - 1e-3 <= best <= 4.17426 + 1e-3; kappa = best * 3 / (32 * math.pi ** 2)
    print(f"KF1 kappa/C_T = {best:.6f} (ladder {', '.join(f'{v:.6f}' for v in vals)}; spread {spread:.1e})  window [{4.17358-1e-3:.5f}, {4.17426+1e-3:.5f}] [{'PASS' if ok1 else 'FAIL'}]")
    print(f"    kappa = {kappa:.7f}  vs CHL09 0.0397: diff {kappa-0.0397:+.1e} [{'PASS' if abs(kappa-0.0397) <= 5e-5 else 'FAIL'}]")
    mf = kap(120, 90, 7.0, factor=1.0)
    print(f"KF-must-fail (counting factor 1): kappa/C_T = {mf:.6f} ratio to KF1 {mf/best:.4f} [{'FIRES' if not (4.17358-1e-3 <= mf <= 4.17426+1e-3) else 'does not fire'}]")
    json.dump(dict(KF0=bool(ok0), KF1=best, ladder=vals, kappa=kappa, mustfail=mf), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "exp071_results.json"), "w"), indent=1)
