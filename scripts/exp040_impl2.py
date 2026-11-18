"""EXP-040 Part B, Implementation 2 (registration and amendment A in report.md).
Independent of Impl-1 (scripts/exp040_impl1_dim_spread.py) at every numerical step:
  scalar  next-nearest-neighbour chain, w^2 = m^2 + 4 s^2 + (4/3) s^4, s = sin(k/2)   (Impl-1: nearest neighbour)
  Dirac   two-component Wilson fermion h(k) = sin k sx + (m + 1 - cos k) sz           (Impl-1: staggered)
  correlators by adaptive quadrature in k (QUADPACK Fourier weight), no ring           (Impl-1: FFT on a ring)
  scalar entropy from singular values of Lx^T Lp (Cholesky)                            (Impl-1: eigh + sqrt)
  c = L dS/dL by a 5-point stencil at L0 = 160, 320, 640, extrapolated                (Impl-1: 2-pt, 120/240)
  Mellin integral by Gauss-Legendre panels in log t on direct nodes, t in [1e-5, 25]   (Impl-1: spline, t >= 2.5e-3)
Formulas: kappa_D = P(D) M(D), P = [(D-2) 2^(D-3) pi^((D-2)/2) Gamma((D-2)/2)]^-1, M = int t^(D-3) c(t) dt  [CH09 ttt1];
C_T free (Osborn-Petkou via BFGLM26 eq. CTfreefields, tr 1 = 2); Einstein k and C_T from BFGLM26 eqs. kholo, CTholo."""
import sys, math, json, time, warnings
warnings.filterwarnings("ignore", message=".*roundoff error.*")
import numpy as np
from scipy.integrate import quad
from scipy.special import gamma, k1
from scipy.optimize import brentq

EPS = dict(epsabs=1e-15, epsrel=1e-13, limit=800)

def kint(f, r, m):
    """(1/pi) int_0^pi f(k) cos(k r) dk, split at the mass scale."""
    edges = [0.0, min(20 * m, 1e-2), 1e-2, 0.3, math.pi]
    edges = sorted(set(e for e in edges if e <= math.pi))
    s = 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        if b <= a: continue
        if r == 0: s += quad(f, a, b, **EPS)[0]
        else:      s += quad(f, a, b, weight="cos", wvar=r, **EPS)[0]
    return s / math.pi

def sint(f, r, m):
    """(1/pi) int_0^pi f(k) sin(k r) dk."""
    if r == 0: return 0.0
    edges = [0.0, min(20 * m, 1e-2), 1e-2, 0.3, math.pi]
    edges = sorted(set(e for e in edges if e <= math.pi))
    s = 0.0
    for a, b in zip(edges[:-1], edges[1:]):
        if b <= a: continue
        s += quad(f, a, b, weight="sin", wvar=r, **EPS)[0]
    return s / math.pi

def scalar_corr(m, R):
    w = lambda k: math.sqrt(m * m + 4 * math.sin(k / 2) ** 2 + (4 / 3) * math.sin(k / 2) ** 4)
    X = np.array([kint(lambda k: 0.5 / w(k), r, m) for r in range(R + 1)])
    P = np.array([kint(lambda k: 0.5 * w(k), r, m) for r in range(R + 1)])
    return X, P

def wilson_corr(m, R):
    M = lambda k: m + 1 - math.cos(k)
    E = lambda k: math.sqrt(math.sin(k) ** 2 + M(k) ** 2)
    fz = np.array([kint(lambda k: M(k) / (2 * E(k)), r, m) for r in range(R + 1)])
    fx = np.array([sint(lambda k: math.sin(k) / (2 * E(k)), r, m) for r in range(R + 1)])
    return fx, fz

def S_scalar(X, P, L):
    idx = np.abs(np.subtract.outer(np.arange(L), np.arange(L)))
    Lx = np.linalg.cholesky(X[idx]); Lp = np.linalg.cholesky(P[idx])
    nu = np.clip(np.linalg.svd(Lx.T @ Lp, compute_uv=False), 0.5, None)
    a, b = nu + 0.5, nu - 0.5
    bb = b[b > 1e-300]
    return float(np.sum(a * np.log(a)) - np.sum(bb * np.log(bb)))

def S_wilson(fx, fz, L):
    r = np.subtract.outer(np.arange(L), np.arange(L))        # i - j
    ar = np.abs(r); sg = np.sign(r)
    FX = sg * fx[ar]; FZ = fz[ar]
    C = np.zeros((2 * L, 2 * L), complex)
    C[0::2, 0::2] = 0.5 * np.eye(L) - FZ
    C[1::2, 1::2] = 0.5 * np.eye(L) + FZ
    C[0::2, 1::2] = -1j * FX
    C[1::2, 0::2] = -1j * FX
    C = (C + C.conj().T) / 2
    nu = np.clip(np.linalg.eigvalsh(C), 1e-300, 1 - 1e-16)
    return float(-np.sum(nu * np.log(nu) + (1 - nu) * np.log1p(-nu)))

