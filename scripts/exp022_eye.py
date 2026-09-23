"""EXP-022: tests of the LMW26b 'eye' inequalities (2609.04302) on this workspace's curves. Pre-registered in report.md.
F_n(u) = tan(theta/4) a_n(theta), u = tan^2(theta/4): positive, decreasing, convex for integer n >= 2 (theorem); n = 1 continuation.
Eq. (37) in corner language: a_1 <= -kappa_n/12 where a_n = kappa_n/theta + a0 + a_1 theta + ..., when Delta_irr > 3/2."""
import sys, json, io, contextlib, warnings, numpy as np
from math import pi, gamma
warnings.filterwarnings("ignore")
sys.path.insert(0, __file__.rsplit('/',1)[0])
with contextlib.redirect_stdout(io.StringIO()):
    from exp001_measure import aE_over_CT
    from exp001_ecg import aECG_over_CT
    from exp012_sign import boson, fermi, kap, ansatz22
D = __file__.rsplit('/',1)[0]
th_of_u = lambda u: 4*np.arctan(np.sqrt(u)); F_of = lambda th, a: np.tan(th/4)*a
kE = pi**2*gamma(0.75)**4/6

def dense_check(name, afun, tol=1e-7):
    us = np.concatenate([np.geomspace(2e-4, 0.02, 40), np.linspace(0.021, 0.995, 160)])
    F = np.array([F_of(th_of_u(u), afun(th_of_u(u))) for u in us])
    s = np.diff(F)/np.diff(us); d2 = 2*np.diff(s)/(us[2:]-us[:-2])
    scale = np.max(np.abs(d2)); worst = d2.min()
    ok = (F.min() > 0) and (s.max() < 0) and (worst >= -tol*scale)
    print(f"  {name:28s} F>0: {F.min()>0}  decreasing: {s.max()<0}  min F''/max|F''| = {worst/scale:+.2e}  ->  {'CONVEX' if ok else 'NOT CONVEX'}")
    return ok

def discrete_check(name, deg, a, eps):
    th = np.radians(deg); u = np.tan(th/4)**2; F = np.tan(th/4)*a
    order = np.argsort(u); u, F = u[order], F[order]
    s = np.diff(F)/np.diff(u); ds = np.diff(s)
    noise = eps*(np.abs(F[:-2])+2*np.abs(F[1:-1])+np.abs(F[2:]))*(1/np.diff(u)[:-1] + 1/np.diff(u)[1:])
    viol = [(i, ds[i], noise[i]) for i in range(len(ds)) if ds[i] < 0]
    signif = [v for v in viol if -v[1] > v[2]]
    print(f"  {name:28s} {len(u)} angles  F>0: {F.min()>0}  decreasing: {s.max()<0}  secant-slope decreases: {len(viol)} (beyond noise: {len(signif)})  ->  {'CONVEX within noise' if not signif and F.min()>0 and s.max()<0 else 'FAIL'}")
    for i, v, n in signif: print(f"      violation between {np.degrees(th_of_u(u[i])):.1f} and {np.degrees(th_of_u(u[i+2])):.1f} deg: {v:+.2e} vs noise {n:.1e}")
    return not signif

print("T-A  KNOWN ANSWERS (theorem at integer n >= 2)")
okA = []
for label, tab, key in (("boson", boson, "boson"), ("fermion", fermi, "fermi")):
    for n in (2, 3, 4):
        okA.append(dense_check(f"HHCWM16 {label} n={n} (eq 22)", lambda t, c=tab[n], k=kap[key][n]: ansatz22(t, c, k)))
r2 = json.load(open(f"{D}/exp004_renyi2_result_n24_24_p15.0_t1.json")); d2v = json.load(open(f"{D}/exp004_dirac2v_result_n24_24_p15.0_t1.json"))
for name, r in (("instrument scalar n=2", r2), ("instrument Dirac n=2", d2v)):
    deg = np.array(r['deg']); s = np.array(r['s']); m = deg >= 15
    okA.append(discrete_check(name, deg[m], s[m], 5e-5))

