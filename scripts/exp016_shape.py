"""EXP-016: shape residual — (1) ECG a0 (out-of-sample test of EXP-015); (2) does imposing a0 = 0 on the
(sigma, kappa) trial function reduce its error for theories without a dimension-1 fusion operator, and not for the
free scalar?  Everything is closed forms or published tables; runtime seconds.
Basis: aL = (th-pi)^2/(th(2pi-th))  [sigma 1/pi^2, kappa pi/2, theta^0 -3/4]
       aE = 1 + (pi-th) cot th      [sigma 1/3,   kappa pi,   theta^0 0]
       f3 (kappa 0) : two choices, cos^2(th/2) [sigma 1/4, theta^0 1] and ((pi-th)/pi)^2 [sigma 1/pi^2, theta^0 1]."""
import sys, numpy as np
from math import pi, gamma
sys.path.insert(0, __file__.rsplit('/',1)[0])
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    from exp001_measure import aE_over_CT
    from exp001_ecg import aECG_over_CT
    from exp012_sign import boson, fermi, kap, series, ansatz22
aL = lambda t: (t-pi)**2/(t*(2*pi-t))
aM = lambda t: 1 + (pi-t)/np.tan(t)
F3 = {"cos^2(th/2)": (lambda t: np.cos(t/2)**2, 0.25), "((pi-th)/pi)^2": (lambda t: ((pi-t)/pi)**2, 1/pi**2)}
def trial2(t, k, s):
    l1 = 2*pi*(k-3*pi*s)/(pi**2-6); l2 = -3*(2*k-pi**3*s)/(pi*(pi**2-6)); return l1*aL(t)+l2*aM(t)
def trial3(t, k, s, f3name, a0=0.0):
    f, s3 = F3[f3name]
    A = np.array([[1/pi**2, 1/3, s3], [pi/2, pi, 0.0], [-0.75, 0.0, 1.0]])   # rows: sigma, kappa, theta^0
    l = np.linalg.solve(A, [s, k, a0]); return l[0]*aL(t)+l[1]*aM(t)+l[2]*f(t)
# sanity: trial3 with a0 = a0~ must equal trial2
kE = pi**2*gamma(0.75)**4/6; sE = pi**2/24
a0t = -0.75*2*pi*(kE-3*pi*sE)/(pi**2-6)
print(f"control: trial3(a0=a0~) - trial2 at 0.7 rad = {trial3(0.7,kE,sE,'cos^2(th/2)',a0t)-trial2(0.7,kE,sE):+.2e} (must be 0)")

print("\n(1) ECG a0 from the exact first-order curve [BCV21 eq 293], kappa_ECG = (1-123mu/20) kappa_E, units C_T")
for mu in (0.00312, 0.001, -0.001, -0.00322):
    k = kE*(1-123*mu/20)/(1-3*mu)
    row = [(aECG_over_CT(t, mu) - k/t) for t in (0.02, 0.01, 0.005)]
    print(f"   mu={mu:+.5f}: a - kappa/theta = {row[0]:+.5f}, {row[1]:+.5f}, {row[2]:+.5f} at theta = 0.02, 0.01, 0.005  -> intercept {2*row[2]-row[1]:+.5f}")
print("   Einstein:", " ".join(f"{aE_over_CT(t)-kE/t:+.5f}" for t in (0.02,0.01,0.005)))

print("\n(2) |residual| in % of the exact value: two-shape trial  vs  a0 = 0 imposed (two choices of third shape)")
ang = [("26.6", np.arctan(0.5)), ("45", pi/4), ("63.4", np.arctan(2.0)), ("90", pi/2), ("135", 3*pi/4)]
def row(name, exact, k, s):
    out = []
    for lab, t in ang:
        e = exact(t); r2 = (trial2(t,k,s)/e-1)*100
        r3 = [(trial3(t,k,s,f)/e-1)*100 for f in F3]
        out.append(f"{lab}:{r2:+.2f}/{r3[0]:+.2f}/{r3[1]:+.2f}")
    print(f"   {name:18s} " + "  ".join(out))
CTc = 3/(16*pi**2)
theories = [("Einstein", aE_over_CT, kE, sE)]
for mu in (0.00312, -0.00322):
    theories.append((f"ECG mu={mu:+.5f}", (lambda t, mu=mu: aECG_over_CT(t, mu)), kE*(1-123*mu/20)/(1-3*mu), sE*1.0))
