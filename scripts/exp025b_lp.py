"""EXP-025b: linear programs (pre-registered in report.md).
Variables: K = F(0) = kappa/4, and a_i = a(theta_i) on a grid theta_0 = theta_min < ... < theta_N = pi (a_N = 0).
CC : F = sqrt(u) a convex in u = tan^2(theta/4), including the endpoint (0, K).
C2 : a nonincreasing, convex in theta.   C3 : b tan(theta/2) nonincreasing, b = -a' (midpoints).   C5 : a(pi) = 0.
LP1: min K s.t. a(pi/2) = 1              -> kappa / a(pi/2) = 4K
LP2: min K s.t. last-midpoint b tan(theta/2) = 4 (sigma = 1)  -> kappa / sigma = 4K
"""
import numpy as np, scipy.sparse as sp
from scipy.optimize import linprog
from math import pi

def grid(N, thmin):
    n1 = N//3; n2 = N - n1
    g1 = np.geomspace(thmin, pi/2, n1 + 1)                        # dense toward 0
    x = np.linspace(0, 1, n2 + 1); g2 = pi/2 + (pi/2)*np.sin(x*pi/2)  # clustered toward pi
    th = np.unique(np.concatenate([g1, g2])); th[-1] = pi
    return th

def build(N, thmin, use_cc=True, norm='a90', c3='exact', use_c3=True):
    th = grid(N, thmin); M = len(th); nv = M + 1              # x = [K, a_0..a_{M-1}]
    u = np.tan(th/4)**2; w = np.sqrt(u)
    rows = [];
    def add(coefs):                                            # coefs: dict var->coef, constraint sum <= 0
        rows.append(coefs)
    A = lambda i: i + 1                                        # index of a_i
    # C2: nonincreasing
    for i in range(M - 1): add({A(i+1): 1.0, A(i): -1.0})
    # C2: convex in theta (second divided difference >= 0  ->  -(...) <= 0)
    for i in range(1, M - 1):
        h1, h2 = th[i] - th[i-1], th[i+1] - th[i]
        add({A(i+1): -1/h2, A(i): 1/h2 + 1/h1, A(i-1): -1/h1})
    # C3: B_i = -(a_{i+1}-a_i)/h_i * tan(m_i/2) nonincreasing:  B_{i+1} - B_i <= 0
    m = 0.5*(th[1:] + th[:-1]); h = np.diff(th); t = np.tan(m/2)
    # exact relaxation: g = b tan(theta/2) nonincreasing  =>  (a_i - a_{i+1}) / C_i  nonincreasing in i,
    # with C_i = int_{I_i} cot(theta/2) dtheta = 2 log(sin(th_{i+1}/2)/sin(th_i/2))  (implied by C3 for every C3 function)
    Ci = 2*np.log(np.sin(th[1:]/2)/np.sin(th[:-1]/2)); Ci[-1] = 2*np.log(1/np.sin(th[-2]/2))
    coef_hi, coef_lo = (t/h, t/h) if c3 == 'mid' else (1/Ci, 1/Ci)
    if use_c3:
        for i in range(M - 2):
            c = {}
            c[A(i+2)] = c.get(A(i+2), 0) - coef_hi[i+1]; c[A(i+1)] = c.get(A(i+1), 0) + coef_hi[i+1]
            c[A(i+1)] = c.get(A(i+1), 0) + coef_lo[i];   c[A(i)] = c.get(A(i), 0) - coef_lo[i]
            add(c)
    # CC: points (0, K), (u_i, w_i a_i)
    if use_cc:
        U = np.concatenate([[0.0], u])
        def Fvar(j): return (0, 1.0) if j == 0 else (A(j-1), w[j-1])
        for j in range(1, len(U) - 1):
            d1, d2 = U[j] - U[j-1], U[j+1] - U[j]
            c = {}
            for jj, coef in ((j+1, -1/d2), (j, 1/d2 + 1/d1), (j-1, -1/d1)):
                v, s = Fvar(jj); c[v] = c.get(v, 0) + coef*s
            add(c)
    r, cidx, vals = [], [], []
    for k, c in enumerate(rows):
        for v, s in c.items(): r.append(k); cidx.append(v); vals.append(s)
    Aub = sp.csr_matrix((vals, (r, cidx)), shape=(len(rows), nv)); bub = np.zeros(len(rows))
    Aeq = []; beq = []
    e = np.zeros(nv); e[A(M-1)] = 1; Aeq.append(e); beq.append(0.0)           # a(pi) = 0
    if norm == 'a90':
        i90 = int(np.argmin(abs(th - pi/2))); assert abs(th[i90] - pi/2) < 1e-12
        e = np.zeros(nv); e[A(i90)] = 1; Aeq.append(e); beq.append(1.0)
    elif c3 == 'mid':  # last midpoint: B = -(a_{M-1}-a_{M-2})/h * tan(m/2) = 4
        e = np.zeros(nv); e[A(M-1)] = -t[-1]/h[-1]; e[A(M-2)] = t[-1]/h[-1]; Aeq.append(e); beq.append(4.0)
    else:              # exact relaxation of sigma = 1: g >= 4 sigma everywhere  =>  a_i - a_{i+1} >= 4 C_i
        extra = sp.lil_matrix((M - 1, nv))
        for i in range(M - 1): extra[i, A(i)] = -1.0; extra[i, A(i+1)] = 1.0
        Aub = sp.vstack([Aub, extra.tocsr()]).tocsr(); bub = np.concatenate([bub, -4*Ci])
    return Aub, bub, np.array(Aeq), np.array(beq), th, nv, w

