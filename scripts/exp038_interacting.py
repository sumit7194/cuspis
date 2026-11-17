"""EXP-038 (pre-registered in report.md): P3 / A5' beyond free fields.

Part B -- holographic CFT (Einstein, AdS4) at O(N^2).  For two sectors of half-width eta, centres theta apart, RT picks
the smaller of  S_dis = 2 S(2 eta)  and  S_con = S(theta - 2 eta) + S(theta + 2 eta)  (Mozaffar-Mollabashi-Omidi 1511.00244
eq. 3.2, in our variables Omega = 2 eta, omega = theta - 2 eta).  Area terms are identical (same four rays), so the log
coefficients decide: disconnected <=> 2 a(2 eta) >= a(theta - 2 eta) + a(theta + 2 eta) [a(x) = a(2 pi - x)], and then
I = 0 identically, so i_G = 0.  Output: eta_c(theta), two implementations of a(Omega).
Part C -- exponent law  i_G ~ eta^{2(2 Delta - 1)}  tested out of sample in the scale-invariant Gaussian family (EXP-035
machinery) at Delta = 0.6 (alpha = 0.8) and Delta = 0.9 (alpha = 0.2)."""
import json, os, sys, time
import numpy as np
from math import pi
from scipy.integrate import quad
from scipy.optimize import brentq
import exp001_measure as e1
import exp035_cylinder_mi as e35

D0 = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D0, "exp038_partC.json")

def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)

# ---------------- Part B ----------------
def a1(om):                       # implementation 1: Hirata-Takayanagi via exp001 (EXP-001, verified), units of C_T
    om = 2 * pi - om if om > pi else om
    return 0.0 if abs(om - pi) < 1e-13 else e1.aE_over_CT(om)

def omega_direct(hs):             # implementation 2: Omega(h*) from the conserved quantity (MMO15 eq. 2.5), own derivation
    c = (1 + hs ** 2) ** 0.5 / hs ** 2
    # h'^2 = (1+h^2)^2/(c^2 h^4) - (1+h^2);  Omega/2 = int_0^{h*} dh / |h'|;  substitute h = h* sin(t) to soften the turning point
    def integrand(t):
        h = hs * np.sin(t); dh = hs * np.cos(t)
        hp2 = (1 + h * h) ** 2 / (c * c * h ** 4) - (1 + h * h)
        return dh / np.sqrt(hp2) if hp2 > 0 else 0.0
    return 2 * quad(integrand, 0, pi / 2, limit=400, epsabs=1e-13, epsrel=1e-12)[0]

def a2(om):                       # a(Omega) via h* from implementation 2 and MMO15 eq. 2.7 (normalised by C_T: a/C_T = (pi^3/6) f)
    om = 2 * pi - om if om > pi else om
    if abs(om - pi) < 1e-13: return 0.0
    hs = brentq(lambda h: omega_direct(h) - om, 1e-4, 1e4, xtol=1e-14)
    f = quad(lambda y: 1 - np.sqrt((1 + hs * hs * (1 + y * y)) / (2 + hs * hs * (1 + y * y))), 0, np.inf, limit=400, epsrel=1e-12)[0]
    return pi ** 3 / 6 * f            # MMO (2.7) with h* = 1/g0 is HT (5.x) with z = y; only the Omega(h*) map is independent

def eta_c(theta, a):
    g = lambda eta: 2 * a(2 * eta) - a(theta - 2 * eta) - a(theta + 2 * eta)
    lo, hi = 1e-3, min(theta, 2 * pi - theta) / 2 - 1e-3
    return brentq(g, lo, hi, xtol=1e-12)

def partB():
    for om in (0.3, 1.0, pi / 2, 2.5):
        x, y = a1(om), a2(om)
        log(f"B two implementations a(Omega={om:.4f})/C_T: HT {x:.12f}  direct-ODE {y:.12f}  rel {abs(x / y - 1):.1e} [{'PASS' if abs(x / y - 1) < 1e-8 else 'FAIL'}]")
    res = {}
    for th in (pi, pi / 2, 2 * pi / 3, pi / 3):
        e_1, e_2 = eta_c(th, a1), eta_c(th, a2)
        res[th] = e_1
        log(f"B eta_c(theta={np.degrees(th):.0f} deg) = {e_1:.10f} (impl 2: {e_2:.10f}); sector opening 2 eta_c = {np.degrees(2 * e_1):.4f} deg")
    log(f"B control: eta_c(180) - pi/4 = {res[pi] - pi / 4:.2e} [{'PASS' if abs(res[pi] - pi / 4) < 1e-9 else 'FAIL'}]")
    return res

# ---------------- Part C ----------------
PLAN = ((1e-3, (32, 64)), (1e-4, (32, 64)), (1e-5, (16, 32)))
def partC():
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    for al in (0.8, 0.2):
        for eta, nps in PLAN:
            for n_p in nps:
                k = f"a{al}_e{eta}_np{n_p}"
                if k in res: continue
                t0 = time.time(); v, M, ee = e35.iG(al, eta, n_p, 96)
                res[k] = {"i90": v[0], "i180": v[1], "M": M}; json.dump(res, open(OUT, "w"), indent=0)
                log(f"  C {k}: M={M} ({time.time() - t0:.0f} s)")
        if f"a{al}_e0.001_np64_q48" not in res:
            v, M, ee = e35.iG(al, 1e-3, 64, 48); res[f"a{al}_e0.001_np64_q48"] = {"i90": v[0], "i180": v[1]}; json.dump(res, open(OUT, "w"), indent=0)
    for al in (0.8, 0.2):
        D = (2 - al) / 2; p_pred = 2 * (2 * D - 1); tol = 0.15 if al == 0.8 else 0.10
        for th in ("i90", "i180"):
            q = abs(res[f"a{al}_e0.001_np64_q48"][th] / res[f"a{al}_e0.001_np64"][th] - 1)
            dr = [abs(res[f"a{al}_e{e}_np{a}"][th] / res[f"a{al}_e{e}_np{b}"][th] - 1) for e, (a, b) in PLAN]
            g = lambda e: res[f"a{al}_e{e}_np{dict(PLAN)[e][1]}"][th]
            p1 = np.log(g(1e-3) / g(1e-4)) / np.log(10); p2 = np.log(g(1e-4) / g(1e-5)) / np.log(10)
            log(f"C alpha={al} (Delta={D}) {th}: gates quad(48 vs 96 @1e-3) {q:.1e}, n_p drift {[f'{x:.1e}' for x in dr]} "
                f"[{'PASS' if q < 1e-3 and max(dr) < 0.02 else 'FAIL'}];  i_G = {g(1e-3):.4e}, {g(1e-4):.4e}, {g(1e-5):.4e}")
            log(f"    local exponent p(1e-3->1e-4) = {p1:.4f};  p(1e-4->1e-5) = {p2:.4f};  predicted 2(2D-1) = {p_pred:.4f}  "
                f"|p2 - pred| = {abs(p2 - p_pred):.4f} <= {tol}: [{'PASS' if abs(p2 - p_pred) <= tol else 'FAIL'}]")

if __name__ == "__main__":
    log("EXP-038 start"); partB(); partC()
