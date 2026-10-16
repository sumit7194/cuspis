"""EXP-031: the QNEC corner inequality Q[a] = a'' + (1/2) tan(theta/2) a' >= 0 and the pure tail a_w.
Pre-registered in report.md (EXP-031). (m1) sympy Hessian, (m2) independent numpy/mpmath finite-difference Hessian,
(m3) spectral kernel K_Q on a grid, (m4) Q on the pre-registered functions and controls.
Signature (-,+,+). Edges e1=(0,1,0), e2=(0,cos t,sin t); future-outward null normals k1=(1,0,-1), k2=(1,-sin t,cos t).
Deformation: edge i -> e_i + c_i k_i (tip fixed). x = cos(theta_eff) = (e1+c1 k1).(e2+c2 k2)."""
import numpy as np, sympy as sp, mpmath as mp

def mink(u, v):
    return -u[0]*v[0] + u[1]*v[1] + u[2]*v[2]

# ---------------- (m1) sympy ----------------
t, c1, c2, s = sp.symbols('theta c1 c2 s', positive=True)
d1, d2 = sp.symbols('d1 d2', nonnegative=True)
e1, e2 = (0, 1, 0), (0, sp.cos(t), sp.sin(t))
k1, k2 = (1, 0, -1), (1, -sp.sin(t), sp.cos(t))
assert sp.simplify(mink(k1, k1)) == 0 and sp.simplify(mink(k2, k2)) == 0
assert sp.simplify(mink(k1, e1)) == 0 and sp.simplify(mink(k2, e2)) == 0
# outward: k_i spatial part points away from the interior bisector
bis = (0, sp.cos(t/2), sp.sin(t/2))
print("(m1) outward checks k1.bis, k2.bis:", sp.simplify(mink((0,)+k1[1:], bis)), "|", sp.simplify(mink((0,)+k2[1:], bis)))
u = [e1[i] + c1*k1[i] for i in range(3)]; v = [e2[i] + c2*k2[i] for i in range(3)]
print("(m1) |u|^2, |v|^2 =", sp.simplify(mink(u, u)), sp.simplify(mink(v, v)), " (length preserved)")
x = sp.expand(sp.simplify(mink(u, v)))
print("(m1) x(c1,c2) =", sp.factor_terms(x))
# a(theta) = f(cos theta): a' = -sin f', a'' = sin^2 f'' - cos f'  =>  f', f'' in terms of a', a''
ap, app, fp, fpp = sp.symbols("ap app fp fpp")
sol = sp.solve([sp.Eq(ap, -sp.sin(t)*fp), sp.Eq(app, sp.sin(t)**2*fpp - sp.cos(t)*fp)], [fp, fpp], dict=True)[0]
# second derivative of f(x(c)) along c = tau*d at tau=0: f'' (grad x . d)^2 + f' (d^T Hess x d)
gx = [sp.diff(x, c1).subs({c1: 0, c2: 0}), sp.diff(x, c2).subs({c1: 0, c2: 0})]
Hx = sp.Matrix([[sp.diff(x, a, b) for b in (c1, c2)] for a in (c1, c2)]).subs({c1: 0, c2: 0})
dv = sp.Matrix([d1, d2])
H = fpp*(gx[0]*d1 + gx[1]*d2)**2 + fp*(dv.T*Hx*dv)[0]
H = sp.expand(H.subs(sol))
Q = app + sp.tan(t/2)/2*ap
zz = sp.symbols('z', positive=True)
def zero(expr, var):   # reduce via the half-angle substitution var = 2 atan(z): a rational function of z
    return sp.simplify(sp.expand_trig(expr.subs(var, 2*sp.atan(zz))))
