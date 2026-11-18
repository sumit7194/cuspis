"""EXP-041 (registration in report.md): the EMI model as a fourth curve across spacetime dimension D.
C_T,EMI(d) = 2(d^2-1)(d-2) kappa/pi^2 (derived in the registration from FLP16 eq. planes); k_EMI from BFGLM26 eq. k_EMI.
Free fields from EXP-040 Impl-2 (scripts/exp040_impl2.json), Einstein exact."""
import json, math, sys
import numpy as np
import mpmath as mp
from scipy.optimize import brentq
import io, contextlib
sys.path.insert(0, "scripts")
with contextlib.redirect_stdout(io.StringIO()):                    # exp040_compare prints its own report on import
    import exp040_compare as X                                     # Impl-2 moments with tails (M2, r2) and closed forms (I2)
# Run-2 fix 1 (post-failure, E4): the scalar's small-t tail integral started at u = -200, which truncates exp((D-2)u)
# for D - 2 <~ 0.05. Re-define it with the lower limit at -max(200, 60/(D-2)); nothing else changes.
from scipy.integrate import quad as _quad
def _M2(cv, D, kind, tcut=None):
    U, W = X.U, X.W
    keep = np.ones_like(U, bool) if tcut is None else (U >= math.log(tcut))
    body = float(np.sum((W*np.exp((D-2)*U)*cv)[keep]))
    u0 = U[keep][0]; c0 = cv[keep][0]; t0 = math.exp(u0)
    if kind == "D": return body + c0*t0**(D-2)/(D-2)
    lnts = u0 - 1/(2*(c0 - 1/3)); lo = -max(200.0, 60.0/(D-2))
    return body + _quad(lambda u: math.exp((D-2)*u)*(1/3 + 1/(2*(u-lnts))), lo, u0, limit=2000)[0]
X.M2 = _M2
I2 = X.I2

def CT_emi(d): return 2 * (d * d - 1) * (d - 2) / math.pi ** 2          # units of kappa
def k_emi(d):  return 2 * math.pi ** ((d - 2) / 2) * math.gamma((d - 2) / 2) / math.gamma(d - 2)
def rEMI(D):   return k_emi(D) / CT_emi(D)

print("=== E1: C_T,EMI against BFGLM26's three published values (units kappa/pi^2) ===")
for d, ref in ((3, 16), (4, 60), (5, 144)):
    v = CT_emi(d) * math.pi ** 2; print(f"  d={d}: {v:.15g} vs {ref}  {'PASS' if abs(v/ref-1) < 1e-12 else 'FAIL'}")
print("=== E2: k_EMI at d = 3, 4, 5 (units kappa) ===")
for d, ref in ((3, 2 * math.pi), (4, 2 * math.pi), (5, math.pi ** 2 / 2)):
    v = k_emi(d); print(f"  d={d}: {v:.15g} vs {ref:.15g}  {'PASS' if abs(v/ref-1) < 1e-12 else 'FAIL'}")
print(f"=== E3: kappa/C_T at D = 3: {rEMI(3):.15g} vs pi^3/8 = {math.pi**3/8:.15g}  {'PASS' if abs(rEMI(3)/(math.pi**3/8)-1) < 1e-12 else 'FAIL'}")

print("=== E4: pinning, (D-2) kappa/C_T near D = 2 (EMI limit 2 pi^2/3 = %.6f) ===" % (2 * math.pi ** 2 / 3))
for D in (2.001, 2.01, 2.05):
    s, d_ = X.r2(D); e = I2.rE(D)
    print(f"  D={D}: EMI {(D-2)*rEMI(D):.5f}  Einstein {(D-2)*e:.5f}  scalar {(D-2)*s:.5f}  Dirac {(D-2)*d_:.5f}")

print("=== E5: second-order EMI coefficient, d = 3, f = cos y (kappa = 1), finite part of a cutoff integral ===")
mp.mp.dps = 30
# direct expansion before any integration by parts (y-averaged): A(delta) = 2 int_delta^inf [cos u/(2u^2) - (1-cos u)/u^4] du
# formula after integration by parts:                         B(delta) = (d-1)(d-2) * 2 int_delta^inf (1-cos u)/u^4 du, d = 3
# Run-2 fix 2 (post-failure, E5): the [10, inf) pieces now use mp.quadosc (oscillatory tail) instead of mp.quad.
fA = lambda u: mp.cos(u) / (2 * u ** 2) - (1 - mp.cos(u)) / u ** 4
fB = lambda u: (1 - mp.cos(u)) / u ** 4
A = lambda dl: 2 * (mp.quad(fA, [dl, 1, 10]) + mp.quadosc(fA, [10, mp.inf], omega=1))
B = lambda dl: 2 * 2 * (mp.quad(fB, [dl, 1, 10]) + mp.quadosc(fB, [10, mp.inf], omega=1))
dls = [mp.mpf(1) / 2 ** k for k in range(6, 12)]
diff = [A(dl) - B(dl) for dl in dls]
# fit diff = p/dl^3 + r/dl + s + t dl + w dl^2 ; the delta^0 coefficient s must vanish (the |q|^3 term is non-local)
M = mp.matrix([[1 / dl ** 3, 1 / dl, 1, dl, dl ** 2, dl ** 3] for dl in dls]); sol = mp.lu_solve(M, mp.matrix(diff))
print(f"  delta^0 coefficient of A - B: {mp.nstr(sol[2], 6)}  (must be 0; finite part of B alone: ", end="")
Bv = [B(dl) for dl in dls]; solB = mp.lu_solve(M, mp.matrix(Bv)); print(f"{mp.nstr(solB[2], 8)}; pi/3 = {mp.nstr(mp.pi/3, 8)})")
print(f"  E5 {'PASS' if abs(sol[2]) < 1e-8 else 'FAIL'}")

print("\n=== EMI across D: kappa/C_T and ratios ===")
print("   D      EMI      scalar    Dirac    Einstein | EMI/S   EMI/D   EMI/E")
for D in (2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 4.0, 4.5, 5.0, 6.0):
    s, d_ = X.r2(D); e = I2.rE(D); m = rEMI(D)
    print(f"  {D:4.2f} {m:9.5f} {s:9.5f} {d_:9.5f} {e:9.5f} | {m/s:6.4f}  {m/d_:6.4f}  {m/e:6.4f}")
print("\n=== crossings of EMI with each trio member in (2.02, 6) ===")
G = np.linspace(2.02, 6.0, 400)
res = {}
for name, f in (("EMI=scalar", lambda D: rEMI(D) / X.r2(D)[0]), ("EMI=Dirac", lambda D: rEMI(D) / X.r2(D)[1]),
                ("EMI=Einstein", lambda D: rEMI(D) / I2.rE(D))):
    v = np.array([math.log(f(D)) for D in G]); idx = np.where(np.sign(v[:-1]) * np.sign(v[1:]) < 0)[0]
    roots = [brentq(lambda D: math.log(f(D)), G[i], G[i + 1]) for i in idx]
    res[name] = roots; print(f"  {name}: {[round(r, 4) for r in roots]}")
json.dump(res, open("scripts/exp041_crossings.json", "w"), indent=1)
