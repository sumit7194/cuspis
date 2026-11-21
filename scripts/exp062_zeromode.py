"""EXP-062 pre-check 4: piece (III), zero mode, with the corrected normalisation Z_n = g_{a_n} - g_0 ~ -(n-1) gdot/4:
(III)(a) = -(1/(8 pi)) f.p. Int 2pi sinh(rho) P_{a-1/2}(cosh rho) D_1(a; rho) gdot(rho) d rho,
D_1(a; rho) = -(2/pi) e^{-a rho}(a sinh rho + cosh rho)/sinh^3 rho (EXP-059 A4, continued frequency),
gdot(rho) = (1/2pi) Int_rho^inf (-t) dt / sqrt(2cosh t - 2cosh rho)   (d/dnu of Q's Laplace form at nu = 0).
Near 0 the integrand is pi/rho^2 (gdot(0) = -pi/4): f.p. = lim [I(rho0) - pi/rho0]; rho0 swept. Works at complex a.
[model: Opus 5.5]"""
from mpmath import mp, mpf, mpc, quad, exp, sinh, cosh, legenp, sqrt, pi, inf
mp.dps = 20
def gdot(r):
    r = mpf(r)
    f = lambda u: -(r + u * u) * 2 * u / sqrt(4 * sinh(r + u * u / 2) * sinh(u * u / 2)) if u > 0 else -r * 2 / sqrt(2 * sinh(r))
    return quad(f, [0, 0.5, 2, 6, 14]) / (2 * pi)
def D1(a, r): return -(2 / pi) * exp(-a * r) * (a * sinh(r) + cosh(r)) / sinh(r) ** 3
def piece3(a, rho0s=(mpf('1e-2'), mpf('1e-3'), mpf('1e-4'))):
    a = mpc(a); a = a.real if a.imag == 0 else a; F = lambda r: 2 * pi * sinh(r) * legenp(a - 0.5, 0, cosh(r), type=3) * D1(a, r) * gdot(r)
    tail = quad(F, [1, 4, 10, 25, 45])
    out = {}
    for r0 in rho0s:
        out[float(r0)] = -(quad(F, [r0, r0 * 10, 0.1, 1]) + tail - pi / r0) / (8 * pi)
    return out
if __name__ == "__main__":
    print("gdot(1e-6) =", mp.nstr(gdot(mpf('1e-6')), 12), "  -pi/4 =", mp.nstr(-pi/4, 12))
    for a in (mpf('0.35'), mpf('0.5'), mpc('0.5', '1'), mpc('0.5', '2'), mpc('0.5', '4')):
        o = piece3(a)
        print(f"a={mp.nstr(a,4)}: (III) at rho0=1e-2,1e-3,1e-4: " + ", ".join(mp.nstr(v, 10) for v in o.values()), flush=True)
