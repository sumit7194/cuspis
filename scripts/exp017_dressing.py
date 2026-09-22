"""EXP-017: the rectangle bootstrap of [LMW26] is closed under Casimir dressing.
Claim: if D(y) = D(1/y) and A(y) = y^(-2G) e^(-e0 y) D(y) is completely monotone (Laplace transform of S >= 0), then
D_E(y) = D(y) exp(E (y + 1/y)), E >= 0, satisfies both with the same corner dimension G and Casimir energy e0 + E.
Proof: A_E = A exp(E/y); exp(E/y) is completely monotone; a product of completely monotone functions is completely
monotone (Bernstein), i.e. S_E = S * (delta + sum_k E^k eps^(k-1)/(k!(k-1)!)) >= 0.
Check on the 2d-BCFT extremal solution D = y^(2G) eta(iy)^(8G), G = -c/16, e0 = pi c/24, with a control that must
fail (A*(1+y), not completely monotone). Light by design: truncated product, derivatives to order 6. Runtime < 1 s."""
import mpmath as mp
mp.mp.dps = 120   # at y = 30 the undressed A equals 1 to ~80 digits; its derivatives need > 80 digits to resolve
c = mp.mpf(1); G = -c/16; e0 = mp.pi*c/24
eta = lambda y: mp.exp(-mp.pi*y/12)*mp.fprod(1 - mp.exp(-2*mp.pi*k*y) for k in range(1, 200))
D = lambda y: y**(2*G)*eta(y)**(8*G)
def A(y, E, bad=False):
    v = y**(-2*G)*mp.exp(-(e0+E)*y)*D(y)*mp.exp(E*(y+1/y))
    return v*(1+y) if bad else v
for E in (0, 1, 5):
    DE = lambda y: D(y)*mp.exp(E*(y+1/y))
    sym = max(abs(DE(y)/DE(1/y)-1) for y in (mp.mpf('0.3'), mp.mpf('0.7'), mp.mpf('2.1')))
    res = [all((-1)**k*mp.diff(lambda t: A(t, E, bad), y, k) >= 0 for y in (mp.mpf('0.5'), 1, 2, 10, 30) for k in range(0, 7)) for bad in (False, True)]
    print(f"E = {E}: modular symmetry max dev {float(sym):.1e};  (-1)^k A^(k) >= 0, k <= 6, y = 0.5,1,2,10,30: {res[0]};  CONTROL A*(1+y) (must be False): {res[1]}")
# Note (EXP-017): with test points only up to y = 2 the control did NOT fire at E = 5, because (1+y) e^(E/y) mimics a
# completely monotone function for y << E; the points y = 10, 30 were added so the control can fail at every E tested.
# Note 2 (EXP-017): at dps = 20 the POSITIVE check failed at E = 0 once y = 30 was added. Cause: the undressed A is 1 + O(1e-80)
# there, so finite-difference derivatives were roundoff. The check was wrong, not the mathematics; dps raised to 120.
