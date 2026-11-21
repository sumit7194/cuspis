"""EXP-077 planted control for the Newton+Levin extrapolator (Bridge's request): synthetic Q(n) = B n + R(n), R completely
monotone (positive mixtures of rho^(n-1), plus a power-corrected case), shaped like the honest P4' data (R(1) ~ 0.2986,
second-difference ratios ~0.02 -> ~0.012), known exact Q'(1). Same pipeline as exp077_newton_hp: 45 dps, Newton forward-
difference derivative series, Levin-u on partial sums starting at j = 1, K = 40 and 59. [model: Opus 5.5]"""
import mpmath as mp
mp.mp.dps = 45
B = mp.mpf("-0.29855273")
cases = {
 "single rho=0.0206":      ([mp.mpf("0.2986")], [mp.mpf("0.0206")]),
 "mixture 0.012..0.05":    ([mp.mpf("0.20"), mp.mpf("0.08"), mp.mpf("0.0186")], [mp.mpf("0.012"), mp.mpf("0.025"), mp.mpf("0.05")]),
 "mixture 0.008..0.04":    ([mp.mpf("0.15"), mp.mpf("0.10"), mp.mpf("0.0486")], [mp.mpf("0.008"), mp.mpf("0.02"), mp.mpf("0.04")]),
}
def pipeline(Qs, K):
    D = list(Qs); a = [Qs[0]]
    for k in range(1, len(Qs)):
        D = [D[i + 1] - D[i] for i in range(len(D) - 1)]; a.append(D[0])
    t = [(-1) ** (k + 1) * a[k] / k for k in range(1, K + 1)]
    S = [mp.fsum(t[:j]) for j in range(1, K + 1)]
    return S[-1], mp.levin(method="levin", variant="u").update_psum(S)[0], all(x < 0 for x in t)
for name, (cs, rs) in cases.items():
    R = lambda n: mp.fsum(c * r ** (n - 1) for c, r in zip(cs, rs))
    Qs = [B * n + R(n) - (B + R(1)) for n in range(1, 61)]          # shift so Q(1) = 0 like the honest data
    exact = B + mp.fsum(c * mp.log(r) for c, r in zip(cs, rs))
    for K in (40, 59):
        raw, lev, neg = pipeline(Qs, K)
        print(f"{name:22s} K={K}: raw {mp.nstr(raw, 9)}  Levin {mp.nstr(lev, 12)}  exact {mp.nstr(exact, 12)}  Levin-exact {mp.nstr(lev - exact, 3)}  all terms<0 {neg}", flush=True)
# power-corrected: R(n) = c rho^(n-1) n^-2  (ratio drifts like the data)
c, r, p = mp.mpf("0.2986"), mp.mpf("0.012"), 2
Rp = lambda n: c * r ** (n - 1) * mp.mpf(n) ** (-p)
Qs = [B * n + Rp(n) - (B + Rp(1)) for n in range(1, 61)]
exact = B + mp.diff(Rp, 1)
for K in (40, 59):
    raw, lev, neg = pipeline(Qs, K)
    print(f"{'power-corrected n^-2':22s} K={K}: raw {mp.nstr(raw, 9)}  Levin {mp.nstr(lev, 12)}  exact {mp.nstr(exact, 12)}  Levin-exact {mp.nstr(lev - exact, 3)}  all terms<0 {neg}", flush=True)
