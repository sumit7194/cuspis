"""EXP-043 addendum A (registration in report.md): A2 sign counts with zero threshold and end signs; K for the scalar-law
Dirac/EMI pair; A3 contour test of the Einstein compact support. Einstein and EMI profiles are inverted directly in each
law (no spline derivative); t < 0.05 uses the contour Re D = 1.5, left of the pinning pole, plus the residue 1/3."""
import io, contextlib, json, math, sys
import numpy as np
from scipy.special import k1, k0
from scipy.interpolate import CubicSpline
from scipy.integrate import quad
sys.path.insert(0, "scripts")
with contextlib.redirect_stdout(io.StringIO()):
    import exp043_profiles as P
TMAX = P.TMAX
def inv(M, t, decay=False):
    if t < 0.05: return 1/3 + P.inv_mellin(M, t, -0.5, P.SEG_E if not decay else [(0, 200, 0.005)])
    if decay: return P.prof_decay(M, t)
    return P.inv_mellin(M, t, 0.5, P.SEG_E)

# free-field profiles (Impl-2 table for t <= 6, source forms outside)
J = json.load(open("scripts/exp040_impl2.json"))
U = np.array(J["U"]); cS = np.array(J["tab"]["S"]["cinf"]); cD = np.array(J["tab"]["D"]["cinf"])
m = np.exp(U) <= 6.0; spS = CubicSpline(U[m], cS[m]); spD = CubicSpline(U[m], cD[m]); u_lo, u_hi = U[0], U[m][-1]
def c_D(t):
    if t < 1e-5: return 1/3 - t*t*math.log(t)**2/3
    if math.log(t) > u_hi: return t/2*k1(2*t)
    return float(spD(math.log(t)))
def c_S(t):
    if t < 1e-5: return 1/3 + 1/(2*math.log(t))
    if math.log(t) > u_hi: return t/4*k1(2*t)
    return float(spS(math.log(t)))
def e_S(t):
    if t < 1e-5: L = math.log(t); return 1/3 + 1/(2*L) + 1/(2*L*L)
    if math.log(t) > u_hi: return t/4*k1(2*t) + t*t/2*k0(2*t)
    u = math.log(t); return float(spS(u) - spS(u, 1))
qD = lambda a, b: quad(lambda x: (1/3 - c_D(x))/x**2, a, b, limit=500)[0]
K = qD(0, 1e-5) + qD(1e-5, 1e-2) + qD(1e-2, 1) + qD(1, 6) + quad(lambda x: (1/3 - c_D(x))/x**2, 6, np.inf, limit=200)[0]
def et_D(t):                       # t int_t^inf c_D/u^2 du = 1/3 - t int_t^inf (1/3 - c_D)/u^2 du
    if t < 1e-5: return 1/3 - K*t + t*(qD(0, t))
    return 1/3 - t*(qD(t, 6) + quad(lambda x: (1/3 - c_D(x))/x**2, 6, np.inf, limit=200)[0]) if t < 6 else t*quad(lambda x: c_D(x)/x**2, t, np.inf, limit=200)[0]