def c_at(kind, t, L0):
    m = t / L0
    if kind == "S":
        X, P = scalar_corr(m, L0 + 2); S = lambda L: S_scalar(X, P, L)
    else:
        fx, fz = wilson_corr(m, L0 + 2); S = lambda L: S_wilson(fx, fz, L)
    d = (-S(L0 + 2) + 8 * S(L0 + 1) - 8 * S(L0 - 1) + S(L0 - 2)) / 12
    return L0 * d

SIZES = (160, 320, 640)
def c_ext(kind, t):
    c = [c_at(kind, t, L) for L in SIZES]
    x = [1 / L for L in SIZES]
    if kind == "S": A = np.array([[1, xi ** 2, xi ** 4] for xi in x])
    else:           A = np.array([[1, xi, xi ** 2] for xi in x])
    cinf = float(np.linalg.solve(A, c)[0])
    two = (4 * c[2] - c[1]) / 3                                 # registered 2-size 1/L^2 form (320, 640)
    return cinf, c, two

# ----- closed forms -----
def P_D(D): return 1 / ((D - 2) * 2 ** (D - 3) * math.pi ** ((D - 2) / 2) * gamma((D - 2) / 2))
def Om(D): return 2 * math.pi ** (D / 2) / gamma(D / 2)                    # Omega_{D-1}
def CT_S(D): return D / (D - 1) / Om(D) ** 2
def CT_D(D): return (D / 2) * 2 / Om(D) ** 2                              # tr 1 = 2
def k_holo(D): return 2 ** (D - 3) * math.pi ** ((D - 1) / 2) * gamma(D / (2 * (D - 1))) ** (D - 1) / ((D - 2) * gamma(1 / (2 * (D - 1))) ** (D - 1))
def CT_holo(D): return gamma(D + 2) / (8 * math.pi ** ((D + 2) / 2) * (D - 1) * gamma(D / 2))
def rE(D): return k_holo(D) / CT_holo(D)

