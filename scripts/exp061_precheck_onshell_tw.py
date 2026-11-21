"""EXP-061 pre-check 4 (characterisation): on-shell value of the n = 1 self-energy in the TWISTED (frequency-sum)
continuation, Sigma~_tw(i a, a) = Sigma~_Leg(i a, a) + f.p. Int 2 pi sinh(rho) P_{a-1/2}(cosh rho) Delta_a(rho) d rho,
Delta = twisted - Legendre ~ c_a/rho^3 + O(1/rho), c_a = S(a)/(2 pi^3) (pre-check 2, verified). The f.p. is
lim_{rho0 -> 0} [ I(rho0) - 2 pi c_a / rho0 ]; rho0 swept. Sigma~_Leg on-shell = (1 + 8a - 4a^2)/(12 pi^2) in the
c-1 finite-part scheme (pre-check 3, verified at unseen points); the Delta part has no log and no scheme constant.
[model: Opus 5.5]"""
import sys, os, time
import numpy as np
D0 = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D0)
from mpmath import mp, mpf, legenq, legenp, re, diff, psi, nsum, inf, pi as mpi
import exp056_sigma_kernel as K
mp.dps = 25

def Dpos_np(q, r): return -(2 / np.pi) * np.exp(-q * r) * (q * np.sinh(r) + np.cosh(r)) / np.sinh(r) ** 3
def sig_tw(a, R):
    Qmax = int(45.0 / R.min()) + 10; tot = np.zeros_like(R)
    for q in range(-Qmax, Qmax + 1):
        tot += Dpos_np(abs(q), R) * K.g(abs(a - q), R)
    return tot / (2 * np.pi)
def sig_leg(a, r):
    nu = mpf(a) - mpf(0.5)
    with mp.workdps(40):
        v = -(2 / (3 * mpi ** 3)) * diff(lambda c: re(legenq(nu, 0, c, type=3)), mp.cosh(mpf(r)), 2)
    return float(v)
def Pleg(a, r): return float(re(legenp(mpf(a) - mpf(0.5), 0, mp.cosh(mpf(r)), type=3)))
def S(a): return psi(0, a + 0.5) - psi(0, mpf(0.5)) + nsum(lambda q: psi(0, q - a + 0.5) + psi(0, q + a + 0.5) - 2 * psi(0, q + 0.5), [1, inf])

def onshell(a, rho0s=(0.04, 0.02, 0.01), rmax=22.0, nlog=48, nlin=160):
    c = float(S(mpf(a)) / (2 * mpi ** 3)); out = []
    xg, wg = np.polynomial.legendre.leggauss(nlog)
    for rho0 in rho0s:
        # [rho0, 1]: Gauss-Legendre in log rho; [1, rmax]: composite Gauss-Legendre in rho
        L0, L1 = np.log(rho0), 0.0
        t = 0.5 * (L1 - L0) * xg + 0.5 * (L1 + L0); R1 = np.exp(t); W1 = 0.5 * (L1 - L0) * wg * R1
        edges = np.linspace(1.0, rmax, 22); xs, ws = np.polynomial.legendre.leggauss(nlin // 20)
        R2 = np.concatenate([0.5 * (b - e) * xs + 0.5 * (b + e) for e, b in zip(edges[:-1], edges[1:])])
        W2 = np.concatenate([0.5 * (b - e) * ws for e, b in zip(edges[:-1], edges[1:])])
        R = np.concatenate([R1, R2]); W = np.concatenate([W1, W2])
        tw = sig_tw(a, R); lg = np.array([sig_leg(a, r) for r in R]); Pv = np.array([Pleg(a, r) for r in R])
        I = np.sum(W * 2 * np.pi * np.sinh(R) * Pv * (tw - lg))
        out.append((rho0, I - 2 * np.pi * c / rho0))
    return c, out

if __name__ == "__main__":
    # internal two-implementation check of the twisted sum (numpy spectral g vs mpmath Legendre Q)
    from exp061_precheck_sigma1 import sig_sum
    for a, r in ((0.35, 0.7), (0.5, 0.1)):
        v_np = sig_tw(a, np.array([r]))[0]; v_mp = float(sig_sum(mpf(a), mpf(r), Qmax=int(60 / r)))
        print(f"twisted sum a={a} rho={r}: numpy {v_np:.12e}  mpmath {v_mp:.12e}  rel {v_np/v_mp-1:.1e}", flush=True)
    for a in (0.2, 0.35, 0.5, 0.65, 0.8):
        t0 = time.time(); c, res = onshell(a)
        leg = (1 + 8 * a - 4 * a * a) / (12 * np.pi ** 2)
        fpD = res[-1][1]
        print(f"a={a}: c_a={c:.9f}; f.p. of Delta part at rho0=" + ", ".join(f"{r0}: {v:+.9f}" for r0, v in res)
              + f"  | Sigma~_Leg on-shell {leg:+.9f}  => Sigma~_tw on-shell {leg + fpD:+.9f}  [{time.time()-t0:.0f}s]", flush=True)
