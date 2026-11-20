"""EXP-053 (pre-registered in report.md, aa0eb4b): large-N cone gap equation from our own mode sum.
E(n, alpha) = pi F(n) - (1/n) sum_{m in Z} [psi(nu_m + 1/2) - psi(|m|/n + 1/2)] = 0,
nu_m = sqrt(m^2/n^2 + alpha^2) (m != 0), nu_0 = alpha (alternate branch; 'regular' must-fail uses +|alpha|).
F(n) = 4 pi r (G_n - G_1) (EXP-052).   [model: Opus 5.5]"""
from mpmath import mp, mpf, quad, coth, sinh, pi, psi, sqrt, findroot, nsum, inf, sin

mp.dps = 30

def F(n):
    n = mpf(n)
    def f(t):
        return ((1 / n) * coth(t / (2 * n)) - coth(t / 2)) / (2 * sinh(t / 2))
    t0 = mpf('1e-3')
    # small-t series of the bracket: t(1/n^2-1)/6 - t^3(1/n^4-1)/360 + 2 t^5 (1/n^6-1)/(945*32); 1/(2 sinh(t/2)) = 1/t - t/24 + 7t^3/5760
    def fs(t):
        br = t * (1 / n**2 - 1) / 6 - t**3 * (1 / n**4 - 1) / 360 + t**5 * (1 / n**6 - 1) / 15120
        return br * (1 / t - t / 24 + 7 * t**3 / 5760)
    with mp.workdps(60):
        return (quad(fs, [0, t0]) + quad(f, [t0, mpf('0.1'), 1, 10, 100])) / pi

def msum(n, a2, M=None):
    n = mpf(n)
    T = lambda m: psi(0, sqrt(m**2 / n**2 + a2) + mpf(1) / 2) - psi(0, m / n + mpf(1) / 2)
    if M is None:
        return 2 * nsum(T, [1, inf])
    s = 2 * sum(T(mpf(m)) for m in range(1, M + 1))
    # tail: T_m ~ a2 n^2/(2 m^2) to leading order -> 2 * a2 n^2/2 * (1/M - 1/(2M^2) + 1/(6M^3))  (Euler-Maclaurin of sum_{m>M} 1/m^2)
    tail = a2 * n**2 * (mpf(1) / M - mpf(1) / (2 * M**2) + mpf(1) / (6 * M**3))
    return s + tail

def E(n, alpha, branch="alt", drop_m=False, M=None, Fn=None):
    n = mpf(n); Fn = F(n) if Fn is None else Fn
    nu0 = alpha if branch == "alt" else abs(alpha)
    m0 = psi(0, nu0 + mpf(1) / 2) - psi(0, mpf(1) / 2)
    rest = 0 if drop_m else msum(n, alpha**2, M)
    return pi * Fn - (m0 + rest) / n

def root(n, **kw):
    Fn = F(n)
    return findroot(lambda a: E(n, a, Fn=Fn, **kw), -0.1 * (n - 1) / (n) - 0.05 if n > 1.5 else -(mpf(n) - 1) / 4)

if __name__ == "__main__":
    print("controls F: n=1/2", F(mpf(1) / 2), "(1/2);  n=1/4", F(mpf(1) / 4), "(", sqrt(2) + mpf(1) / 2, ");  n=1/3", F(mpf(1) / 3), "(", 1 / sin(pi / 3), ")")
    for M in (200, 400, 800, None):
        a2 = root(2, M=M); print(f"P1 alpha_2 (M={M}): {a2}")
    a2 = root(2)
    print(f"P1: alpha_2 = {a2}  vs MFS09 -0.16515 +- 5e-5: diff {a2 + mpf('0.16515')}  [{'PASS' if abs(a2 + mpf('0.16515')) <= 5e-5 else 'FAIL'}]")
    a = root(mpf('1.01')); r = a / mpf('0.01')
    print(f"P2: alpha(1.01)/0.01 = {r}  [{'PASS' if abs(r + mpf(1)/4) <= 0.01 else 'FAIL'}]  (Neon: -0.248317)")
    for n, ref in ((3, '-0.26594'), (4, '-0.32905'), (5, '-0.36743')):
        an = root(n); print(f"P3: alpha_{n} = {an} vs {ref}: diff {an - mpf(ref)}  [{'within' if abs(an - mpf(ref)) <= 5e-5 else 'outside'} 5e-5]; 2 alpha > -1: {2*an > -1}")
    F2 = F(2)
    import mpmath
    grid = [mpf(-0.49) + mpf(0.98) * i / 98 for i in range(99)]
    vals = [E(2, x, branch="reg", Fn=F2) for x in grid]
    sc = sum(1 for u, v in zip(vals, vals[1:]) if u * v < 0)
    print(f"must-fail (regular branch nu0=+|alpha|): sign changes of E(2,.) on (-0.49,0.49): {sc}; max E = {max(vals)}  [{'PASS (no root)' if sc == 0 else 'FAIL (root exists)'}]")
    ad = findroot(lambda x: E(2, x, drop_m=True, Fn=F2), -0.2)
    print(f"sensitivity (drop m != 0): alpha_2 -> {ad}, shift {ad - a2}  [{'PASS (> tol)' if abs(ad - a2) > 5e-5 else 'FAIL'}]")