if __name__ == "__main__":
    print(f"=== A2: K = int_0^inf (1/3 - c_D)/u^2 du = {K:.5f}   (one sign change for scalar-law Dirac/EMI predicted to need K > 1.233: "
          f"{'PASS' if K > 1.233 else 'FAIL'})")
    nodes = np.unique(np.concatenate([np.exp(np.linspace(math.log(1e-4), math.log(0.5), 220)), np.linspace(0.5, TMAX - 1e-3, 60),
                                      np.exp(np.linspace(math.log(TMAX + 1e-3), math.log(20.0), 120))]))
    prof = {"D-law": {}, "S-law": {}}
    prof["D-law"]["scalar"] = np.array([e_S(t) for t in nodes]); prof["S-law"]["scalar"] = np.array([c_S(t) for t in nodes])
    prof["D-law"]["Dirac"] = np.array([c_D(t) for t in nodes]); prof["S-law"]["Dirac"] = np.array([et_D(t) for t in nodes])
    for law, ME, MM in (("D-law", P.M_E_D, P.M_EMI_D), ("S-law", P.M_E_S, P.M_EMI_S)):
        prof[law]["Einstein"] = np.array([inv(ME, t) if t < TMAX else 0.0 for t in nodes])
        prof[law]["EMI"] = np.array([inv(MM, t, decay=True) for t in nodes])
        print(f"[{law} Einstein/EMI inverted on {len(nodes)} nodes]", flush=True)
    print("=== A2: zero-threshold sign changes on the nodes in [1e-4, 20] (Einstein set to 0 beyond t_max) ===")
    names = ["scalar", "Dirac", "Einstein", "EMI"]; ok = True; out = {}
    for i in range(4):
        for j in range(i + 1, 4):
            a, b = names[i], names[j]; r = {}
            for law in ("D-law", "S-law"):
                d = prof[law][a] - prof[law][b]; s = np.sign(d); s = s[s != 0]
                r[law] = int(np.sum(s[:-1]*s[1:] < 0))
            ok &= r["D-law"] == 1 and r["S-law"] == 1; out[f"{a}-{b}"] = r
            print(f"  {a:8s} vs {b:8s}: D-law {r['D-law']}, S-law {r['S-law']}")
    print("  A2 count", "PASS" if ok else "FAIL")
    print("=== A2: end signs (small t from source forms / shifted contour; large t from asymptotic forms / saddle contour) ===")
    small = (1e-6, 1e-5, 1e-4); large = (20.0, 40.0, 60.0)
    def val(law, k, t):
        if k == "scalar": return e_S(t) if law == "D-law" else c_S(t)
        if k == "Dirac": return c_D(t) if law == "D-law" else et_D(t)
        if k == "Einstein": return (inv(P.M_E_D if law == "D-law" else P.M_E_S, t) if t < TMAX else 0.0)
        return inv(P.M_EMI_D if law == "D-law" else P.M_EMI_S, t, decay=True)
    ends_ok = True
    for i in range(4):
        for j in range(i + 1, 4):
            a, b = names[i], names[j]
            for law in ("D-law", "S-law"):
                ss = [np.sign(val(law, a, t) - val(law, b, t)) for t in small]
                sl = [np.sign(val(law, a, t) - val(law, b, t)) for t in large]
                good = len(set(ss)) == 1 and len(set(sl)) == 1 and ss[0] == -sl[0] and ss[0] != 0
                ends_ok &= good
                print(f"  {a:8s} vs {b:8s} {law}: small-t signs {[int(x) for x in ss]}, large-t signs {[int(x) for x in sl]}  {'opposite' if good else 'NOT opposite/consistent'}")
    print("  A2 ends", "PASS" if ends_ok else "FAIL")

    print("=== A3: Einstein (S-law) on four contours ===")
    for t in (0.62, 0.8):
        v = [P.inv_mellin(P.M_E_S, t, s, P.SEG_E) for s in (0.5, 5, 20, 80)]
        print(f"  outside, t={t}: " + "  ".join(f"sigma={s}: {x:+.2e}" for s, x in zip((0.5, 5, 20, 80), v)) +
              f"   {'PASS' if all(abs(x) < 1e-8 for x in v) else 'FAIL'}")
    for t, sig in ((0.5, (0.5, 5, 20, 80)), (0.3, (0.5, 5, 20))):
        v = [P.inv_mellin(P.M_E_S, t, s, P.SEG_E) for s in sig]
        print(f"  inside, t={t}: " + "  ".join(f"sigma={s}: {x:.10f}" for s, x in zip(sig, v)) +
              f"   spread {max(v)-min(v):.1e}  {'PASS' if max(v)-min(v) < 1e-7 else 'FAIL'}")
    yy = np.concatenate([np.linspace(0, 400, 40001), np.linspace(400, 30000, 59201)])
    for s in (0.5, 5, 20, 80):
        b = np.abs(P.M_E_S(2 + s + 1j*yy)) * TMAX**(-s) * (1 + yy)**2.5
        print(f"  sup_y |M(2+sigma+iy)| t_max^-sigma (1+|y|)^(5/2), sigma={s}: {b.max():.3e}")
    json.dump(dict(K=K, nodes=nodes.tolist(), counts=out), open("scripts/exp043_addA.json", "w"))