if __name__ == "__main__":
    t0 = time.time(); out = {}
    print("=== K3 large t (c / [N_p (t/4) K1(2t)] at t = 6, tolerance 2e-3) ===")
    for kind, Np in (("S", 1), ("D", 2)):
        cinf, cs, two = c_ext(kind, 6.0); ratio = cinf / (Np * 6 / 4 * k1(12.0))
        print(f"  {kind}: {ratio:.6f}  (sizes {[f'{x/(Np*1.5*k1(12.0)):.5f}' for x in cs]})  {'PASS' if abs(ratio-1)<=2e-3 else 'FAIL'}")
    print(f"  [{time.time()-t0:.0f}s]")
    print("=== K2 small t ===")
    for t in (1e-4, 1e-3, 1e-2):
        cinf, cs, two = c_ext("D", t); ref = 1/3 - t*t*math.log(t)**2/3; tol = 3*t*t*abs(math.log(t))
        print(f"  D t={t:g}: c={cinf:.9f} ref={ref:.9f} |diff|={abs(cinf-ref):.2e} tol {tol:.2e} {'PASS' if abs(cinf-ref)<=tol else 'FAIL'}   sizes {[f'{x:.7f}' for x in cs]}")
    for t in (1e-5, 1e-4):
        cinf, cs, two = c_ext("S", t); ref = 1/3 + 1/(2*math.log(t)); tol = 2/math.log(t)**2
        print(f"  S t={t:g}: c={cinf:.7f} ref={ref:.7f} |diff|={abs(cinf-ref):.2e} tol {tol:.2e} {'PASS' if abs(cinf-ref)<=tol else 'FAIL'}   sizes {[f'{x:.7f}' for x in cs]}")
    print(f"  [{time.time()-t0:.0f}s]")
    print("=== K4 formulas ===")
    for D in (2.5, 3, 3.5, 4, 5, 6):
        alt = ((1/4)*(2**(D-1)*math.pi**((D-1)/2)/(D-2))*(gamma(D/(2*D-2))/gamma(1/(2*D-2)))**(D-1)) / ((D+1)/(D-1)*gamma(D+1)/(math.pi**(D/2)*gamma(D/2))/(8*math.pi))
        print(f"  D={D}: BFGLM26 {rE(D):.15g}  Impl-1 form {alt:.15g}  rel {rE(D)/alt-1:.1e}")
    print(f"  D=3 vs pi^2 Gamma(3/4)^4/6: {rE(3)/(math.pi**2*gamma(0.75)**4/6)-1:.1e}")

    # ----- c(t) on Gauss-Legendre panels in u = log t -----
    xg, wg = np.polynomial.legendre.leggauss(8)
    edges = np.linspace(math.log(1e-5), math.log(25.0), 15)
    U, W = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        U += list((b - a) / 2 * xg + (a + b) / 2); W += list((b - a) / 2 * wg)
    U, W = np.array(U), np.array(W)
    tab = {}
    for kind in ("S", "D"):
        rows = [c_ext(kind, float(math.exp(u))) for u in U]
        tab[kind] = dict(cinf=[r[0] for r in rows], sizes=[r[1] for r in rows], two=[r[2] for r in rows])
        print(f"[{kind}] {len(U)} nodes done at {time.time()-t0:.0f}s", flush=True)
    tmin = 1e-5
    # boundary value for tails: c at tmin, from a dedicated evaluation
    cS0 = c_ext("S", tmin)[0]; cD0 = c_ext("D", tmin)[0]
    def M(kind, D, col="cinf", tail="model"):
        cv = np.array(tab[kind][col])
        body = float(np.sum(W * np.exp((D - 2) * U) * cv))
        if kind == "D" or tail == "const":
            c0 = cD0 if kind == "D" else cS0
            tl = c0 * tmin ** (D - 2) / (D - 2)
        else:
            lnts = math.log(tmin) - 1 / (2 * (cS0 - 1 / 3))      # ln t*
            tl = quad(lambda u: math.exp((D - 2) * u) * (1/3 + 1/(2*(u - lnts))), -200, math.log(tmin), limit=400)[0]
        return body + tl, tl / (body + tl)
    def ratios(D, col="cinf", tail="model"):
        MS, fS = M("S", D, col, tail); MD, fD = M("D", D, col, tail)
        s = P_D(D) * MS / CT_S(D); d = P_D(D) * MD / CT_D(D); e = rE(D)
        return s, d, e, fS, fD

    print("\n=== K1: CH09 Table, kappa per degree of freedom ===")
    CH = {3: (3.97e-2, 3.61e-2), 4: (5.54e-3, 5.38e-3), 5: (1.31e-3, 1.30e-3), 6: (4.08e-4, 4.06e-4)}
    k1ok = True
    for D, (b, f) in CH.items():
        kb = P_D(D) * M("S", D)[0]; kf = P_D(D) * M("D", D)[0] / 2
        ulp = lambda v: 0.5 * 10 ** (math.floor(math.log10(v)) - 2)
        okb = abs(kb - b) <= ulp(b); okf = abs(kf - f) <= ulp(f); k1ok &= okb and okf
        print(f"  D={D}: boson {kb:.6e} vs {b:.2e} {'PASS' if okb else 'FAIL'};  fermion/Majorana {kf:.6e} vs {f:.2e} {'PASS' if okf else 'FAIL'}")
    print("  K1", "PASS" if k1ok else "FAIL")

    print("\n=== d-scan (Impl-2), kappa_D/C_T ===")
    print("    D     scalar      Dirac     Einstein |  S/E      D/E      S/D   | tail frac S, D")
    Ds = (2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 4.0, 4.5, 5.0, 6.0)
    for D in Ds:
        s, d, e, fS, fD = ratios(D)
        out[D] = dict(scalar=s, dirac=d, einstein=e)
        print(f"  {D:4.2f} {s:10.5f} {d:10.5f} {e:10.5f} | {s/e:7.4f}  {d/e:7.4f}  {s/d:7.4f} | {fS:.1e} {fD:.1e}")
    print("\n=== crossings (registered: Impl-2 main; nuisance variants) ===")
    cr = {}
    for name, f in (("S/D", lambda D, **k: ratios(D, **k)[0] / ratios(D, **k)[1]),
                    ("S/E", lambda D, **k: ratios(D, **k)[0] / ratios(D, **k)[2]),
                    ("D/E", lambda D, **k: ratios(D, **k)[1] / ratios(D, **k)[2])):
        main = brentq(lambda D: f(D) - 1, 2.4, 3.2)
        v2 = brentq(lambda D: f(D, col="two") - 1, 2.4, 3.2)
        vc = brentq(lambda D: f(D, tail="const") - 1, 2.4, 3.2)
        cr[name] = dict(main=main, two_size=v2, const_tail=vc)
        print(f"  {name}: D_c = {main:.4f}   [2-size 1/L^2 form {v2:.4f}; constant scalar tail {vc:.4f}]")
    json.dump(dict(U=list(U), W=list(W), tab=tab, cS0=cS0, cD0=cD0, scan=out, crossings=cr), open("scripts/exp040_impl2.json", "w"), indent=1)
    print(f"\nwall {time.time()-t0:.0f}s")
