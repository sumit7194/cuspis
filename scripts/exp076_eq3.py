"""EXP-076 E2/E3: Neon T36's eq. (2)-(3) implemented for a scalar 'Delta G' function g (an analytic function on (0,1),
continued off-axis), vs exact integer-n inner sums K_n^(q/n) = (2/n) sum_k g(k/n) g(((q-k)/n) mod 1).
(a) T36's own polynomial toy g = a(1-a): reproduce its stated C1(beta) = -(1/6) b(1-b)(2+b(1-b)) [implementation check].
(b) pure straddle toy g = e^{2 pi i a} - 1 (G1 = 1, B1 = 2): gauge covariance at integer n requires
    B^(q) = B1 + 4 Gbar_n + K_n^(q) = 2 e^{2 pi i q/n}; test what eq.(2)-(3) gives at n = 1. [model: Opus 5.5]"""
import numpy as np
from scipy.integrate import quad
def cquad(f, a, b, **kw):
    re = quad(lambda x: f(x).real, a, b, limit=400, **kw)[0]; im = quad(lambda x: f(x).imag, a, b, limit=400, **kw)[0]
    return re + 1j * im
def K1_eq3(g, beta):
    frac = lambda x: x - np.floor(x)
    main = 2 * (cquad(lambda a: g(a) * g(beta - a), 0, beta) + cquad(lambda a: g(a) * g(beta - a + 1), beta, 1))
    def tail(t):
        it = 1j * t
        return ((g(it) - g(1 + it)) * g(beta - it) - (g(-it) - g(1 - it)) * g(beta + it)
                + g(beta + it) * (g(1 - it) - g(-it)) - g(beta - it) * (g(1 + it) - g(it))) / np.expm1(2 * np.pi * t)
    tails = 2j * cquad(tail, 0, 40)
    return main, tails, main + tails
def Kn(g, n, q):
    return (2.0 / n) * sum(g(k / n) * g(((q - k) / n) % 1.0) for k in range(n))
def gbar(g, n):
    return sum(g(k / n) for k in range(n)) / n
if __name__ == "__main__":
    gp = lambda a: a * (1 - a)
    print("(a) polynomial toy g = a(1-a): eq.(2)-(3) K1 vs T36's stated C1(beta)")
    for b in (0.25, 0.5, 0.7):
        m, t, K = K1_eq3(gp, b); C1 = -(1 / 6) * b * (1 - b) * (2 + b * (1 - b))
        print(f"   beta={b}: main {m.real:+.10f} tails {t.real:+.10f} K1 {K.real:+.10f} | C1 {C1:+.10f} | K1/C1 {K.real/C1:.6f}")
    print("    integer-n K_n^(q/n), n=2..6, q=1 (for comparison):", [round(Kn(gp, n, 1), 8) for n in range(2, 7)])
    gs = lambda a: np.exp(2j * np.pi * a) - 1
    print("(b) pure straddle toy g = e^{2 pi i a} - 1  (G1 = 1, B1 = 2)")
    for n in (2, 3, 5):
        for q in range(n):
            Bq = 2 + 4 * gbar(gs, n) + Kn(gs, n, q)
            print(f"   n={n} q={q}: 4*Gbar={4*gbar(gs, n):+.3f}  K_n={Kn(gs, n, q):+.4f}  B^(q)={Bq:+.4f}  vs 2e^(2pi i q/n)={2*np.exp(2j*np.pi*q/n):+.4f}")
    for b in (0.0, 0.25, 0.5, 0.5 + 0.3j):
        m, t, K = K1_eq3(gs, b)
        print(f"   n=1 eq.(2)-(3): beta={b}: main {m:+.5f} tails {t:+.1e}  K1 {K:+.5f} | gauge-required K1 = 2(e^(2pi i b)-1) = {2*(np.exp(2j*np.pi*b)-1):+.5f}")
