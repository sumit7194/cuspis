"""EXP-061 pre-check 1 (instrument characterisation, unregistered): Hadamard finite part of the closed-form D_q(rho) on H^2 vs the dim-reg Gamma form D~_1(k,q). Adaptive precision near rho=0 (fixed quad cancellation). [model: Opus 5.5]"""
import sys; sys.path.insert(0,'.')
from mpmath import mp, mpf, mpc, quad, exp, sinh, cosh, legenp, re, log10, ceil
from exp059_stageA import Dt
mp.dps = 20
def fsub(r, q, k):
    extra = int(ceil(2 * max(0, -log10(r)))) + 10
    with mp.workdps(mp.dps + extra):
        r = mpf(r); P = re(legenp(mpc(-0.5, k), 0, cosh(r), type=3))
        v = -4 * exp(-q * r) * (q * sinh(r) + cosh(r)) * P / sinh(r) ** 2 + 4 / r ** 2
    return +v
def fp(k, q):
    f = lambda r: -4*exp(-q*r)*(q*sinh(r)+cosh(r))*re(legenp(mpc(-0.5,k),0,cosh(r),type=3))/sinh(r)**2
    return quad(lambda r: fsub(r, q, k), [0, 0.25, 1]) + quad(f, [1, 5, 20, 60]) + 4
worst = 0
for q in (0, mpf('0.5'), 1, 2, 3):
    for k in (mpf('0.3'), mpf(2), mpf(5), mpf(9)):
        v = fp(k, q); d = re(Dt(k, mpf(q))); worst = max(worst, abs(v/d-1))
        print(f"q={q} k={k}: f.p. {mp.nstr(v,14)}  D~_1 {mp.nstr(d,14)}  rel {mp.nstr(v/d-1,3)}")
print("worst rel", mp.nstr(worst,3))
