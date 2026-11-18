"""EXP-043 (registration in report.md): mass profiles e_X(t), the Mellin dual in dimension D of kappa_D/C_T.
M_X(D) = (kappa_D/C_T)_X * C_ref(D)/P(D) = int_0^inf t^(D-3) e_X(t) dt, C_ref = Dirac law D/Omega^2.
'D-law' profile e_X; 'S-law' profile et_X (M divided by D-1), with e = et - t et'.
Free fields from the EXP-040 Impl-2 table (t <= 6) and the one-particle form beyond; Einstein and EMI by inverse Mellin."""
import io, contextlib, json, math, sys
import numpy as np
from scipy.special import loggamma, k1, k0
from scipy.interpolate import CubicSpline
from scipy.integrate import quad
sys.path.insert(0, "scripts")
with contextlib.redirect_stdout(io.StringIO()):
    import exp041_emi as E41
X, I2 = E41.X, E41.I2
TMAX = math.pi / (2 * math.e)

# ---------- closed forms, complex D ----------
def lnM_E_S(D):       # Einstein, scalar law
    return ((2*D - 5)*math.log(2) + (D - 1)/2*math.log(math.pi) + (D - 1)*(loggamma(D/(2*D - 2)) - loggamma(1/(2*D - 2)))
            + np.log(D) + 3*loggamma(D/2) + loggamma(D/2 - 1) - loggamma(D + 2))
M_E_S = lambda D: np.exp(lnM_E_S(D))
M_E_D = lambda D: (D - 1) * M_E_S(D)
M_EMI_D = lambda D: np.exp(math.log(math.sqrt(math.pi)/4) + np.log(D) + loggamma(D/2 - 1) + 2*loggamma(D/2) - np.log(D*D - 1) - loggamma((D - 1)/2))
M_EMI_S = lambda D: M_EMI_D(D) / (D - 1)
M_1p = lambda D: np.exp(loggamma(D/2 - 1) + loggamma(D/2)) / 8
C_ref = lambda D: D / I2.Om(D) ** 2

def simpson(f, h):
    n = len(f) - 1
    if n % 2: f = f[:-1]; n -= 1
    return h/3 * (f[0] + f[-1] + 4*np.sum(f[1:-1:2]) + 2*np.sum(f[2:-1:2]))

def inv_mellin(Mfun, t, sigma, segs):
    """e(t) = (1/pi) Re int_0^inf M(2+sigma+iy) t^(-sigma-iy) dy on piecewise-uniform segments [(y0, y1, dy), ...]."""
    tot = 0.0
    for y0, y1, dy in segs:
        n = int(round((y1 - y0)/dy)); n += n % 2
        y = y0 + (y1 - y0)*np.arange(n + 1)/n
        f = (Mfun(2 + sigma + 1j*y) * np.exp(-(sigma + 1j*y)*math.log(t))).real
        tot += simpson(f, (y1 - y0)/n)
    return tot / math.pi

SEG_E = [(0, 400, 0.01), (400, 30000, 0.05)]
def prof_decay(Mfun, t):                      # exponentially decaying transforms: saddle contour
    s = max(0.5, 2*t); Y = 80 + 30*math.sqrt(s)
    return inv_mellin(Mfun, t, s, [(0, Y, 0.01)])

