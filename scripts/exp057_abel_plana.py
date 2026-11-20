"""EXP-057 (pre-registered in report.md, 54768d6): Abel-Plana continuation S_h(n) = sum_{k=1}^{n-1} h(k/n) for symmetric h.
S_h(n) = n Int_0^1 h - h(0) + 2i Int_0^inf [h(it/n) - h(-it/n)] / (e^{2 pi t} - 1) dt.   [model: Opus 5.5]"""
from mpmath import mp, mpf, quad, exp, sin, pi, inf, diff, zeta, sinh, log, expm1, re

mp.dps = 30

def S(h, n):
    n = mpf(n)
    I0 = quad(h, [0, 0.5, 1])
    I1 = quad(lambda t: (h(1j * t / n) - h(-1j * t / n)) / expm1(2 * pi * t), [0, 0.5, 2, 10, inf])
    return re(n * I0 - h(mpf(0)) + 2j * I1)

def direct(h, n): return sum(h(mpf(k) / n) for k in range(1, n))

def proto(L): return lambda a: (1 - exp(-2 * a * L)) * (1 - exp(-2 * (1 - a) * L))
def O1(L):
    def f(a):
        def one(x): return (1 - exp(-2 * x * L)) / (2 * x) if abs(x) > mpf('1e-25') else L
        return one(a) + one(1 - a)
    return f

if __name__ == "__main__":
    tests = {"a(1-a)": lambda a: a * (1 - a), "sin^2(pi a)": lambda a: sin(pi * a) ** 2,
             "proto L=3": proto(3), "proto L=10": proto(10)}
    ok1 = True
    for name, h in tests.items():
        v = S(h, 1); good = abs(v) <= 1e-12; ok1 &= good
        print(f"Q1 {name}: S_h(1) = {mp.nstr(v, 5)}  [{'PASS' if good else 'FAIL'}]")
    print(f"Q1 {'PASS' if ok1 else 'FAIL'}")
    hb = lambda a: sin(2 * pi * a) ** 2
    vb = S(hb, 1)
    print(f"Q1 must-fail sin^2(2 pi a) (growth e^{{4 pi|Im|}}): formula S(1) = {mp.nstr(vb, 8)} vs true 0 (predicted 1/2)  "
          f"[{'PASS (fires)' if abs(vb) > 0.1 else 'FAIL'}]")
    ok2 = True
    for L in (3, 10):
        d = diff(lambda n: S(proto(L), n), 1); c = 1 + L / sinh(L) ** 2; good = abs(d - c) <= 1e-10; ok2 &= good
        print(f"Q2 proto L={L}: dS/dn|1 = {mp.nstr(d, 15)} vs 1 + L/sinh^2 L = {mp.nstr(c, 15)}  diff {mp.nstr(d - c, 3)}  [{'PASS' if good else 'FAIL'}]")
    print(f"Q2 {'PASS' if ok2 else 'FAIL'}")
    for L in (5, 20, 80):
        h = O1(L); d = diff(lambda n: S(h, n), 1)
        print(f"Q3 O(1) channel L={L}: dS/dn|1 = {mp.nstr(d, 12)}   (zeta(2) = {mp.nstr(zeta(2), 12)}; ln L = {mp.nstr(log(L), 6)}); S(1) = {mp.nstr(S(h, 1), 5)}")
    ok4 = True
    for name, h in list(tests.items()) + [("O1 L=5", O1(5))]:
        for n in (2, 3, 5):
            a, b = S(h, n), direct(h, n); good = abs(a - b) <= 1e-12; ok4 &= good
            if not good: print(f"Q4 {name} n={n}: continued {a} vs direct {b}  FAIL")
    print(f"Q4 integer-n control {'PASS' if ok4 else 'FAIL'}")
