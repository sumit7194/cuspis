"""EXP-062 pre-check 2: analytic coincident shift of the twisted propagator on S^1_{2 pi n} (H^2 frame),
dG(n, a) = (1/4pi^2) Int_0^inf [h_n(t) - coth(t/2)] / (2 sinh(t/2)) dt,  h_n = (1/n)[e^{-a t} + e^{-(1/n - a)t}]/(1 - e^{-t/n}).
Checks: n = 1 gives -S(a)/(4 pi^2) (pre-check 2 of EXP-061); a = 0 gives EXP-052's cone shift. Then the rho^-3
coefficient of d_n R predicted as A = -(2/pi) d_n dG |_{n=1}, compared with rho^3 d_n R at small rho (pre-check 1). [model: Opus 5.5]"""
import sys, os
from mpmath import mp, mpf, quad, exp, sinh, coth, inf, pi, diff, psi, nsum
mp.dps = 25
def h(t, n, a): return (exp(-a * t) + exp(-(1 / n - a) * t)) / (n * (-mp.expm1(-t / n)))
def _ig(t, n, a):
    extra = int(mp.ceil(2 * max(0, -mp.log10(t)))) + 15          # run 1 lost digits to h - coth cancellation near t = 0
    with mp.workdps(mp.dps + extra):
        t = mp.mpf(t); v = (h(t, mp.mpf(n), mp.mpc(a) if isinstance(a, (complex, mp.mpc)) else mp.mpf(a)) - coth(t / 2)) / (2 * sinh(t / 2))
    return +v
def dG(n, a):
    return quad(lambda t: _ig(t, n, a), [0, 1, 5, 20, inf]) / (4 * pi ** 2)
def S(a): return psi(0, a + 0.5) - psi(0, mpf(0.5)) + nsum(lambda q: psi(0, q - a + 0.5) + psi(0, q + a + 0.5) - 2 * psi(0, q + 0.5), [1, inf])
if __name__ == "__main__":
    for a in (mpf('0.35'), mpf('0.5')):
        print(f"n=1 a={a}: dG {mp.nstr(dG(1, a), 15)}   -S/(4pi^2) {mp.nstr(-S(a)/(4*pi**2), 15)}")
    n = mpf('1.3')
    def _cg(t):
        with mp.workdps(mp.dps + int(mp.ceil(2*max(0,-mp.log10(t))))+15):
            t = mp.mpf(t); v = ((1/n)*coth(t/(2*n)) - coth(t/2)) / (2*sinh(t/2))
        return +v
    cone = quad(_cg, [0, 1, 5, 20, inf]) / (4*pi**2)
    print(f"a=0 n=1.3: dG {mp.nstr(dG(n, 0), 15)}   EXP-052 cone integral/(4 pi^2) {mp.nstr(cone, 15)}")
    for a in (mpf('0.35'), mpf('0.5'), mpf('0.2')):
        A = -(2 / pi) * (dG(1 + mpf('1e-6'), a) - dG(1 - mpf('1e-6'), a)) / mpf('2e-6')
        print(f"a={a}: predicted rho^3 coefficient A = {mp.nstr(A, 12)}")
