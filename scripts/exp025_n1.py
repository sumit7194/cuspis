"""EXP-025 (CF-9): controls K1-K4 and the H4 number, as pre-registered in report.md.

Frame: the NS "time" t is a spatial coordinate of the t_Minkowski = 0 plane; z = t + i y; slice Sigma_0 = {t = 0};
punctures at z = +-i.  u-flow: xi_u = (1 - u z^2)/2 (complex form of (P_0 - u K_0)/2), fixed points +-X, X = 1/sqrt(u).
Phi_s(z) = tanh(atanh(sqrt(u) z) + sqrt(u) s / 2) / sqrt(u).
u'-eye: the two circles through +-X' (X' = 1/sqrt(u')) and +-i; upper eyelid centre (0, c'), c' = (1 - X'^2)/2,
radius R' = (1 + X'^2)/2; the eye is the intersection of the two disks.  P = the part of the u'-eye boundary in t < 0.
"""
import sys, io, contextlib, warnings, numpy as np
from math import pi, gamma
warnings.filterwarnings("ignore")
sys.path.insert(0, __file__.rsplit('/', 1)[0])
with contextlib.redirect_stdout(io.StringIO()):
    from exp022_eye import dense_check
    from exp001_measure import aE_over_CT
    from exp012_sign import boson, fermi, kap, ansatz22

def eye(up):
    X = 1/np.sqrt(up); c = (1 - X**2)/2; R = (1 + X**2)/2
    return X, c, R

def in_eye(z, up, strict=1e-12):
    X, c, R = eye(up)
    return (abs(z - 1j*c) < R - strict) & (abs(z + 1j*c) < R - strict)

def P_arc(up, n=4000):
    """upper-left eyelid from +i (excluded) to -X' (excluded), with inward normals of the eye."""
    X, c, R = eye(up)
    a0 = np.pi/2; a1 = np.angle(-X - 1j*c)          # angle of -X' seen from the centre i c
    if a1 < a0: a1 += 2*np.pi
    ang = np.linspace(a0, a1, n + 2)[1:-1]
    q = 1j*c + R*np.exp(1j*ang); nin = (1j*c - q)/R
    return q, nin

xi = lambda z, u: (1 - u*z**2)/2
def Phi(z, u, s):
    r = np.sqrt(u); return np.tanh(np.arctanh(r*z) + r*s/2)/r

print("K1  GEOMETRY  (nesting of the flowed half-eyes; must hold on the whole grid)")
grid = [0.02, 0.05, 0.1, 0.1716, 0.3, 0.5, 0.7, 0.9, 1.0]
k1 = True; rows = []
for u in grid:
    for up in grid:
        if u == up: continue
        q, nin = P_arc(up); ximag = np.abs(xi(q, u))
        dot = np.real(xi(q, u)*np.conj(nin))/ximag            # cos(angle between xi_u and the inward normal)
        want = +1 if u < up else -1                             # interior nested if u < u', exterior if u > u'
        transverse = np.all(want*dot > 0)
        # containment: u'-eye inside u-lens (u < u') or u-lens inside u'-eye (u > u')
        Xu, cu, Ru = eye(u); Xp, cp, Rp = eye(up)
        if u < up: cont = np.all(in_eye(P_arc(up, 800)[0]*(1 - 1e-9), u, strict=-1e-12))
        else:      cont = np.all(in_eye(P_arc(u, 800)[0]*(1 - 1e-9), up, strict=-1e-12))
        # direct crossing count along flow lines from Sigma_0, flowed backward to s = -40/sqrt(u)
        ss = -np.linspace(0, 40/np.sqrt(u), 20001)[1:]
        y0s = np.concatenate([np.linspace(-0.98, 0.98, 25), np.linspace(1.05, 6, 12), -np.linspace(1.05, 6, 12)])
        bad = 0
        for y0 in y0s:
            path = Phi(np.full_like(ss, 1j*y0, dtype=complex), u, ss)
            ins = in_eye(path, up) & (path.real < 0)
            flips = np.count_nonzero(ins[1:] != ins[:-1])
            if u < up:   expect = 1 if abs(y0) < 1 else 0     # lens lines enter h' once; outside lines never meet h'
            else:        expect = 0 if abs(y0) < 1 else 1     # lens lines stay inside h'; exterior lines cross P once
            start_in = in_eye(np.array([1j*y0 - 1e-6]), up)[0]
            if flips != expect: bad += 1
        ok = transverse and cont and bad == 0
        k1 &= ok
        rows.append((u, up, dot.min() if want > 0 else (-dot).min(), cont, bad, ok))
