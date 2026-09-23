"""EXP-023 (bridge: cuboid step of the bounds chain; CF-24): is the cuboid bootstrap of [LMW26] (2609.04041, eqs. 41-46)
closed under Casimir dressing?  Constraints (read on the source): (42) D(r1,r2) = D(r2,r1) = D(1/r1, r2/r1);
(43) A(r1,r2) = (sqrt(r2)/r1)^(8G/3) exp(-(r1/sqrt(r2)) eps4(r2)) D(r1,r2) completely monotone in r1 for each r2; no r2 constraint.
Two dressings, both scale invariant (so G unchanged):
  four-body: G4 = exp[E (L1/sqrt(L2 L3) + L2/sqrt(L1 L3) + L3/sqrt(L1 L2))]        -> eps4(r2) += E; leftover exp[E (r2 + r2^(-1/2))/sqrt(r1)]
  pair:      Gp = exp[E' sum_{i != j} L_i/L_j]  (the rectangle dressing on each face)  -> eps4(r2) += E'(sqrt(r2) + 1/sqrt(r2))
Checks: (i) the symmetries (42) of both factors at random points; (ii) the leftover factor in A after the eps4 shift, at random
points, equals the claimed closed form; (iii) the leftover factor is completely monotone in r1 (derivative signs, k <= 6), with a
control that must fail.  No sympy on this machine; everything is checked numerically at 40 digits."""
import mpmath as mp, random
mp.mp.dps = 40
random.seed(1)
def G4(r1, r2, E): return mp.exp(E*(r1/mp.sqrt(r2) + r2/mp.sqrt(r1) + 1/mp.sqrt(r1*r2)))
def Gp(r1, r2, E): return mp.exp(E*(r1 + 1/r1 + r2 + 1/r2 + r1/r2 + r2/r1))
worst_sym = 0
for _ in range(200):
    r1, r2 = mp.mpf(random.uniform(0.05, 20)), mp.mpf(random.uniform(0.05, 20)); E = mp.mpf(random.uniform(0.1, 3))
    for G in (G4, Gp):
        v = G(r1, r2, E)
        worst_sym = max(worst_sym, abs(G(r2, r1, E)/v - 1), abs(G(1/r1, r2/r1, E)/v - 1))
print(f"(i)  symmetries (42) of both dressings, 200 random points: max relative deviation {float(worst_sym):.1e}")
worst_left = 0
for _ in range(200):
    r1, r2 = mp.mpf(random.uniform(0.05, 20)), mp.mpf(random.uniform(0.05, 20)); E = mp.mpf(random.uniform(0.1, 3))
    left4 = G4(r1, r2, E)*mp.exp(-(r1/mp.sqrt(r2))*E);                     claim4 = mp.exp(E*(r2 + 1/mp.sqrt(r2))/mp.sqrt(r1))   # corrected: first version had (1+r2)/sqrt(r1 r2), a hand-algebra slip caught by check (ii)
    leftp = Gp(r1, r2, E)*mp.exp(-(r1/mp.sqrt(r2))*E*(mp.sqrt(r2) + 1/mp.sqrt(r2))); claimp = mp.exp(E*((1 + r2)/r1 + r2 + 1/r2))
    worst_left = max(worst_left, abs(left4/claim4 - 1), abs(leftp/claimp - 1))
print(f"(ii) leftover factor after the eps4 shift equals the closed form, 200 random points: max relative deviation {float(worst_left):.1e}")
print("(iii) complete monotonicity in r1 of the leftover factors ((-1)^k d^k/dr1^k >= 0, k <= 6), and a control that must fail:")
for E in (mp.mpf('0.5'), mp.mpf(2)):
    for r2 in (mp.mpf('0.2'), mp.mpf(1), mp.mpf(5)):
        f4 = lambda x: mp.exp(E*(r2 + 1/mp.sqrt(r2))/mp.sqrt(x))
        fp = lambda x: mp.exp(E*((1 + r2)/x + r2 + 1/r2))
        bad = lambda x: fp(x)*(1 + x)
        pts = (mp.mpf('0.3'), mp.mpf(1), mp.mpf(3), mp.mpf(30))
        cm = [all((-1)**k*mp.diff(f, x, k) >= 0 for x in pts for k in range(7)) for f in (f4, fp, bad)]
        print(f"     E={float(E)}, r2={float(r2)}: four-body {cm[0]}, pair {cm[1]}, CONTROL (1+r1)*pair (must be False) {cm[2]}")
