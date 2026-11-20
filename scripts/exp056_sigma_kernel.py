"""EXP-056 instrument (gap (c) of Neon's Lemma U): the phi-bubble B_n on H^2 x S^1_{2 pi n} (Weyl image of the cone),
in Matsubara sector omega_q = q/n, on the imaginary Mehler-Fock axis k = i kappa:
  B_n(i kappa, q) = (2/(2 pi n)) sum_{m in Z} Int_0^inf 2 pi sinh(rho) P_{kappa-1/2}(cosh rho) g_{nu_m}(rho) g_{nu_{q-m}}(rho) drho,
  g_nu = Q_{nu-1/2}(cosh rho)/(2 pi)  (H^2 Green function with Mehler-Fock transform 1/(k^2+nu^2)),
  nu_m = sqrt(m^2/n^2 + a_n) (m != 0), nu_0 = alpha_n (alternate branch; a_n = alpha_n^2, EXP-053 root).
n = 1 closed form (position space, G_1 = 1/(4 pi sqrt(2(cosh rho - cos tau)))):  B_1(i kappa, q) = 1/4 Int P_{kappa-1/2}(cosh rho) e^{-|q| rho} drho.
[model: Opus 5.5]"""
import numpy as np

def g(nu, rho, dv=0.04):
    """H^2 Green function g_nu = Q_{nu-1/2}(cosh rho)/(2 pi), nu > -1/2, from the toroidal integral
    Q_{nu-1/2}(cosh rho) = Int_0^inf e^{-nu(rho+s)} ds / sqrt(4 sinh(rho+s/2) sinh(s/2)), with s = u^2, u = c sinh v,
    c = sqrt(2 tanh rho) (removes the endpoint singularity and the small-rho log scale); trapezoid in v (spectral)."""
    rho = np.asarray(rho, float)[:, None]
    c = np.sqrt(2 * np.tanh(rho))
    V = np.arcsinh(np.sqrt(60.0 / (nu + 0.5)) / c)
    v = np.arange(0.0, float(V.max()) + dv, dv)[None, :]
    u = c * np.sinh(v); s = u * u
    with np.errstate(under="ignore", over="ignore", invalid="ignore", divide="ignore"):
        f = 2 * u * np.exp(-nu * (rho + s)) / np.sqrt(4 * np.sinh(rho + s / 2) * np.sinh(s / 2)) * c * np.cosh(v)
    f[:, 0] = 2 * np.exp(-nu * rho[:, 0]) * c[:, 0] / np.sqrt(2 * np.sinh(rho[:, 0]))   # u -> 0 limit
    f = np.nan_to_num(np.where(v <= V, f, 0.0))
    w = np.full(v.shape[1], dv); w[0] = dv / 2
    return (f @ w) / (2 * np.pi)

_Pcache = {}
def P(nu, rho):
    """Legendre P_nu(cosh rho) via mpmath (cached per (nu, grid))."""
    from mpmath import mp, legenp, cosh, mpf, re
    rho = np.asarray(rho, float); key = (round(float(nu), 14), rho.size, float(rho[0]), float(rho[-1]))
    if key not in _Pcache:
        with mp.workdps(20):
            _Pcache[key] = np.array([float(re(legenp(nu, 0, cosh(mpf(float(r))), type=3))) for r in rho])
    return _Pcache[key]

def rho_grid(rmax, npan=24, nper=48):
    edges = np.concatenate([[0.0], np.geomspace(1e-6, 1.0, 8), np.linspace(1.0, rmax, npan)[1:]])
    x, w = np.polynomial.legendre.leggauss(nper)
    R = []; W = []
    for a, b in zip(edges[:-1], edges[1:]):
        R.append(0.5 * (b - a) * x + 0.5 * (b + a)); W.append(0.5 * (b - a) * w)
    return np.concatenate(R), np.concatenate(W)

def nus(n, alpha, mmax):
    m = np.arange(-mmax, mmax + 1)
    nu = np.sqrt((m / n) ** 2 + alpha ** 2); nu[m == 0] = alpha
    return m, nu

def threshold(n, alpha, q, mmax=50):
    m, nu = nus(n, alpha, mmax + abs(q)); d = dict(zip(m, nu))
    return 0.5 + min(d[j] + d[q - j] for j in range(-mmax, mmax + 1))

def B(n, alpha, q, kappa, M=200, rmax=None):
    kth = threshold(n, alpha, q)
    if kappa >= kth: raise ValueError("kappa above threshold")
    if rmax is None: rmax = min(400.0, 40.0 / (kth - kappa))
    R, W = rho_grid(rmax)
    base = 2 * np.pi * np.sinh(R) * P(kappa - 0.5, R) * W
    m, nu = nus(n, alpha, M + abs(q)); d = dict(zip(m, nu))
    gcache = {}
    def gg(j):
        v = float(d[j])
        if v not in gcache: gcache[v] = g(v, R)
        return gcache[v]
    def S(MM):
        return (2 / (2 * np.pi * n)) * sum(float(base @ (gg(j) * gg(q - j))) for j in range(-MM, MM + 1))
    s1, s2 = S(M // 2), S(M)
    return 2 * s2 - s1, abs(s2 - s1)            # Richardson in 1/M; second value = size of the tail correction

def B1_closed(q, kappa, rmax=None):
    if rmax is None: rmax = min(400.0, 40.0 / (0.5 + abs(q) - kappa))
    R, W = rho_grid(rmax)
    return 0.25 * float((P(kappa - 0.5, R) * np.exp(-abs(q) * R)) @ W)

# ---- complex-k evaluation and argument-principle zero count ----
def weight(n, alpha, q, kmax_im, M=200):
    """W(rho) drho such that B_n(k, q) = sum W * P_{-1/2+ik}(cosh rho); grid sized for |Im k| <= kmax_im < threshold."""
    kth = threshold(n, alpha, q)
    rmax = min(400.0, 40.0 / (kth - kmax_im))
    R, Wt = rho_grid(rmax)
    m, nu = nus(n, alpha, M + abs(q)); d = dict(zip(m, nu)); gc = {}
    def gg(j):
        v = float(d[j])
        if v not in gc: gc[v] = g(v, R)
        return gc[v]
    def S(MM): return (2 / (2 * np.pi * n)) * sum(gg(j) * gg(q - j) for j in range(-MM, MM + 1))
    Wr = 2 * S(M) - S(M // 2)
    return R, 2 * np.pi * np.sinh(R) * Wr * Wt, kth

def Bk(R, W, k):
    from mpmath import mp, legenp, cosh, mpf, mpc
    with mp.workdps(20):
        Pk = np.array([complex(legenp(mpc(-0.5, 0) + 1j * k, 0, cosh(mpf(float(r))), type=3)) for r in R])
    return complex(W @ Pk)

def winding(f, corners, npts=40):
    """(1/2pi) total change of arg f along the closed polygon through `corners` (counter-clockwise)."""
    tot = 0.0; prev = None; first = None
    for a, b in zip(corners, corners[1:] + corners[:1]):
        for s in np.linspace(0, 1, npts, endpoint=False):
            z = a + (b - a) * s; v = f(z)
            if prev is not None: tot += np.angle(v / prev)
            else: first = v
            prev = v
    tot += np.angle(first / prev)
    return tot / (2 * np.pi)
