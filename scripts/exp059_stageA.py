"""EXP-059 (pre-registered in report.md, f3990fa): Sigma build stage A at n = 1. [model: Opus 5.5]"""
import sys, os, time, math
import numpy as np
from mpmath import mp, mpf, mpc, quad, exp, legenp, cosh, sinh, gamma, loggamma, pi, inf, tanh, re, im
D0 = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D0)
mp.dps = 25

def log(*a): print(time.strftime("%H:%M:%S"), *a, flush=True)

def lap_closed(p, nu):
    return gamma((p - nu) / 2) * gamma((p + nu + 1) / 2) / (2 * gamma((p - nu + 1) / 2) * gamma((p + nu + 2) / 2))

def Dt(k, q, swap=False):                       # D~_1(k, q) = 1/B~_1 (Gamma ratio); swap -> wrong form (must-fail)
    a, b = (q + mpf(3) / 2, q + mpf(1) / 2) if not swap else (q + mpf(1) / 2, q + mpf(3) / 2)
    return 8 * exp(loggamma((a - 1j * k) / 2) + loggamma((a + 1j * k) / 2) - loggamma((b - 1j * k) / 2) - loggamma((b + 1j * k) / 2))

def B3(x): return x ** 3 - mpf(3) / 2 * x ** 2 + x / 2
def cq(q): return mpf(16) / 3 * (B3(q / 2 + mpf(3) / 4) - B3(q / 2 + mpf(1) / 4))

def Dpos(q, r): return -(2 / pi) * exp(-q * r) * (q * sinh(r) + cosh(r)) / sinh(r) ** 3

def invMF(F, r, K=300, width=1.0, nodes=24):
    x, w = np.polynomial.legendre.leggauss(nodes); tot = mpf(0); a = 0.0
    ch = cosh(mpf(r))
    while a < K:
        b = a + width
        for xi, wi in zip(x, w):
            k = mpf(0.5 * (b - a) * xi + 0.5 * (b + a))
            tot += mpf(0.5 * (b - a) * wi) * k * tanh(pi * k) / (2 * pi) * re(legenp(mpc(-0.5, k), 0, ch, type=3)) * re(F(k))
        a = b
    return tot

def recon(qt, r, swap=False, K=300):
    c0, c1, c2 = cq(mpf(qt)), cq(mpf(1)), cq(mpf(2))
    l1 = (c0 - c2) / (c1 - c2); l2 = 1 - l1
    R = lambda k: Dt(k, mpf(qt), swap) - l1 * Dt(k, mpf(1), swap) - l2 * Dt(k, mpf(2), swap)
    return invMF(R, r, K=K) + l1 * Dpos(1, mpf(r)) + l2 * Dpos(2, mpf(r)), (l1, l2)

if __name__ == "__main__":
    ok = True
    for p, nu in ((mpf('1.3'), mpf('-0.2')), (mpf('2.5'), mpc('0.7', '0.4')), (mpf('0.9'), mpc('-0.5', '1.1'))):
        num = quad(lambda t: exp(-p * t) * legenp(nu, 0, cosh(t), type=3), [0, 1, 5, 20, inf]); cl = lap_closed(p, nu)
        good = abs(num - cl) <= 1e-10 * abs(cl); ok &= good
        log(f"A1 p={p} nu={nu}: quad {mp.nstr(num, 14)}  closed {mp.nstr(cl, 14)}  [{'PASS' if good else 'FAIL'}]")
    log(f"A1 {'PASS' if ok else 'FAIL'}")
    # Stirling coefficient sanity (diagnostic): k^2 (D/(4k) - 1) -> c(q)
    for q in (0, 1, 2):
        k = mpf(400); log(f"  c({q}) = {mp.nstr(cq(mpf(q)), 10)};  k^2(D/4k - 1) at k=400: {mp.nstr(k**2 * (re(Dt(k, mpf(q))) / (4 * k) - 1), 10)}")
    # A2: Gamma form vs EXP-056 mode-sum instrument at n = 1
    import exp056_sigma_kernel as K
    ok2 = True
    for q in (0, 1, 2):
        R, Wt = K.rho_grid_fine(400.0); Ws, sig, _ = K.weight_scaled(1.0, 0.0, q, R, Wt)
        for k in (0.3, 1.7, 5.0):
            inst = K.Bks(R, Ws, sig, k).real; cl = float(re(1 / Dt(mpf(k), mpf(q))))
            good = abs(inst / cl - 1) <= 3e-5; ok2 &= good
            log(f"A2 q={q} k={k}: mode-sum {inst:.10f}  Gamma form {cl:.10f}  rel {inst/cl-1:+.1e} [{'PASS' if good else 'FAIL'}]")
    log(f"A2 {'PASS' if ok2 else 'FAIL'}")
    ok3 = True
    for r in (0.3, 1.0, 3.0):
        t0 = time.time(); v, lam = recon(0, r); tgt = Dpos(0, mpf(r)); rel = abs(v / tgt - 1); good = rel <= 1e-4; ok3 &= good
        log(f"A3 rho={r}: reconstructed D_0 {mp.nstr(v, 12)}  closed {mp.nstr(tgt, 12)}  rel {mp.nstr(rel, 3)} [{'PASS' if good else 'FAIL'}]  (lambda {mp.nstr(lam[0],6)}, {mp.nstr(lam[1],6)}; {time.time()-t0:.0f}s)")
    log(f"A3 {'PASS' if ok3 else 'FAIL'}")
    ok4 = True
    for r in (0.3, 1.0, 3.0):
        v, _ = recon(0.5, r); tgt = Dpos(mpf('0.5'), mpf(r)); rel = abs(v / tgt - 1); good = rel <= 1e-4; ok4 &= good
        log(f"A4 q=0.5 rho={r}: reconstructed {mp.nstr(v, 12)}  continued closed {mp.nstr(tgt, 12)}  rel {mp.nstr(rel, 3)} [{'PASS' if good else 'FAIL'}]")
    log(f"A4 {'PASS' if ok4 else 'FAIL'}")
    v, _ = recon(0, 1.0, swap=True); tgt = Dpos(0, mpf(1)); rel = abs(v / tgt - 1)
    log(f"must-fail (swapped Gamma form) rho=1: {mp.nstr(v, 8)} vs {mp.nstr(tgt, 8)}  rel {mp.nstr(rel, 3)} [{'PASS (fires)' if rel > 0.1 else 'FAIL'}]")
