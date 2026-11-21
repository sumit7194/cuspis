"""EXP-061 pre-check 6: the twisted on-shell total by an independent route. tau-space Sigma_tw integrated against
P_{a-1/2} in x = c - 1 with ONE finite part: subtract S(x) = -(2/(3pi^2)) x^-2 + 2pi c_a (2x)^{-3/2} on (0,1],
add back f.p. Int_0^1 S = 2/(3pi^2) - 4pi c_a 2^{-3/2}. Target (same c-1 scheme): [1 + 4a^2 - 24a(1-a)]/(12 pi^2).
Run 1 (kept: _run1_nan) gave NaN: 2cosh t - 2cosh rho cancels to 0 in double at tiny rho; here the exact product
form 4 sinh((t+rho)/2) sinh((t-rho)/2) and rho = 2 asinh(sqrt(x/2)) are used, and tau breakpoints are clipped.
x_min in {1e-6, 1e-8} shares all panels above 1e-6. [model: Opus 5.5]"""
import sys, os, time
import numpy as np
from scipy.integrate import quad
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, legenp, re
from exp061_precheck_onshell_tw import S as Spsi

def Gtw(a, rho, tau):
    def f(u, part):
        t = rho + u * u; z1 = t - 1j * tau; z2 = t + 1j * tau
        den = np.sqrt(4 * np.sinh(rho + u * u / 2) * np.sinh(u * u / 2)) if u > 0 else 1.0
        num = (np.exp(-a * z1) / (-np.expm1(-z1)) + np.exp(-(1 - a) * z2) / (-np.expm1(-z2)))
        v = num * 2 * u / den if u > 0 else num * 2 / np.sqrt(2 * np.sinh(rho))
        return v.real if part == 0 else v.imag
    return (quad(f, 0, 12, args=(0,), limit=400, epsabs=1e-15, epsrel=1e-12)[0]
            + 1j * quad(f, 0, 12, args=(1,), limit=400, epsabs=1e-15, epsrel=1e-12)[0]) / (4 * np.pi ** 2)

def sig_tau(a, rho):
    c = np.cosh(rho); cm = 2 * np.sinh(rho / 2) ** 2      # c - 1 without cancellation
    def h(tau, part):
        den = (cm + 2 * np.sin(tau / 2) ** 2) ** 2           # (c - cos tau)^2
        v = np.exp(-1j * a * tau) * (-1 / (np.pi ** 2 * den)) * Gtw(a, rho, tau)
        return v.real if part == 0 else v.imag
    pts = sorted({p for p in (rho, 3 * rho, np.pi, 2 * np.pi - 3 * rho, 2 * np.pi - rho) if 0 < p < 2 * np.pi})
    return quad(h, 0, 2 * np.pi, args=(0,), points=pts, limit=400, epsabs=0, epsrel=1e-11)[0]

def total(a, nper=12):
    ca = float(Spsi(mpf(a))) / (2 * np.pi ** 3)
    xs, ws = np.polynomial.legendre.leggauss(nper)
    def F(x):
        rho = 2 * np.arcsinh(np.sqrt(x / 2)); P = float(re(legenp(mpf(a) - mpf(0.5), 0, 1 + mpf(x), type=3)))
        return 2 * np.pi * P * sig_tau(a, rho)
    Sx = lambda x: -(2 / (3 * np.pi ** 2)) / x ** 2 + 2 * np.pi * ca * (2 * x) ** -1.5
    low = 0.0; high = 0.0
    ue = np.geomspace(1e-4, 1.0, 9)                      # u = sqrt(x); panels below u = 1e-3 are the x in [1e-8, 1e-6] part
    for lo, hi in zip(ue[:-1], ue[1:]):
        u = 0.5 * (hi - lo) * xs + 0.5 * (hi + lo); w = 0.5 * (hi - lo) * ws
        part = sum(wi * 2 * ui * (F(ui * ui) - Sx(ui * ui)) for ui, wi in zip(u, w))
        if hi <= 1e-3 + 1e-15: low += part
        else: high += part
    xe = np.geomspace(1.0, 3e4, 10)
    for lo, hi in zip(xe[:-1], xe[1:]):
        x = 0.5 * (hi - lo) * xs + 0.5 * (hi + lo); w = 0.5 * (hi - lo) * ws
        high += sum(wi * F(xi) for xi, wi in zip(x, w))
    add = 2 / (3 * np.pi ** 2) - 4 * np.pi * ca * 2 ** -1.5
    return high + add, high + low + add

if __name__ == "__main__":
    alist = [float(v) for v in sys.argv[1:]] or [0.2, 0.5, 0.8]
    for a in alist:
        t0 = time.time(); v6, v8 = total(a)
        target = (1 + 4 * a * a - 24 * a * (1 - a)) / (12 * np.pi ** 2)
        print(f"a={a}: direct f.p. at x_min=1e-6, 1e-8: {v6:+.9f}, {v8:+.9f}   target {target:+.9f}  diff {v8-target:+.1e}  "
              f"(Legendre-only would be {(1+8*a-4*a*a)/(12*np.pi**2):+.9f})  [{time.time()-t0:.0f}s]", flush=True)
