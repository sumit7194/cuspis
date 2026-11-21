"""EXP-061 pre-check 5 (second implementation of the twisted self-energy component): tau-space route.
G_tw(rho,tau) = (1/4pi^2) Int_rho^inf dt [e^{-a(t-i tau)}/(1-e^{-(t-i tau)}) + e^{-(1-a)(t+i tau)}/(1-e^{-(t+i tau)})]/sqrt(2cosh t - 2cosh rho)
(geometric sums inside Q's Laplace form); Sigma_tw,a(rho) = Int_0^{2pi} dtau e^{-i a tau} D(rho,tau) G_tw(rho,tau),
D = -1/(pi^2 (cosh rho - cos tau)^2). Compared with the frequency-sum route (exp061_precheck_onshell_tw.sig_tw).
Control: a = 0 must give the untwisted G = 1/(4 pi sqrt(2(cosh rho - cos tau))). [model: Opus 5.5]"""
import sys, os
import numpy as np
from scipy.integrate import quad
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exp061_precheck_onshell_tw import sig_tw

def Gtw(a, rho, tau):
    def f(u, part):   # t = rho + u^2
        t = rho + u * u; z1 = t - 1j * tau; z2 = t + 1j * tau
        v = (np.exp(-a * z1) / (-np.expm1(-z1)) + np.exp(-(1 - a) * z2) / (-np.expm1(-z2))) * 2 * u / np.sqrt(2 * np.cosh(t) - 2 * np.cosh(rho))
        return v.real if part == 0 else v.imag
    re_ = quad(f, 0, 12, args=(0,), limit=400, epsabs=1e-14, epsrel=1e-12)[0]
    im_ = quad(f, 0, 12, args=(1,), limit=400, epsabs=1e-14, epsrel=1e-12)[0]
    return (re_ + 1j * im_) / (4 * np.pi ** 2)

def sig_tau(a, rho):
    c = np.cosh(rho)
    h = lambda tau, part: ((np.exp(-1j * a * tau) * (-1 / (np.pi ** 2 * (c - np.cos(tau)) ** 2)) * Gtw(a, rho, tau)).real if part == 0
                           else (np.exp(-1j * a * tau) * (-1 / (np.pi ** 2 * (c - np.cos(tau)) ** 2)) * Gtw(a, rho, tau)).imag)
    pts = [rho, 3 * rho, np.pi, 2 * np.pi - 3 * rho, 2 * np.pi - rho]
    r = quad(h, 0, 2 * np.pi, args=(0,), points=pts, limit=400, epsabs=1e-13, epsrel=1e-11)[0]
    i = quad(h, 0, 2 * np.pi, args=(1,), points=pts, limit=400, epsabs=1e-13, epsrel=1e-11)[0]
    return r + 1j * i

if __name__ == "__main__":
    for rho, tau in ((0.5, 0.3), (1.2, 2.0)):
        print(f"control a=0 rho={rho} tau={tau}: G_tw {Gtw(0.0, rho, tau).real:.12e}  closed {1/(4*np.pi*np.sqrt(2*(np.cosh(rho)-np.cos(tau)))):.12e}", flush=True)
    for a in (0.35, 0.5):
        for rho in (0.1, 0.5, 1.5):
            s1 = sig_tau(a, rho); s2 = sig_tw(a, np.array([rho]))[0]
            print(f"a={a} rho={rho}: tau-space {s1.real:+.12e} (Im {s1.imag:+.1e})  freq-sum {s2:+.12e}  rel {s1.real/s2-1:+.1e}", flush=True)