for u, up, m, cont, bad, ok in rows:
    if not ok: print(f"   FAIL u={u} u'={up}: min transversality {m:+.3e} containment {cont} bad flow lines {bad}")
mins = [r[2] for r in rows]
print(f"   {len(rows)} ordered pairs (u != u') on grid {grid}")
print(f"   transversality margin (cos angle, sign-corrected) over all pairs: min {min(mins):+.3e}; containment all: {all(r[3] for r in rows)}; wrong crossing counts: {sum(r[4] for r in rows)}")
print(f"   K1 -> {'PASS' if k1 else 'FAIL'}")
# check that the check can fail: reverse the nesting requirement (interior family for u > u') must be flagged
q, nin = P_arc(0.3); dot = np.real(xi(q, 0.7)*np.conj(nin))
print(f"   control: interior-nesting test for u=0.7 > u'=0.3 (must be flagged): min cos = {dot.min()/1:+.3e} -> {'flagged' if not np.all(dot > 0) else 'NOT flagged (check is decoration)'}")

print("\nK2  FALSIFIERS: SSA-satisfying conformal models must obey CC at n = 1")
aEMI = lambda t: 1 + (pi - t)/np.tan(t)
k2 = [dense_check("EMI 1+(pi-t)cot t", aEMI),
      dense_check("Einstein (exact)", aE_over_CT),
      dense_check("scalar n=1 (HHCWM16 eq 22)", lambda t: ansatz22(t, boson[1], kap['boson'][1])),
      dense_check("Dirac n=1 (HHCWM16 eq 22)", lambda t: ansatz22(t, fermi[1], kap['fermi'][1]))]
# Why did a K2 line fire?  Locate the violation window of the eq-22 Dirac curve (EXP-022 documented an artifact at 3.4-4.1 deg).
us = np.concatenate([np.geomspace(2e-4, 0.02, 40), np.linspace(0.021, 0.995, 160)])
th_u = 4*np.arctan(np.sqrt(us)); Fd = np.tan(th_u/4)*np.array([ansatz22(t, fermi[1], kap['fermi'][1]) for t in th_u])
sl = np.diff(Fd)/np.diff(us); dd = 2*np.diff(sl)/(us[2:] - us[:-2]); badu = us[1:-1][dd < 0]
if len(badu):
    print(f"   eq-22 Dirac: F'' < 0 only for u in [{badu.min():.2e}, {badu.max():.2e}] = theta in [{np.degrees(4*np.arctan(np.sqrt(badu.min()))):.2f}, {np.degrees(4*np.arctan(np.sqrt(badu.max()))):.2f}] deg;"
          f" its small-angle constant a0 = lim (a - kappa/theta), linear extrapolation from 0.1 and 0.2 deg: {2*(ansatz22(np.radians(0.1), fermi[1], kap['fermi'][1]) - kap['fermi'][1]/np.radians(0.1)) - (ansatz22(np.radians(0.2), fermi[1], kap['fermi'][1]) - kap['fermi'][1]/np.radians(0.2)):+.6f}")
    print("   -> the EXP-022 artifact (eq. 22's constructed tail carries a0 > 0); the measured Dirac a0 is 0.00 +- 0.02 C_T (EXP-020).")
    print("   Measured n = 1 curves from this workspace's solver (as in EXP-022 T-B):")
import json
from exp022_eye import discrete_check
D = __file__.rsplit('/', 1)[0]
dr = json.load(open(f"{D}/exp004_dirac_result_n24_24_p15.0_t14.json")); er = json.load(open(f"{D}/exp004_eehp_result_Mcut13.1.json"))
k2m = []
for name, r in (("instrument Dirac n=1", dr), ("instrument scalar n=1", er)):
    deg = np.array(r['deg']); s = np.array(r['s']); m = deg >= 20
    k2m.append(discrete_check(name, deg[m], s[m], 5e-5))