if __name__ == "__main__":
    print("=== K1: known inverse, M_1p -> (t/2) K1(2t) ===")
    ok = True
    for t in (0.05, 0.3, 1.0, 3.0):
        v = prof_decay(M_1p, t); ref = t/2*k1(2*t); ok &= abs(v - ref) < 1e-6
        print(f"  t={t}: {v:.10f} vs {ref:.10f}  diff {v-ref:+.1e}")
    print("  K1", "PASS" if ok else "FAIL")
    print("=== K2: closed forms against EXP-040/041 at real D ===")
    ok = True
    for D in (2.5, 3.0, 4.0, 6.0):
        a = float(M_E_D(D).real) * I2.P_D(D) / C_ref(D) / I2.rE(D) - 1
        b = float(M_EMI_D(D).real) * I2.P_D(D) / C_ref(D) / E41.rEMI(D) - 1
        ok &= abs(a) < 1e-10 and abs(b) < 1e-10
        print(f"  D={D}: Einstein rel {a:+.1e}   EMI rel {b:+.1e}")
    print("  K2", "PASS" if ok else "FAIL")

    # ---------- free-field profiles ----------
    J = json.load(open("scripts/exp040_impl2.json"))
    U = np.array(J["U"]); cS = np.array(J["tab"]["S"]["cinf"]); cD = np.array(J["tab"]["D"]["cinf"])
    m = np.exp(U) <= 6.0
    spS = CubicSpline(U[m], cS[m]); spD = CubicSpline(U[m], cD[m]); u_hi = U[m][-1]; u_lo = U[0]
    def c_S(t):
        u = math.log(t)
        if u > u_hi: return t/4*k1(2*t)
        if u < u_lo: return float(spS(u_lo))
        return float(spS(u))
    def c_D(t):
        u = math.log(t)
        if u > u_hi: return t/2*k1(2*t)
        if u < u_lo: return 1/3 - t*t*math.log(t)**2/3
        return float(spD(u))
    def e_S(t):                               # D-law scalar profile c - t c'
        u = math.log(t)
        if u > u_hi: return t/4*k1(2*t) + t*t/2*k0(2*t)
        if u < u_lo: return float(spS(u_lo))
        return float(spS(u) - spS(u, 1))
    def et_D(t):                              # S-law Dirac profile: t int_t^inf c_D(u)/u^2 du
        return t * (quad(lambda x: c_D(x)/x**2, t, max(t, 6.0), limit=400)[0] + quad(lambda x: c_D(x)/x**2, max(t, 6.0), 60, limit=200)[0])
    print("=== K5: free-field profiles return EXP-040's kappa/C_T ===")
    ok = True
    def mell(f, D, lo=1e-5, hi=40.0):
        body = quad(lambda u: math.exp((D - 2)*u)*f(math.exp(u)), math.log(lo), math.log(hi), limit=800)[0]
        return body + f(lo)*lo**(D - 2)/(D - 2)
    for D in (3.0, 4.0):
        s, d = X.r2(D)
        a = mell(e_S, D)*I2.P_D(D)/C_ref(D)/s - 1; b = mell(c_D, D)*I2.P_D(D)/C_ref(D)/d - 1
        ok &= abs(a) < 5e-4 and abs(b) < 5e-4
        print(f"  D={D}: scalar rel {a:+.1e}   Dirac rel {b:+.1e}")
    print("  K5", "PASS" if ok else "FAIL")

    # ---------- Einstein and EMI profiles ----------
    tg = np.unique(np.concatenate([np.exp(np.linspace(math.log(1e-4), math.log(0.3), 70)), np.linspace(0.3, TMAX - 0.03, 60),
                                   np.linspace(TMAX - 0.03, TMAX - 0.001, 59), [TMAX - 0.02, TMAX - 0.005, 0.5],
                                   [0.58, 0.6, 0.62, 0.7, 0.8, 1.0, 1.5, 2.0]]))
    etE = np.array([inv_mellin(M_E_S, t, 0.5, SEG_E) for t in tg])
    print("=== P1: compact support of the Einstein profile (S-law), t_max = %.5f ===" % TMAX)
    get = lambda t: float(etE[np.argmin(abs(tg - t))])
    p1 = all(abs(get(t)) < 1e-4 for t in (0.62, 0.8, 1.5)) and get(0.5) > 1e-2
    for t in (0.5, TMAX - 0.02, TMAX - 0.005, 0.58, 0.6, 0.62, 0.8, 1.5):
        print(f"  et_E({t:.5f}) = {get(t):+.3e}")
    print("  P1", "PASS" if p1 else "FAIL")
    sl = math.log(get(TMAX - 0.02)/get(TMAX - 0.005)) / math.log(0.02/0.005)
    print(f"=== P2: edge exponent (S-law), log-slope between t_max-0.02 and t_max-0.005: {sl:.3f}  {'PASS' if 1.3 <= sl <= 1.7 else 'FAIL'}")
    ins = tg < TMAX - 0.0005
    spE = CubicSpline(np.log(tg[ins]), etE[ins])
    et_E = lambda t: float(spE(math.log(t))) if t < tg[ins][-1] else 0.0
    e_E = lambda t: float(spE(math.log(t)) - spE(math.log(t), 1)) if t < tg[ins][-1] else 0.0
    fine = np.exp(np.linspace(math.log(1e-4), math.log(tg[ins][-1]), 4000))
    eEv = np.array([e_E(t) for t in fine]); etEv = np.array([et_E(t) for t in fine])
    print(f"=== P3: max of the D-law Einstein profile = {eEv.max():.4f} at t = {fine[eEv.argmax()]:.4f}  {'PASS' if eEv.max() > 0.34 else 'FAIL'}")
    print(f"  open question: S-law Einstein profile: min {etEv.min():+.2e}; max {etEv.max():.5f} at t = {fine[etEv.argmax()]:.2e}; "
          f"decreasing on the grid: {'YES' if np.all(np.diff(etEv) <= 1e-7) else 'NO'}")
    print(f"                 D-law Einstein profile: min {eEv.min():+.2e}; decreasing: {'YES' if np.all(np.diff(eEv) <= 1e-7) else 'NO'}")
    tl = np.exp(np.linspace(math.log(1e-4), math.log(25.0), 1500))
    eMv = np.array([prof_decay(M_EMI_D, t) for t in tl]); etMv = np.array([prof_decay(M_EMI_S, t) for t in tl])
    print(f"  open question: EMI D-law: min {eMv.min():+.2e}, max {eMv.max():.5f}, decreasing: {'YES' if np.all(np.diff(eMv) <= 1e-9) else 'NO'};"
          f"  S-law: min {etMv.min():+.2e}, max {etMv.max():.5f}, decreasing: {'YES' if np.all(np.diff(etMv) <= 1e-9) else 'NO'}")
    lsM = CubicSpline(np.log(tl), np.log(np.clip(eMv, 1e-300, None))); lsMt = CubicSpline(np.log(tl), np.log(np.clip(etMv, 1e-300, None)))
    e_M = lambda t: math.exp(float(lsM(math.log(t)))); et_M = lambda t: math.exp(float(lsMt(math.log(t))))

    print("=== K3: round trip, Mellin of the computed profiles ===")
    ok = True
    for D in (2.5, 3.0, 4.0, 6.0):
        r = [mell(et_E, D, 1e-4, tg[ins][-1]) / float(M_E_S(D).real) - 1, mell(e_E, D, 1e-4, tg[ins][-1]) / float(M_E_D(D).real) - 1,
             mell(e_M, D, 1e-4, 25.0) / float(M_EMI_D(D).real) - 1, mell(et_M, D, 1e-4, 25.0) / float(M_EMI_S(D).real) - 1]
        ok &= all(abs(x) < 1e-3 for x in r)
        print(f"  D={D}: Einstein S-law {r[0]:+.1e}, D-law {r[1]:+.1e};  EMI D-law {r[2]:+.1e}, S-law {r[3]:+.1e}")
    print("  K3", "PASS" if ok else "FAIL")
    k4 = [e_E(1e-3), e_M(1e-3), et_E(1e-3), et_M(1e-3)]
    print(f"=== K4: pinning at t = 1e-3: Einstein {k4[0]:.5f}, EMI {k4[1]:.5f} (D-law); {k4[2]:.5f}, {k4[3]:.5f} (S-law); 1/3 = 0.33333  "
          f"{'PASS' if all(abs(v - 1/3) < 5e-3 for v in k4) else 'FAIL'}")

    # ---------- areas and sign changes ----------
    prof = {"D-law": {"scalar": e_S, "Dirac": c_D, "Einstein": e_E, "EMI": e_M},
            "S-law": {"scalar": c_S, "Dirac": et_D, "Einstein": et_E, "EMI": et_M}}
    print("=== areas under the D-law profiles (kappa/C_T at D = 3 is area * 16 pi/3) ===")
    for k, f in prof["D-law"].items():
        a = mell(f, 3.0, 1e-5 if k in ("scalar", "Dirac") else 1e-4, 40.0 if k != "Einstein" else tg[ins][-1])
        print(f"  {k:9s} area {a:.5f}  -> kappa/C_T = {a*16*math.pi/3:.4f};  width = area/(1/3) = {3*a:.4f}")
    G = np.exp(np.linspace(math.log(1e-4), math.log(20.0), 3000))
    vals = {law: {k: np.array([f(t) for t in G]) for k, f in d.items()} for law, d in prof.items()}
    print("=== P4: sign changes of e_X - e_Y on [1e-4, 20] (relative threshold 1e-4 of the larger profile; Einstein = 0 beyond t_max) ===")
    names = ["scalar", "Dirac", "Einstein", "EMI"]; out = {}; p4 = True
    for i in range(4):
        for j in range(i + 1, 4):
            a, b = names[i], names[j]; res = {}
            for law in ("D-law", "S-law"):
                d = vals[law][a] - vals[law][b]; sc = np.maximum(abs(vals[law][a]), abs(vals[law][b]))
                keep = abs(d) > 1e-4 * sc
                s = np.sign(d[keep]); tt = G[keep]; idx = np.where(s[:-1] * s[1:] < 0)[0]
                res[law] = [float(math.sqrt(tt[k]*tt[k+1])) for k in idx]
            one = any(len(v) == 1 for v in res.values()); p4 &= one; out[f"{a}-{b}"] = res
            print(f"  {a:8s} vs {b:8s}: D-law {len(res['D-law'])} at t = {[round(x,4) for x in res['D-law']]};  S-law {len(res['S-law'])} at t = {[round(x,4) for x in res['S-law']]}  "
                  f"{'one sign change in at least one law' if one else 'NOT one'}")
    print("  P4", "PASS" if p4 else "FAIL")
    json.dump(dict(t=G.tolist(), profiles={law: {k: v.tolist() for k, v in d.items()} for law, d in vals.items()}, sign_changes=out,
                   tg=tg.tolist(), etE=etE.tolist()), open("scripts/exp043_profiles.json", "w"))