r11 = zero(H.subs({d1: 1, d2: 1}) - 4*Q, t)
r10 = zero(H.subs({d1: 1, d2: 0}) - (Q - sp.cot(t/2)/2*ap), t)
print("(m1) Hess(1,1) - 4Q =", r11, "   Hess(1,0) - (Q - cot(t/2)a'/2) =", r10)
coef = sp.simplify(sp.expand(H).coeff(d1*d2) - 2*sp.expand(H).coeff(d1**2))
print("(m1) H = (d1+d2)^2 A + d1 d2 B with B =", sp.simplify(sp.expand_trig(coef)), " (<= 0 when a' <= 0, so min on simplex at d1=d2)")
# off-diagonal (cross-edge) term alone, h12 = (1/2) d1d2-coefficient: SSA gives h12 >= 0 by itself (verifier, 2026-10-17)
h12 = sp.expand(H).coeff(d1*d2)/2
print("(m1) h12 - CHL[a] =", zero(h12 - (app + ap/sp.sin(t)), t), " (the SSA cross term alone reproduces CHL09)")
print("(m1) h11 - (Q - cot(t/2)a'/2) =", zero(sp.expand(H).coeff(d1**2) - (Q - sp.cot(t/2)/2*ap), t))
# future-past variant: k2 -> past-outward (-1,-sin,cos)
k2m = (-1, -sp.sin(t), sp.cos(t)); vm = [e2[i] + c2*k2m[i] for i in range(3)]
xm = sp.expand(mink(u, vm)); Hxm = sp.diff(xm, c1, c2).subs({c1: 0, c2: 0})
print("(m1) future-past cross term d^2x/dc1dc2 =", sp.simplify(Hxm), "(sign opposite to future-future", sp.simplify(Hx[0, 1]), ")")
# spectral kernel
eps = sp.symbols('epsilon', positive=True)
mode = (sp.cosh(s*(sp.pi - t)) - 1)/s**2
KQ = sp.simplify((sp.diff(mode, t, 2) + sp.tan(t/2)/2*sp.diff(mode, t)).subs(t, sp.pi - eps))
print("(m1) K_Q(s,eps) =", KQ)
CHLk = sp.simplify((sp.diff(mode, t, 2) + sp.diff(mode, t)/sp.sin(t)).subs(t, sp.pi - eps))
idt = zero(KQ - (CHLk - sp.cot((sp.pi - eps)/2)/2*sp.diff(mode, t).subs(t, sp.pi - eps)), eps)
print("(m1) identity Q = CHL - cot(theta/2) a'/2 on a mode: residual =", idt)

# ---------------- (m2) independent finite-difference Hessian ----------------
mp.mp.dps = 40
def xnum(th, a1, a2):
    U = [mp.mpf(0) + a1, mp.mpf(1), -a1]
    V = [a2, mp.cos(th) - a2*mp.sin(th), mp.sin(th) + a2*mp.cos(th)]
    return -U[0]*V[0] + U[1]*V[1] + U[2]*V[2]
pi = mp.pi
def aw(w):
    return lambda th: mp.e**(-w*th)/th + mp.e**(-w*(2*pi - th))/(2*pi - th) - 2*mp.e**(-w*pi)/pi
EMI = lambda th: 1 + (pi - th)*mp.cot(th)
AMIN = lambda th: mp.log(1/mp.sin(th/2))
CHORD = lambda th: mp.cot(th/2)/2
def Qf(f, th):
    return mp.diff(f, th, 2) + mp.tan(th/2)/2*mp.diff(f, th, 1)
h = mp.mpf('1e-12'); worst = 0
for name, f in (("EMI", EMI), ("a_w(3)", aw(3)), ("a_min", AMIN)):
    for deg in (20, 60, 90, 120, 160):
        th = mp.radians(deg)
        F = lambda a1, a2: f(mp.acos(xnum(th, a1, a2)))
        fd = (F(h, h) - 2*F(0, 0) + F(-h, -h))/h**2       # direction d=(1,1)
        fd10 = (F(h, 0) - 2*F(0, 0) + F(-h, 0))/h**2
        rel = abs(fd/(4*Qf(f, th)) - 1); rel10 = abs(fd10/(Qf(f, th) - mp.cot(th/2)/2*mp.diff(f, th)) - 1)
        worst = max(worst, rel, rel10)