for n in (1,2,3,4):
    c = fermi[n]; k = kap['fermi'][n]
    theories.append((f"Dirac n={n}", (lambda t, c=c, k=k: (series(t,c) if t>=pi/2-1e-9 else ansatz22(t,c,k))/CTc), k/CTc, c[0]/CTc))
for n in (1,2):
    c = boson[n]; k = kap['boson'][n]
    theories.append((f"scalar n={n}", (lambda t, c=c, k=k: (series(t,c) if t>=pi/2-1e-9 else ansatz22(t,c,k))/CTc), k/CTc, c[0]/CTc))
print("   format  angle: two-shape / a0=0 with cos^2 / a0=0 with ((pi-th)/pi)^2")
for th_ in theories: row(*th_)

print("\n(3) the two numbers per theory: x = kappa/sigma (3pi = 9.4248) and the smooth-end residual (sigma'~ - sigma')/sigma'")
def smooth(k, s, sp):
    l1 = 2*pi*(k-3*pi*s)/(pi**2-6); l2 = -3*(2*k-pi**3*s)/(pi*(pi**2-6)); return (l1/pi**4 + l2/45)/sp - 1
spE = 5/192
for mu in (0.00312, 0.001, 0.0, -0.001, -0.00322):
    s = sE*(1-3*mu)/(1-3*mu); k = kE*(1-123*mu/20)/(1-3*mu); sp = spE*(1-33*mu/4)/(1-3*mu)
    print(f"   ECG mu={mu:+.5f}: x = {k/s:.4f}  smooth-end {smooth(k,s,sp)*100:+.2f}%   sharp-end sign(3pi - x) = {'+' if k/s<3*pi else '-'}")
for name, tab in (("Dirac", fermi), ("scalar", boson)):
    for n in (1,2,3,4):
        c = tab[n]; k = kap['fermi' if name=='Dirac' else 'boson'][n]
        print(f"   {name} n={n}: x = {k/c[0]:.4f}  smooth-end {smooth(k,c[0],c[1])*100:+.2f}%   sharp-end sign(3pi - x) = {'+' if k/c[0]<3*pi else '-'}{'  (has a dimension-1 fusion operator: rule not applicable)' if name=='scalar' else ''}")

print("\n(4) which imposed a0 fits best?  Scan a0 (units C_T), minimise rms residual over the five angles.")
print("    Einstein and ECG have a0 = 0 exactly (known-answer controls); the free scalar's is about -0.3 (second control);")
print("    Dirac is the unknown, predicted 0 by EXP-015.  This is inference from a fit, labelled as such.")
grid = np.linspace(-0.6, 0.4, 2001)
for name, exact, k, s_ in theories:
    best = []
    for f in F3:
        rms = [np.sqrt(np.mean([(trial3(t,k,s_,f,a0)/exact(t)-1)**2 for _,t in ang])) for a0 in grid]
        i = int(np.argmin(rms)); best.append((grid[i], rms[i]*100))
    a0t = -0.75*2*pi*(k-3*pi*s_)/(pi**2-6)
    print(f"   {name:18s} best a0 = {best[0][0]:+.3f} (rms {best[0][1]:.3f}%) / {best[1][0]:+.3f} (rms {best[1][1]:.3f}%)   two-shape a0~ = {a0t:+.3f}")

print("\n(5) do (sigma, kappa) leave 'little freedom'?  An admissible function with Einstein's exact sigma and kappa:")
print("    a_lam = (1-lam) a_min + lam aL_hat, proven in C1-C6 (RESULT.md Theorem (a)), lam = kappa_E/(pi^5/48)")
amin = lambda t: (pi**2/3)*np.log(1/np.sin(t/2))
aLh  = lambda t: (pi**4/24)*(pi-t)**2/(pi**2-(pi-t)**2)
lam = kE/(pi**5/48)
alam = lambda t: (1-lam)*amin(t) + lam*aLh(t)
print(f"    lam = {lam:.4f};  sigma check: {(alam(pi-1e-4))/1e-8:.6f} vs pi^2/24 = {pi**2/24:.6f};  kappa check: {alam(1e-5)*1e-5:.4f} vs {kE:.4f}")
for lab, t in ang:
    e = aE_over_CT(t); print(f"    {lab:>5} deg: Einstein {e:.4f}   two-shape trial {trial2(t,kE,sE):.4f} ({(trial2(t,kE,sE)/e-1)*100:+.2f}%)   admissible a_lam {alam(t):.4f} ({(alam(t)/e-1)*100:+.2f}%)")
