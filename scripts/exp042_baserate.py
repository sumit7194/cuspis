"""EXP-042 (Bridge rule, adopted in EXP-041): toy-ensemble base rate for a fifth curve's crossings with the existing four
(scalar, Dirac, Einstein, EMI) landing in the window [2.75, 2.95]. Ensemble = EXP-040 Part C's 24 toy curves (12 scalar-law,
12 Dirac-law), unchanged. Computed BEFORE any fifth curve exists."""
import io, contextlib, math, sys, json
import numpy as np
from scipy.optimize import brentq
sys.path.insert(0, "scripts")
with contextlib.redirect_stdout(io.StringIO()):
    import exp041_emi as E          # brings X (EXP-040 Impl-2 moments, tail-fixed) and rEMI
import exp040_partC as C
X, I2 = E.X, E.I2
REAL = {"scalar": lambda D: X.r2(D)[0], "Dirac": lambda D: X.r2(D)[1], "Einstein": I2.rE, "EMI": E.rEMI}
G = np.linspace(2.02, 6.0, 300)
realv = {k: np.array([f(D) for D in G]) for k, f in REAL.items()}
LO, HI = 2.75, 2.95
toys = []
for law, Np, CT in (("scalar-law", 1, I2.CT_S), ("Dirac-law", 2, I2.CT_D)):
    for tau in C.TAUS:
        for p in C.PS:
            M, _ = C.toy(Np, tau, p)
            toys.append((f"{law} tau={tau} p={p}", np.array([I2.P_D(D) * M(D) / CT(D) for D in G])))
allc, n_any, n_all_in, per = [], 0, 0, []
for name, tv in toys:
    cs = []
    for k, rv in realv.items():
        v = np.log(tv / rv); idx = np.where(np.sign(v[:-1]) * np.sign(v[1:]) < 0)[0]
        cs += [float(G[i] - v[i] * (G[i + 1] - G[i]) / (v[i + 1] - v[i])) for i in idx]
    allc += cs
    if cs:
        n_any += 1; inw = [LO <= c <= HI for c in cs]; per.append(np.mean(inw))
        n_all_in += all(inw)
allc = np.array(allc)
print(f"toy curves: {len(toys)}; with >= 1 crossing against the four in (2.02, 6): {n_any}")
print(f"  P(all of a curve's crossings lie in [{LO}, {HI}] | it crosses at all) = {n_all_in}/{n_any} = {n_all_in/max(n_any,1):.3f}")
print(f"  per-crossing rate: {np.mean((allc>=LO)&(allc<=HI)):.3f} of {len(allc)} crossings lie in the window")
print(f"  crossing locations: quartiles {np.percentile(allc,[25,50,75]).round(3)}, min {allc.min():.3f}, max {allc.max():.3f}")
print(f"  naive uniform rate on (2, 4) for a 0.2-wide window: 0.100")
json.dump(dict(n_toys=len(toys), n_any=n_any, n_all_in=n_all_in, crossings=allc.tolist()), open("scripts/exp042_baserate.json", "w"))
