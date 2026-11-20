"""EXP-052: check of an outside referee claim (Gemini 4 Neon, relayed by the Bridge, 2026-11-21; UNVERIFIED on arrival).
Claim: for a massless 3D scalar on (2D cone of angle 2 pi n) x R, the coincident propagator shift at distance r from the
edge is 4 pi r (G_n - G_1) = -(pi/8)(n-1) + (pi/6)(n-1)^2 + ...
Our route: J^2 mode sum -> Legendre Q_{nu-1/2} toroidal rep -> sum over m gives coth:
    4 pi r (G_n - G_1) = (1/pi) Int_0^inf [(1/n) coth(t/2n) - coth(t/2)] / (2 sinh(t/2)) dt.
Controls: n = 1/2 and 1/4 (method of images, exact). Closure: the alternate-branch m = 0 exponent alpha changes the
2D m = 0 partial wave by +|alpha|/(2 pi) K0 K0 (from d/dnu I_nu|_0 = -K0, checked numerically), which in 3D at
coincidence is |alpha|/(8 r) (Int_0^inf K0^2 = pi^2/4); the large-N gap equation then fixes |alpha'(1)|, to be compared
with MFS09 eq. (6.27) read at source (-1/4 in D = 3).   [model: Opus 5.5]"""
from mpmath import mp, quad, coth, sinh, csch, pi, mpf, sin, besseli, besselk, diff

mp.dps = 40

def F(n):
    f = lambda t: ((1 / n) * coth(t / (2 * n)) - coth(t / 2)) / (2 * sinh(t / 2))
    with mp.workdps(90):
        return quad(f, [mpf('1e-30'), mpf('1e-3'), mpf('0.1'), 1, 10, 90]) / pi

def coeffs():
    fu = lambda x: coth(x) - x * csch(x) ** 2                                   # d/du [u coth(u t/2)] at u = 1, x = t/2
    fuu = lambda x: x * (-2 * csch(x) ** 2 + 2 * x * csch(x) ** 2 * coth(x))    # d2/du2 at u = 1
    I = lambda g: quad(lambda t: g(t / 2) / (2 * sinh(t / 2)), [mpf('1e-30'), mpf('1e-3'), mpf('0.1'), 1, 10, 90]) / pi
    with mp.workdps(90):
        return I(lambda x: -fu(x)), I(lambda x: (fuu(x) + 2 * fu(x)) / 2)       # d/dn = -u^2 d/du

if __name__ == "__main__":
    print("control n=1/2:", F(mpf(1) / 2), " exact 1/2")
    print("control n=1/4:", F(mpf(1) / 4), " exact", (2 / sin(pi / 4) + 1) / 2)
    c1, c2 = coeffs()
    print("c1 =", c1, " claim -pi/8, diff", c1 + pi / 8)
    print("c2 =", c2, " claim +pi/6, diff", c2 - pi / 6)
    for x in (mpf('0.3'), mpf(1), mpf(4)):
        print(f"d/dnu I_nu(x)|0 + K0(x) at x={x}:", diff(lambda nu: besseli(nu, x), 0) + besselk(0, x))
    print("Int K0^2 - pi^2/4:", quad(lambda u: besselk(0, u) ** 2, [0, 1, mp.inf]) - pi ** 2 / 4)
    print("closure |alpha'(1)| = -8 c1/(4 pi) =", -8 * c1 / (4 * pi), " MFS09 (6.27), D=3: 1/4")
