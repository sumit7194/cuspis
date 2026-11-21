"""EXP-061 pre-check 2 (characterisation, unregistered): two continuations of the n = 1 phi self-energy to
non-integer external frequency w.
  Legendre/Laplace: Sigma_w(rho) = -(2/(3 pi^3)) d^2/dc^2 Q_{|w|-1/2}(c), c = cosh rho
                    [from (c - cos tau)^{-5/2} = (4/3) d_c^2 (c - cos tau)^{-1/2} and Heine's series]
  frequency sum (twisted phi, sigma untwisted): (1/2pi) sum_q D_q(rho) g_{|w-q|}(rho)
Checks: agreement at integer w (also vs the direct tau-integral); difference at non-integer w; small-rho scaling
of the difference. [model: Opus 5.5]"""
import sys, os
D0 = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D0)
from mpmath import mp, mpf, quad, exp, cosh, legenq, re, pi, diff, cos, sqrt
from exp059_stageA import Dpos
mp.dps = 25
def Q(nu, c): return re(legenq(nu, 0, c, type=3))
def g(w, r): return Q(abs(w) - mpf(0.5), cosh(r)) / (2 * pi)
def sig_leg(w, r): return -(2 / (3 * pi**3)) * diff(lambda c: Q(abs(w) - mpf(0.5), c), cosh(r), 2)
def sig_sum(w, r, Qmax=60): return sum(Dpos(abs(q), r) * g(w - q, r) for q in range(-Qmax, Qmax + 1)) / (2 * pi)
def sig_tau(m, r):
    c = cosh(r); return re(quad(lambda t: exp(-1j*m*t) * (-1/(4*sqrt(2)*pi**3)) * (c - cos(t))**(-2.5), [0, pi, 2*pi]))
if __name__ == "__main__":
    for r in (mpf('0.7'), mpf('1.5')):
        for w in (0, 1, mpf('0.35'), mpf('0.8')):
            a, b = sig_leg(w, r), sig_sum(w, r)
            ex = f"  tau-integral {mp.nstr(sig_tau(int(w), r),12)}" if w in (0, 1) else ""
            print(f"rho={r} w={w}: Legendre {mp.nstr(a,12)}  freq-sum {mp.nstr(b,12)}  rel {mp.nstr(b/a-1,3)}{ex}", flush=True)
    for w in (mpf('0.35'), mpf('0.5')):
        for r in (mpf('0.3'), mpf('0.1'), mpf('0.03'), mpf('0.01')):
            a = sig_leg(w, r); b = sig_sum(w, r, Qmax=int(60/float(r)) if r < 0.3 else 60)
            print(f"w={w} rho={r}: Delta = sum - Legendre = {mp.nstr(b-a,10)};  rho^3*Delta = {mp.nstr((b-a)*r**3,8)}  (Legendre {mp.nstr(a,6)})", flush=True)
