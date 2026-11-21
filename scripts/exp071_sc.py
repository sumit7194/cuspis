"""SC (sector-continuation) module for delta-kappa, built for EXP-071+ (K-free first). Fresh implementations, tested against
EXP-044 (c-functions, kappa) and EXP-069 (complex-twist BIE). [model: Opus 5.5]
C_line(g): Cuspis's own n->1 continuation  C[g] = d/dn sum_{q=1}^{n-1} g(q/n) |_{n=1} = Int_0^inf ds (pi/cosh^2 pi s) g(1/2+is), symmetric g
(sign/normalisation to be fixed against the EXP-044 C0 identity in the pre-check, not assumed)."""
import math
import numpy as np
from scipy.integrate import quad
def C_line(g, smax=6.0, ns=60):
    x, w = np.polynomial.legendre.leggauss(ns); s = 0.5 * smax * (x + 1); w = 0.5 * smax * w
    return sum(wi * math.pi / math.cosh(math.pi * si) ** 2 * g(0.5 + 1j * si) for si, wi in zip(s, w))
def honest_dn(g, n_list=(2, 3, 4, 5, 6)):
    """finite sums S(n) = sum_{q=1}^{n-1} g(q/n) at integer n (for the C0-type identity check)"""
    return {n: sum(g(q / n) for q in range(1, n)) for n in n_list}
