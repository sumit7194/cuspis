"""EXP-040 Part C, post-hoc diagnostics (labelled as such in report.md): (i) why P1 fired: c against its one-particle
form at large t on the Impl-2 table; (ii) P1 restricted to t <= 6; (iii) C3 breakdown of non-crossing toy pairs."""
import json, math, itertools, sys
import numpy as np
from scipy.special import k1
sys.path.insert(0, "scripts"); import exp040_partC as C
J = json.load(open("scripts/exp040_impl2.json"))
U = np.array(J["U"]); cS = np.array(J["tab"]["S"]["cinf"]); cD = np.array(J["tab"]["D"]["cinf"]); t = np.exp(U)
print("(i) large t: c / one-particle form, and the size-to-size spread of the raw c (a noise proxy)")
for i in np.where(t > 4.5)[0]:
    sS = np.ptp(J["tab"]["S"]["sizes"][i]); sD = np.ptp(J["tab"]["D"]["sizes"][i])
    print(f"  t={t[i]:7.3f}  c_S/(tK1/4) = {cS[i]/(t[i]/4*k1(2*t[i])):10.4f}   c_D/(tK1/2) = {cD[i]/(t[i]/2*k1(2*t[i])):10.4f}   c_S = {cS[i]:.2e}")
m = t <= 6.0
rat = cD[m] / cS[m]
print(f"(ii) P1 restricted to t <= 6 ({m.sum()} nodes): monotone increasing {'YES' if np.all(np.diff(rat) > 0) else 'NO'}; "
      f"range {rat[0]:.4f} -> {rat[-1]:.4f}; max {rat.max():.4f} (2 is the one-particle limit)")
print("(iii) C3 toy pairs: where is r relative to 1?")
S = [C.toy(1, a, p) for a in C.TAUS for p in C.PS]; D = [C.toy(2, a, p) for a in C.TAUS for p in C.PS]
cnt = dict(above=0, below=0, cross=0); r3 = []
for (Ms, _), (Md, _) in itertools.product(S, D):
    lnr = np.array([math.log((x - 1) * Ms(x) / Md(x)) for x in C.DG])
    sel = C.DG < 4
    if np.all(lnr[sel] > 0): cnt["above"] += 1
    elif np.all(lnr[sel] < 0): cnt["below"] += 1
    else: cnt["cross"] += 1
    r3.append(math.exp(np.interp(3, C.DG, lnr)))
print(f"  r > 1 on all of (2.02, 4): {cnt['above']};  r < 1 on all: {cnt['below']};  changes sign: {cnt['cross']}")
r3 = np.array(r3); print(f"  r(3) over the 144 pairs: min {r3.min():.3f}, median {np.median(r3):.3f}, max {r3.max():.3f}")
print(f"  initial slope d ln r/dD at D = 2.02: negative in {sum(1 for (Ms,_),(Md,_) in itertools.product(S,D) if math.log(((2.03-1)*Ms(2.03)/Md(2.03))/((2.02-1)*Ms(2.02)/Md(2.02))) < 0)} of 144 pairs")
