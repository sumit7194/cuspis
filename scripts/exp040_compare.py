"""EXP-040 Part B: replication criteria, Impl-2 against Impl-1, and the t_min nuisance variant (registration in report.md)."""
import json, math, sys
import numpy as np
from scipy.interpolate import CubicSpline
from scipy.integrate import quad
from scipy.optimize import brentq
sys.path.insert(0, "scripts"); import exp040_impl2 as I2
J1 = json.load(open("scripts/exp040_impl1_L120.json")); J2 = json.load(open("scripts/exp040_impl2.json"))
S1 = np.array(J1["c_table"]["S"]); D1 = np.array(J1["c_table"]["D"]); ts1 = S1[:, 0]; lt1 = np.log(ts1)
def M1(tab, D, tail):
    sp = CubicSpline(lt1, tab[:, 1]); body = quad(lambda x: math.exp((D-2)*x)*float(sp(x)), lt1[0], lt1[-1], limit=400)[0]
    c0 = float(sp(lt1[0]))
    if tail == "const": return body + c0*ts1[0]**(D-2)/(D-2)
    lnts = lt1[0] - 1/(2*(c0 - 1/3))
    return body + quad(lambda u: math.exp((D-2)*u)*(1/3 + 1/(2*(u-lnts))), -200, lt1[0], limit=400)[0]
def r1(D, tail="const"):
    return (I2.P_D(D)*M1(S1, D, tail)/I2.CT_S(D), I2.P_D(D)*M1(D1, D, "const")/I2.CT_D(D))
U = np.array(J2["U"]); W = np.array(J2["W"]); cS = np.array(J2["tab"]["S"]["cinf"]); cD = np.array(J2["tab"]["D"]["cinf"])
def M2(cv, D, kind, tcut=None):
    keep = np.ones_like(U, bool) if tcut is None else (U >= math.log(tcut))
    body = float(np.sum((W*np.exp((D-2)*U)*cv)[keep]))
    u0 = U[keep][0]; c0 = cv[keep][0]; t0 = math.exp(u0)
    if kind == "D": return body + c0*t0**(D-2)/(D-2)
    lnts = u0 - 1/(2*(c0 - 1/3))
    return body + quad(lambda u: math.exp((D-2)*u)*(1/3 + 1/(2*(u-lnts))), -200, u0, limit=400)[0]
def r2(D, tcut=None):
    return (I2.P_D(D)*M2(cS, D, "S", tcut)/I2.CT_S(D), I2.P_D(D)*M2(cD, D, "D", tcut)/I2.CT_D(D))
print("Replication: kappa_D/C_T, Impl-2 vs Impl-1 (as run: constant scalar tail)")
ok = True
for D in (2.5, 2.75, 3.0, 3.25, 3.5, 4.0, 5.0, 6.0):
    a, b = r2(D), r1(D); tol = 0.01 if D == 2.5 else 0.003
    ds, dd = a[0]/b[0]-1, a[1]/b[1]-1; p = abs(ds) <= tol and abs(dd) <= tol; ok &= p
    print(f"  D={D}: scalar {a[0]:.5f} vs {b[0]:.5f} ({ds:+.2e});  Dirac {a[1]:.5f} vs {b[1]:.5f} ({dd:+.2e})  tol {tol}  {'PASS' if p else 'FAIL'}")
print("  value criterion:", "PASS" if ok else "FAIL")
def cross(fn):
    return [brentq(lambda D: fn(D)[0]/fn(D)[1]-1, 2.4, 3.2),
            brentq(lambda D: fn(D)[0]/I2.rE(D)-1, 2.4, 3.2),
            brentq(lambda D: fn(D)[1]/I2.rE(D)-1, 2.4, 3.2)]
c2 = cross(r2); c1c = cross(lambda D: r1(D, "const")); c1l = cross(lambda D: r1(D, "log")); c2t = cross(lambda D: r2(D, 1e-4))
for name, i in (("S/D", 0), ("S/E", 1), ("D/E", 2)):
    print(f"  crossing {name}: Impl-2 {c2[i]:.4f} | Impl-1 const {c1c[i]:.4f}, log {c1l[i]:.4f} | Impl-2 t_min=1e-4 {c2t[i]:.4f}"
          f"  -> |Impl-2 - Impl-1| = {abs(c2[i]-c1c[i]):.1e} {'PASS' if abs(c2[i]-c1c[i]) <= 0.01 else 'FAIL'}")