print(f"(m2) finite-difference Hessian vs 4Q and single-edge form: worst relative deviation = {mp.nstr(worst, 3)}")

# ---------------- (m3) kernel minimum ----------------
S = np.concatenate([np.linspace(1e-6, 2, 400), np.linspace(2, 60, 600)])
E = np.linspace(1e-4, np.pi - 1e-4, 1500)
SS, EE = np.meshgrid(S, E)
with np.errstate(over='ignore'):
    KQn = np.cosh(SS*EE) - 0.5/np.tan(EE/2)*np.sinh(SS*EE)/SS
    rel = KQn/np.cosh(SS*EE)
print(f"(m3) min K_Q on grid = {np.nanmin(KQn):.3e}; min K_Q/cosh = {np.nanmin(rel):.3e} at s->0, eps->0 (analytic min 0)")
print(f"(m3) check: tanh(s eps)/s <= eps <= 2 tan(eps/2) everywhere on grid: {bool(np.all(np.tanh(SS*EE)/SS <= 2*np.tan(EE/2)*(1+1e-14)))}")
rng = np.random.default_rng(31); bad = 0
for _ in range(2000):
    n = rng.integers(1, 6); ss = rng.exponential(3, n); mm = rng.exponential(1, n)
    for th in np.linspace(0.02, np.pi - 0.02, 60):
        ep = np.pi - th
        q = np.sum(mm*(np.cosh(ss*ep) - 0.5*np.tan(th/2)*np.sinh(ss*ep)/ss))
        bad += q < -1e-12*np.sum(mm*np.cosh(ss*ep))
print(f"(m3) random positive discrete measures (2000 x 60 angles): Q < 0 in {bad} cases")

# ---------------- (m4) the pre-registered table ----------------
degs = [d for d in range(2, 179, 1)]
def scan(f):
    vals = [(d, Qf(f, mp.radians(d))) for d in degs]
    return min(vals, key=lambda p: p[1]), vals
print("(m4) function: min Q over 2..178 deg  [verdict]")
for w in (1, 3, 6, 10):
    (dm, qm), _ = scan(aw(w))
    print(f"  a_w w={w:>2}: min Q = {mp.nstr(qm, 6)} at {dm} deg  [{'pass' if qm >= 0 else 'FAIL'}]")
(dm, qm), _ = scan(EMI); print(f"  EMI (positive control): min Q = {mp.nstr(qm, 6)} at {dm} deg  [{'pass' if qm >= 0 else 'FAIL'}]")
dev = max(abs(Qf(AMIN, mp.radians(d)) - mp.cot(mp.radians(d)/2)**2/4) for d in degs)
print(f"  a_min (known answer Q = cot^2(theta/2)/4): max |Q - known| = {mp.nstr(dev, 3)}")
DR = lambda th: EMI(th) + 1e4*aw(6)(th)
(dm, qm), _ = scan(DR); print(f"  EMI + 1e4*a_6 (dressed, kappa/sigma ~ 1e4): min Q = {mp.nstr(qm, 6)} at {dm} deg  [{'pass' if qm >= 0 else 'FAIL'}]")
_, vals = scan(CHORD); neg = [d for d, q in vals if q < 0]
thr = mp.degrees(2*mp.atan(mp.sqrt(2)))
print(f"  chord (negative control): Q < 0 on {neg[0]}..{neg[-1]} deg ({len(neg)} angles); predicted threshold {mp.nstr(thr, 6)} deg  [{'fires' if neg and neg[0] == int(mp.ceil(thr)) else 'MISBEHAVES'}]")
z = mp.findroot(lambda th: Qf(CHORD, th), mp.radians(110)); print(f"  chord: root of Q at {mp.nstr(mp.degrees(z), 10)} deg")
