"""EXP-062 pre-check 1 (stage B, piece (I)): image/Riemann piece R(n; rho) = Int_0^{2 pi n} dtau e^{-i a tau} D^(n) G_tw^(n)
with closed-form D^(n) (geometric sum of D_1's continued-frequency form on the lattice Z/n) and G_tw^(n) (twisted, step 1/n).
Gate: R(1) = Sigma_tw (pre-check 5). Then d_n R at n = 1 by central differences (step swept) and its small-rho form.
[model: Opus 5.5]"""
import sys, os, time
import numpy as np
from scipy.integrate import quad
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp061_precheck_onshell_direct import sig_tau as sig_tw_n1

def Dn(rho, tau, n):
    ch, sh = np.cosh(rho / n), np.sinh(rho / n); ct = np.cos(tau / n)
    den = ch - ct
    if den < 1e-300: return -np.inf
    K = sh / den; dK = (1.0 / n) * (1 - ch * ct) / den ** 2
    return -(2 / np.pi) / (2 * np.pi * n) * (-np.sinh(rho) * dK + np.cosh(rho) * K) / np.sinh(rho) ** 3

def Gtw_n(a, rho, tau, n):
    def f(u, part):
        t = rho + u * u; z1 = t - 1j * tau; z2 = t + 1j * tau
        num = np.exp(-a * z1) / (-np.expm1(-z1 / n)) + np.exp(-(1 / n - a) * z2) / (-np.expm1(-z2 / n))
        v = num * 2 * u / np.sqrt(4 * np.sinh(rho + u * u / 2) * np.sinh(u * u / 2)) if u > 0 else num * 2 / np.sqrt(2 * np.sinh(rho))
        return v.real if part == 0 else v.imag
    return (quad(f, 0, 12, args=(0,), limit=400, epsabs=1e-15, epsrel=1e-12)[0]
            + 1j * quad(f, 0, 12, args=(1,), limit=400, epsabs=1e-15, epsrel=1e-12)[0]) / (4 * np.pi ** 2 * n)

def R(a, rho, n):
    T = 2 * np.pi * n
    def h(tau, part):
        v = np.exp(-1j * a * tau) * Dn(rho, tau, n) * Gtw_n(a, rho, tau, n)
        return v.real if part == 0 else v.imag
    pts = sorted({p for p in (rho, 3 * rho, T / 2, T - 3 * rho, T - rho) if 0 < p < T})
    return (quad(h, 0, T, args=(0,), points=pts, limit=400, epsabs=0, epsrel=1e-11)[0]
            + 1j * quad(h, 0, T, args=(1,), points=pts, limit=400, epsabs=1e-30, epsrel=1e-11)[0])

if __name__ == "__main__":
    for a, rho in ((0.35, 0.5), (0.5, 1.5)):
        r1 = R(a, rho, 1.0); s = sig_tw_n1(a, rho)
        print(f"gate a={a} rho={rho}: R(1) {r1.real:+.12e} (Im {r1.imag:+.1e})  Sigma_tw {s:+.12e}  rel {r1.real/s-1:+.1e}", flush=True)
    for a in (0.35,):
        for rho in (1.0, 0.3, 0.1, 0.03):
            t0 = time.time(); d = {}
            for dl in (2e-3, 1e-3):
                d[dl] = (R(a, rho, 1 + dl) - R(a, rho, 1 - dl)) / (2 * dl)
            print(f"a={a} rho={rho}: d_nR (step 2e-3) {d[2e-3].real:+.10e}  (1e-3) {d[1e-3].real:+.10e}  Im {d[1e-3].imag:+.1e}  "
                  f"rho^3*d_nR {d[1e-3].real*rho**3:+.8e}  [{time.time()-t0:.0f}s]", flush=True)