print("\nT-B  CONTINUATION TO n = 1 (not guaranteed)")
okB = []
okB.append(dense_check("Einstein (exact)", aE_over_CT))
for mu in (0.00312, 0.001, -0.001, -0.00322):
    okB.append(dense_check(f"ECG mu={mu:+.5f} (exact)", lambda t, mu=mu: aECG_over_CT(t, mu)))
for label, tab, key in (("boson", boson, "boson"), ("fermion", fermi, "fermi")):
    okB.append(dense_check(f"HHCWM16 {label} n=1 (eq 22)", lambda t, c=tab[1], k=kap[key][1]: ansatz22(t, c, k)))
dr = json.load(open(f"{D}/exp004_dirac_result_n24_24_p15.0_t14.json")); er = json.load(open(f"{D}/exp004_eehp_result_Mcut13.1.json"))
for name, r in (("instrument Dirac n=1", dr), ("instrument scalar n=1", er)):
    deg = np.array(r['deg']); s = np.array(r['s']); m = deg >= 20
    okB.append(discrete_check(name, deg[m], s[m], 5e-5))

print("\nEQ. (37): a_1 <= -kappa/12  (a_1 = theta^1 coefficient of a_n; applies when Delta_irr > 3/2)")
def a1_exact(afun, k):
    v = [(afun(t) - k/t)/t for t in (0.01, 0.005, 0.0025)]; return v
rows = [("Einstein n=1", aE_over_CT, kE)] + [(f"ECG mu={mu:+.5f} n=1", (lambda t, mu=mu: aECG_over_CT(t, mu)), kE*(1-123*mu/20)/(1-3*mu)) for mu in (0.00312, 0.001, -0.001, -0.00322)]
res37 = []
for name, f, k in rows:
    v = a1_exact(f, k); a1 = v[-1]
    print(f"  {name:22s} (a - kappa/theta)/theta at theta = 0.01, 0.005, 0.0025: {v[0]:+.5f} {v[1]:+.5f} {v[2]:+.5f}   bound -kappa/12 = {-k/12:+.5f}   ratio a_1/(-kappa/12) = {a1/(-k/12):.3f}  ->  {'PASS' if a1 < -k/12 else 'FAIL'}")
    res37.append((name, a1/(-k/12)))
def fit_a1(deg, s, k, lo, hi, a0zero=True):
    th = np.radians(deg); m = (deg >= lo) & (deg <= hi); x = th[m]; y = s[m] - k/x
    cols = [x, x**2, x**3] if a0zero else [np.ones_like(x), x, x**2, x**3]
    cf, *_ = np.linalg.lstsq(np.vstack(cols).T, y, rcond=None)
    return (cf[0], cf[1]) if a0zero else (cf[1], cf[2])
for name, r, k0, kerr in (("Dirac n=1", dr, 0.0722, 5e-5), ("Dirac n=2", d2v, 0.0472338, 1e-7)):
    deg = np.array(r['deg']); s = np.array(r['s']); out = []; c2 = []
    for k in (k0 - kerr, k0, k0 + kerr):
        for lo, hi in ((20, 50), (20, 60), (26, 60), (20, 70)):
            a1, a2 = fit_a1(deg, s, k, lo, hi); out.append(a1/(-k/12)); c2.append(a2)
    lo_, hi_ = min(out), max(out)
    print(f"  {name:22s} fits (a0 = 0; 4 windows x kappa +- its last digit): a_1/(-kappa/12) in [{lo_:.3f}, {hi_:.3f}]  ->  {'PASS' if lo_ > 1 else ('FAIL' if hi_ < 1 else 'INCONCLUSIVE')}")
    print(f"  {'':22s} T-C theta^2 coefficient of a_n across the same fits: [{min(c2):+.4f}, {max(c2):+.4f}] (prediction >= 0; inference, low weight)")
    res37.append((name, lo_))
print("\nSUMMARY: T-A all pass:", all(okA), "| T-B all pass:", all(okB))
