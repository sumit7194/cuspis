"""EXP-040 Part B: hold Implementation 1 to control K1 ([CH09] Table, kappa per degree of freedom, D = 3..6), with its
constant small-t tail (as run) and the log-matched scalar tail (nuisance variant)."""
import json, math, sys
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import quad
sys.path.insert(0, "scripts"); import exp040_impl1_dim_spread as I
J = json.load(open("scripts/exp040_impl1_L120.json"))
S = np.array(J["c_table"]["S"]); Dd = np.array(J["c_table"]["D"]); ts = S[:, 0]; lt = np.log(ts)
def M(tab, D, tail):
    sp = CubicSpline(lt, tab[:, 1]); body = quad(lambda x: math.exp((D - 2) * x) * float(sp(x)), lt[0], lt[-1], limit=400)[0]
    c0 = float(sp(lt[0]))
    if tail == "const": return body + c0 * ts[0] ** (D - 2) / (D - 2)
    lnts = lt[0] - 1 / (2 * (c0 - 1 / 3))
    return body + quad(lambda u: math.exp((D - 2) * u) * (1/3 + 1/(2*(u - lnts))), -200, lt[0], limit=400)[0]
CH = {3: (3.97e-2, 3.61e-2), 4: (5.54e-3, 5.38e-3), 5: (1.31e-3, 1.30e-3), 6: (4.08e-4, 4.06e-4)}
ulp = lambda v: 0.5 * 10 ** (math.floor(math.log10(v)) - 2)
for tail in ("const", "log"):
    ok = True
    for D, (b, f) in CH.items():
        kb = I.pref(D) * M(S, D, tail); kf = I.pref(D) * M(Dd, D, "const") / 2
        pb = abs(kb - b) <= ulp(b); pf = abs(kf - f) <= ulp(f); ok &= pb and pf
        print(f"[{tail} scalar tail] D={D}: boson {kb:.6e} vs {b:.2e} {'PASS' if pb else 'FAIL'}; fermion/Majorana {kf:.6e} vs {f:.2e} {'PASS' if pf else 'FAIL'}")
    print(f"  K1 for Impl-1 with {tail} tail:", "PASS" if ok else "FAIL")
