"""EXP-061 pre-check 7 (stage C for the n = 1 factor): the twisted Delta-part on the CH07b line a = 1/2 + iy.
Analyticity in a plus the real-a closed form (pre-check 4, verified) predicts f.p.[Delta] = -8a(1-a)/(3pi^2)
= -8(1/4 + y^2)/(3 pi^2): real, polynomial growth. Computed directly with the tau-space kernel at complex a
(analytic in a) minus the Legendre form at complex degree, finite part in rho with c_a = S(a)/(2pi^3) at complex a.
Must-fail (pre-checked from real-a data): omitting the Delta-part, i.e. Legendre only, must miss the twisted total
by |8a(1-a)|/(3pi^2) >= 0.067. [model: Opus 5.5]"""
import sys, os, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mpmath import mp, mpf, mpc, legenq, legenp, diff, psi, nsum, inf, pi as mpi
from exp061_precheck_onshell_direct import Gtw
from scipy.integrate import quad
mp.dps = 25

def sig_tau_c(a, rho):
    cm = 2 * np.sinh(rho / 2) ** 2
    def h(tau, part):
        v = np.exp(-1j * a * tau) * (-1 / (np.pi ** 2 * (cm + 2 * np.sin(tau / 2) ** 2) ** 2)) * Gtw(a, rho, tau)
        return v.real if part == 0 else v.imag
    pts = sorted({p for p in (rho, 3 * rho, np.pi, 2 * np.pi - 3 * rho, 2 * np.pi - rho) if 0 < p < 2 * np.pi})
    return (quad(h, 0, 2 * np.pi, args=(0,), points=pts, limit=400, epsabs=0, epsrel=1e-11)[0]
            + 1j * quad(h, 0, 2 * np.pi, args=(1,), points=pts, limit=400, epsabs=1e-30, epsrel=1e-11)[0])
def sig_leg_c(a, r):
    nu = mpc(a) - mpf(0.5)
    with mp.workdps(40):
        v = -(2 / (3 * mpi ** 3)) * diff(lambda c: legenq(nu, 0, c, type=3), mp.cosh(mpf(r)), 2)
    return complex(v)
def S_c(a):
    a = mpc(a); return complex(psi(0, a + 0.5) - psi(0, mpf(0.5)) + nsum(lambda q: psi(0, q - a + 0.5) + psi(0, q + a + 0.5) - 2 * psi(0, q + 0.5), [1, inf]))

def delta_fp(a, rmax=22.0, nper=12):
    ca = S_c(a) / (2 * np.pi ** 3); xs, ws = np.polynomial.legendre.leggauss(nper)
    edges_log = [0.005, 0.01, 0.02, 0.05, 0.1, 0.25, 0.5, 1.0]
    panels = []
    for lo, hi in zip(edges_log[:-1], edges_log[1:]):
        L0, L1 = np.log(lo), np.log(hi); t = 0.5 * (L1 - L0) * xs + 0.5 * (L1 + L0)
        panels.append((lo, np.exp(t), 0.5 * (L1 - L0) * ws * np.exp(t)))
    for lo, hi in zip(np.linspace(1, rmax, 15)[:-1], np.linspace(1, rmax, 15)[1:]):
        panels.append((lo, 0.5 * (hi - lo) * xs + 0.5 * (hi + lo), 0.5 * (hi - lo) * ws))
    contrib = []
    for lo, R, W in panels:
        val = 0
        for r, w in zip(R, W):
            P = complex(legenp(mpc(a) - mpf(0.5), 0, mp.cosh(mpf(r)), type=3))
            val += w * 2 * np.pi * np.sinh(r) * P * (sig_tau_c(a, r) - sig_leg_c(a, r))
        contrib.append((lo, val))
    out = {}
    for r0 in (0.02, 0.01, 0.005):
        out[r0] = sum(v for lo, v in contrib if lo >= r0 - 1e-12) - 2 * np.pi * ca / r0
    return out

if __name__ == "__main__":
    a = 0.35; t0 = time.time(); o = delta_fp(a)          # real-a control against pre-check 4
    print(f"control a={a}: f.p.[Delta] " + ", ".join(f"{k}: {v.real:+.8f}{v.imag:+.1e}j" for k, v in o.items())
          + f"  closed {-8*a*(1-a)/(3*np.pi**2):+.8f}  [{time.time()-t0:.0f}s]", flush=True)
    for y in (0.5, 1.0, 2.0):
        a = 0.5 + 1j * y; t0 = time.time(); o = delta_fp(a); pred = -8 * a * (1 - a) / (3 * np.pi ** 2)
        print(f"a=1/2+{y}i: f.p.[Delta] " + ", ".join(f"{k}: {v.real:+.8f}{v.imag:+.1e}j" for k, v in o.items())
              + f"  predicted {pred.real:+.8f}{pred.imag:+.1e}j  [{time.time()-t0:.0f}s]", flush=True)
