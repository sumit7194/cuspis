"""EXP-041 addendum A: the E5 check of the EMI second-order step at d = 4 and 5 (registration in report.md)."""
import mpmath as mp
mp.mp.dps = 30
def g(n, r):                      # angular average of cos(u_1) over S^(n-1), n = d - 2
    return mp.gamma(mp.mpf(n) / 2) * (2 / r) ** (mp.mpf(n) / 2 - 1) * mp.besselj(mp.mpf(n) / 2 - 1, r)
def AB(d, dl):
    n = d - 2; Om = 2 * mp.pi ** (mp.mpf(n) / 2) / mp.gamma(mp.mpf(n) / 2)
    fA = lambda r: r ** (n - 1) * (g(n, r) / (2 * r ** (2 * (d - 2))) - (d - 2) * (1 - g(n, r)) / r ** (2 * (d - 1)))
    fB = lambda r: r ** (n - 1) * (d - 1) * (d - 2) * (1 - g(n, r)) / r ** (2 * (d - 1))
    I = lambda f: mp.quad(f, [dl, 1, 10]) + mp.quadosc(f, [10, mp.inf], omega=1)
    return Om * I(fA), Om * I(fB)
dls = [mp.mpf(1) / 2 ** k for k in range(5, 14)]
for d, basis, key in ((4, lambda x: [x**-4, x**-2, mp.log(x), 1, x**2, x**2*mp.log(x), x**4, x**4*mp.log(x), x**6], 2),
                      (5, lambda x: [x**-5, x**-3, x**-1, 1, x, x**2, x**3, x**4, x**5], 3)):
    rows = [AB(d, x) for x in dls]
    M = mp.matrix([basis(x) for x in dls])
    sD = mp.lu_solve(M, mp.matrix([a - b for a, b in rows])); sB = mp.lu_solve(M, mp.matrix([b for a, b in rows]))
    lab = "log(delta)" if d == 4 else "delta^0"
    print(f"d={d}: {lab} coefficient of A - B = {mp.nstr(sD[key], 6)}  -> {'PASS' if abs(sD[key]) < 1e-8 else 'FAIL'};  "
          f"{lab} coefficient of B alone = {mp.nstr(sB[key], 12)}" + (f";  delta^0 of A - B (local, reported only) = {mp.nstr(sD[3], 6)}" if d == 4 else ""))
