"""Sealed-derivation check (a): E1 (1/n) sum_k f(k/n) = A + 2 Br r^(n-1)/(1-r^n) at integer n, r in {1e-2,1e-6,1e-12,1e-20},
direct alpha-sums at 50 digits; plus E2 vs a 50-digit central difference of the E1 continuation."""
import mpmath as mp; mp.mp.dps = 50
for r in (mp.mpf('1e-2'), mp.mpf('1e-6'), mp.mpf('1e-12'), mp.mpf('1e-20')):
    sq = (1 + r) / (2 * (1 - r)); lam = sq ** 2                  # from r = (2 sq - 1)/(2 sq + 1)
    A = 2 / (sq * (2 * sq + 1)); Br = -2 / (sq * (2 * sq + 1) ** 2)
    f = lambda a: 1 / (lam - (mp.mpc(0, 0.5) / mp.tan(mp.pi * a)) ** 2) if a != 0 else mp.mpf(0)
    worst = 0
    for n in range(1, 7):
        direct = sum(f(mp.mpf(k) / n) for k in range(n)) / n; E1 = A + 2 * Br * r ** (n - 1) / (1 - r ** n)
        worst = max(worst, abs(direct - E1))
    I = lambda n: A + 2 * Br * r ** (n - 1) / (1 - r ** n); h = mp.mpf('1e-20')
    E2 = 2 * Br * mp.log(r) / (1 - r) ** 2; fd = (I(1 + h) - I(1 - h)) / (2 * h)
    print(f"r={mp.nstr(r,3)}: lambda-1/4={mp.nstr(lam-0.25,4)}, A={mp.nstr(A,6)}, Br={mp.nstr(Br,6)}: max|direct-E1| over n=1..6 = {mp.nstr(worst,3)}; E2 = {mp.nstr(E2,8)} vs FD {mp.nstr(fd,8)}")