print(f"   K2 as literally pre-registered (eq-22 Dirac included) -> {'PASS' if all(k2) else 'FIRED on eq-22 Dirac'};"
      f"  physical curves (EMI, Einstein, scalar, measured Dirac and scalar) -> {'PASS' if all(k2[:3]) and all(k2m) else 'FAIL'}")

print("\nK3  THE CC TEST MUST FIRE (sigma units)")
amin = lambda t: 8*np.log(1/np.sin(t/2))
aL = lambda t: pi**2*(t - pi)**2/(t*(2*pi - t)); lam = 0.5818
k3 = [not dense_check("a_min (must fail)", amin),
      not dense_check("witness a_lambda, lambda=.5818 (must fail)", lambda t: (1 - lam)*amin(t) + lam*aL(t)),
      dense_check("convex control F=(1-u)^2 (must pass)", lambda t: (1 - np.tan(t/4)**2)**2/np.tan(t/4))]
print(f"   K3 -> {'PASS' if all(k3) else 'FAIL'}")

print("\nK4  RECTANGLE SATURATOR S* (kappa = 2a, a = 1): concave, symmetric, not CM")
a = 1.0; S1 = 0.0
S = lambda y: np.where(y >= 1, S1 - 2*a*(y - 1), S1 - 4*a*np.log(y) - 2*a*(1/y - 1))
ys = np.geomspace(0.05, 20, 4001); Sv = S(ys)
d2 = np.diff(Sv, 2)
sym = np.max(np.abs(S(ys) - (S(1/ys) - 4*a*np.log(ys))))
slope_inf = (S(np.array([1e4]))[0] - S(np.array([1e4 - 1]))[0])
g = lambda y: 2*a*(1/y - 1)**2                              # g = S' + kappa on y < 1 (analytic)
yy = np.linspace(0.55, 0.95, 5); hank = 8*a**2*(1/yy - 1)**2*(1 - 2*yy)/yy**4
print(f"   concave (max 2nd difference {d2.max():+.2e} <= 0): {d2.max() <= 1e-12};  symmetry defect {sym:.1e};  slope at infinity {slope_inf:+.6f} = -kappa")
print(f"   log-convexity of g = S'+kappa (needed by complete monotonicity): g g'' - g'^2 on y in (1/2,1): {np.array2string(hank, precision=3)}  -> violated: {np.all(hank < 0)}")
print(f"   and g == 0 on y >= 1 while g > 0 on y < 1: not real-analytic, so not CM.  K4 -> {'PASS' if d2.max() <= 1e-12 and sym < 1e-12 and np.all(hank < 0) else 'FAIL'}")

print("\nH4  CHORD BOUND a(theta) <= (kappa/2) cot(theta/2) from CC, and the kappa bound with a >= a_min")
xs = np.linspace(1e-4, pi/2 - 1e-4, 2_000_001); gx = np.tan(xs)*np.log(1/np.sin(xs)); i = gx.argmax()
from scipy.optimize import brentq
xstar = brentq(lambda x: -np.log(np.sin(x)) - np.cos(x)**2, 0.3, 0.7)
gstar = np.tan(xstar)*np.log(1/np.sin(xstar))
print(f"   max_x tan x log(1/sin x) = {gstar:.10f} at x* = {xstar:.10f} (theta* = {np.degrees(2*xstar):.4f} deg); grid max {gx[i]:.10f}")
print(f"   kappa/C_T >= (2 pi^2/3) * {gstar:.6f} = {2*pi**2/3*gstar:.6f}    [pi/2 route: 2 pi^2 ln2/6 = {pi**2*np.log(2)/3:.6f}; S4 conditional: (2pi/3)(pi^2 ln2/6) = {2*pi/3*pi**2*np.log(2)/6:.6f}]")
kE = pi**2*gamma(0.75)**4/6
ths = np.linspace(0.02, pi - 0.02, 400)
for name, f, k in (("Einstein", aE_over_CT, kE), ("scalar n=1 eq22", lambda t: ansatz22(t, boson[1], kap['boson'][1]), kap['boson'][1]),
                   ("Dirac n=1 eq22", lambda t: ansatz22(t, fermi[1], kap['fermi'][1]), kap['fermi'][1]), ("EMI", aEMI, pi)):
    r = np.array([f(t) for t in ths])/(k/2/np.tan(ths/2))
    print(f"   {name:18s} max a/((kappa/2)cot(theta/2)) = {r.max():.4f} (must be <= 1)")