def solve(N, thmin, **kw):
    Aub, bub, Aeq, beq, th, nv, w = build(N, thmin, **kw)
    c = np.zeros(nv); c[0] = 1.0
    res = linprog(c, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=[(0, None)]*nv, method='highs')
    return res, th

def feasible(afun, kappa, N, thmin, norm, **kw):
    """plug a physical curve into the discrete rows: returns max violation of A_ub x <= b_ub (relative) and eq residual"""
    Aub, bub, Aeq, beq, th, nv, w = build(N, thmin, norm=norm, **kw)
    def safe(t):
        if t >= pi - 1e-12: return 0.0
        try: return afun(t)
        except RuntimeError: return np.nan
    a = np.array([safe(t) for t in th])
    if np.isnan(a).any():
        bad = th[np.isnan(a)]; raise RuntimeError(f"curve evaluation failed at {len(bad)} grid angles, e.g. {bad[:3]}")
    if norm == 'a90': sc = 1/afun(pi/2)
    else:             sc = 1.0
    x = np.concatenate([[kappa/4], a])*sc
    viol = Aub @ x - bub; scale = np.abs(Aub).max(axis=1).toarray().ravel()*np.abs(x).max()
    return (viol/np.maximum(scale, 1e-300)).max()

if __name__ == "__main__":
    import sys, io, contextlib
    sys.path.insert(0, __file__.rsplit('/', 1)[0])
    with contextlib.redirect_stdout(io.StringIO()):
        from exp001_measure import aE_over_CT
    from math import gamma
    chord1, chord2 = 2.0, 16*0.4023711713
    print(f"floors from the chord bound: LP1 >= {chord1}, LP2 >= {chord2:.4f};  (R) threshold 2pi/3 = {2*pi/3:.6f}")
    print("\nCONTROL A: no CC (must give kappa ~ 0; the no-bound theorem)")
    for c3 in ('mid', 'exact'):
        for norm in ('a90', 'sig'):
            r, th = solve(1600, 1e-3, use_cc=False, norm=norm, c3=c3)
            print(f"   C3={c3:5s} {norm}: status {r.status}  kappa/norm = {4*r.x[0]:.6f}")
    print("\nCONTROL B: CC + C2 + C5 without C3 (LP1 must be exactly 2: a = (kappa/2)cot(theta/2) is feasible and optimal)")
    for N in (400, 1600):
        r, th = solve(N, 1e-3, use_cc=True, norm='a90', use_c3=False)
        print(f"   N={N:5d}: status {r.status}  kappa/a(pi/2) = {4*r.x[0]:.8f}")
    print("\nCONTROL C: physical curves must satisfy every discrete row (max relative violation should be <= ~1e-12 for 'exact')")
    kE = pi**2*gamma(0.75)**4/6
    aEMI = lambda t: 1 + (pi - t)/np.tan(t)
    for name, f, k in (("EMI", aEMI, pi), ("Einstein", aE_over_CT, kE)):
        for c3 in ('mid', 'exact'):
            v = feasible(f, k, 800, 1e-2, 'a90', c3=c3)
            print(f"   {name:8s} C3={c3:5s}: max relative violation {v:+.2e}  -> {'feasible' if v <= 1e-9 else 'VIOLATES a discrete row'}")
    print("\nWITH CC (both discretisations of C3; 'exact' is a rigorous relaxation)")
    out = {}
    for c3 in ('mid', 'exact'):
        for norm in ('a90', 'sig'):
            for thmin in (1e-3, 1e-4):
                for N in (200, 400, 800, 1600, 3200):
                    r, th = solve(N, thmin, use_cc=True, norm=norm, c3=c3)
                    val = 4*r.x[0] if r.status == 0 else float('nan'); out[(c3, norm, thmin, N)] = val
                    extra = f"  kappa/C_T = {val*pi**2/24:.5f}" if norm == 'sig' else f"  vs 2pi/3: {val - 2*pi/3:+.5f}"
                    print(f"   C3={c3:5s} {'LP1 kappa/a(pi/2)' if norm == 'a90' else 'LP2 kappa/sigma  '}  thmin={thmin:.0e} N={N:5d}: status {r.status}  value {val:.6f}{extra}")
    for c3 in ('mid', 'exact'):
        for norm in ('a90', 'sig'):
            v = [out[(c3, norm, tm, N)] for tm in (1e-3, 1e-4) for N in (200, 400, 800, 1600, 3200)]
            print(f"   C3={c3:5s} {norm}: range over the sweep [{min(v):.6f}, {max(v):.6f}], drift {max(v) - min(v):.2e}")
