"""sigma_engine.py — Stage P0 engine for the O(N^0) sector continuation (EXP-079, registered in report.md, 6906e70).

Formula (Neon T40, verified on the P4' toy by EXP-078):
    Q'(1) = Tr(B1^{-1} d_n B_n^(0)|_1) + C[g_1],   g_1(beta) = logdet B_1^(beta) - logdet B1,
    C[g] = int_0^inf ds pi/cosh^2(pi s) g(1/2 + is),
    B_n^(beta) = continued inner sector sum (2/n) sum_k G^(k/n) o G^(beta - k/n).
This file is Cuspis's own code (no T40 code imported). Components:
  * ap_single(f, n): continued (1/n) sum_{k=0}^{n-1} f(k/n) for f analytic on (0,1) with jump df(z) = f(z) - f(1+z):
        I_n[f] = int_0^1 f + (f(0+) - f(1-))/(2n) + i int_0^inf [df(it) - df(-it)] / (e^{2 pi n t} - 1) dt
    (Abel-Plana on [0, n] minus the k = n term; derived in report EXP-079 notes).
  * inner_general(g, n, beta): T40's strip formula, coded here independently, for scalar g (mpmath):
        int_0^beta 2 g(a) g(beta-a) + int_beta^1 2 g(a) g(1+beta-a)
        + 4i int_0^inf [dg(it) g(beta-it) - dg(-it) g(beta+it)] / (e^{2 pi n t} - 1) dt.
  * Lattice (1-periodic meromorphic G(a) = H(e^{2 pi i a})^{-1}): poles a = +-i s_j from det H(z) = 0; inner sum by
    Poisson with residue-evaluated Fourier coefficients, second-factor poles ANCHORED at beta (k -> q-k symmetry), so the
    n-dependence is only through 1/(e^{2 pi n s_j} - 1) (type 0 in Im n). beta = 0: double poles, contour residues.
  * Outer: route (i) the n = 1 formula above; route (ii) shifted Abel-Plana Q_cont(n) at eps = 1/(2n) (T40's outer
    formula, coded here independently) for integer checks and a finite-difference Q'(1).
[model: Opus 5.5]"""
import numpy as np
import mpmath as mp
from numpy.polynomial.legendre import leggauss

# ----------------------------------------------------------------------------------------------- generic pieces
def C_line(g, smax=10.0, nseg=(0.0, 0.5, 1.5, 3.0, 6.0, 10.0), npt=24, mpmode=False):
    """C[g] = int_0^inf ds pi/cosh^2(pi s) g(1/2 + is) (truncated at smax; weight ~ 4 pi e^{-2 pi s})."""
    if mpmode:
        return mp.quad(lambda s: mp.pi / mp.cosh(mp.pi * s) ** 2 * g(mp.mpf("0.5") + 1j * s), list(nseg))
    x, w = leggauss(npt); tot = 0.0
    for lo, hi in zip(nseg[:-1], nseg[1:]):
        s = 0.5 * (hi - lo) * (x + 1) + lo; ws = 0.5 * (hi - lo) * w
        tot = tot + sum(wi * np.pi / np.cosh(np.pi * si) ** 2 * g(0.5 + 1j * si) for si, wi in zip(s, ws))
    return tot

def ap_single(f, n, f0=None, f1=None):
    """continued (1/n) sum_{k=0}^{n-1} f(k/n), scalar mpmath f analytic on (0,1); jump df(z) = f(z) - f(1+z)."""
    f0 = f(mp.mpf(0)) if f0 is None else f0; f1 = f(mp.mpf(1)) if f1 is None else f1
    df = lambda z: f(z) - f(1 + z)
    tail = mp.quad(lambda t: 1j * (df(1j * t) - df(-1j * t)) / mp.expm1(2 * mp.pi * n * t), [0, 1, 4, mp.inf])
    return mp.quad(f, [0, 0.5, 1]) + (f0 - f1) / (2 * n) + tail

def inner_general(g, n, beta):
    """T40 strip formula for scalar g (mpmath), coded independently. Straight segments 0->beta, beta->1 in C."""
    dg = lambda z: g(z) - g(1 + z)
    I1 = mp.quad(lambda u: beta * 2 * g(u * beta) * g((1 - u) * beta), [0, 1])
    I2 = mp.quad(lambda u: (1 - beta) * 2 * g(beta + u * (1 - beta)) * g(1 - u * (1 - beta)), [0, 1])
    tail = mp.quad(lambda t: 4j * (dg(1j * t) * g(beta - 1j * t) - dg(-1j * t) * g(beta + 1j * t)) / mp.expm1(2 * mp.pi * n * t),
                   [0, 1, 4, mp.inf])
    return I1 + I2 + tail

def honest_inner_scalar(g, n, q):
    """(2/n) sum_k g(k/n) g({(q-k)/n}) with g's periodic extension on [0,1)."""
    return (mp.mpf(2) / n) * mp.fsum(g(mp.mpf(k) / n) * g(mp.mpf((q - k) % n) / n) for k in range(n))

# ----------------------------------------------------------------------------------------------- lattice provider
class Lattice:
    """2D lattice slice: H(z) = diag + hopping, twist z = e^{2 pi i a} on given links (going 'up' carries z).
    Gives G(a) = H(e^{2 pi i a})^{-1}, its poles a = +-i s_j (det H(z) = 0, z real in (0,1) or > 1) and residues."""
    def __init__(self, Lx, Lt, m2, cut_links, order="xt"):
        self.Lx, self.Lt, self.m2, self.cut = Lx, Lt, m2, set(cut_links)   # cut link (x,t): (x,t) -> (x,t+1)
        self.N = Lx * Lt
        self.idx = (lambda x, t: x * Lt + t) if order == "xt" else (lambda x, t: t * Lx + x)
        self._poles()
    def H(self, z):
        N, M = self.N, np.zeros((self.N, self.N), dtype=complex)
        for x in range(self.Lx):
            for t in range(self.Lt):
                i = self.idx(x, t); M[i, i] = 4.0 + self.m2
                if x + 1 < self.Lx:
                    j = self.idx(x + 1, t); M[i, j] = M[j, i] = -1.0
                if t + 1 < self.Lt:
                    j = self.idx(x, t + 1)
                    if (x, t) in self.cut: M[j, i] = -z; M[i, j] = -1.0 / z
                    else: M[i, j] = M[j, i] = -1.0
        return M
    def G(self, a):
        return np.linalg.inv(self.H(np.exp(2j * np.pi * a)))
    def _poles(self):
        R = len(self.cut); deg = 2 * R
        zs = np.exp(2j * np.pi * np.arange(deg + 1) / (deg + 1))
        V = np.array([[z ** p for p in range(deg + 1)] for z in zs])
        c = np.linalg.solve(V, [z ** R * np.linalg.det(self.H(z)) for z in zs])
        roots = np.roots(c[::-1])
        inside = sorted([r.real for r in roots if abs(r.imag) < 1e-8 * abs(r) and 0 < r.real < 1], reverse=True)
        self.s = [-np.log(r) / (2 * np.pi) for r in inside]          # poles at a = +- i s_j
        if len(self.s) != R:
            raise ValueError(f"expected {R} real-positive pole pairs, got {len(self.s)}: roots {roots}")
        self.Rp = [self.residue(1j * s) for s in self.s]; self.Rm = [self.residue(-1j * s) for s in self.s]
    def residue(self, a0, rad=1e-6, M=32):
        th = 2 * np.pi * np.arange(M) / M
        return sum(self.G(a0 + rad * np.exp(1j * t)) * (rad * np.exp(1j * t)) for t in th) / M

def inner_pair(La, Lb, n, beta, npt=40):
    """continued (2/n) sum_k Ga(k/n) o Gb(beta - k/n), 0 < Re beta < 1: main integral (straight segments in C)
    + residue tails: first-factor poles of Ga (anchor 0) and second-factor poles of Gb anchored at beta (k -> q-k).
    Both tails depend on n only through 1/(e^{2 pi n s} - 1)."""
    x, w = leggauss(npt); u = 0.5 * (x + 1); wu = 0.5 * w
    I1 = sum(wi * beta * 2 * La.G(ui * beta) * Lb.G((1 - ui) * beta) for ui, wi in zip(u, wu))
    I2 = sum(wi * (1 - beta) * 2 * La.G(beta + ui * (1 - beta)) * Lb.G(1 - ui * (1 - beta)) for ui, wi in zip(u, wu))
    tail = 0
    for s, Rp, Rm in zip(La.s, La.Rp, La.Rm):       # poles of Ga at +-is: upper kernel 1/(e^{-2pi i n a}-1), lower -1/(e^{2pi i n a}-1)
        tail = tail + (2j * np.pi) * (2 * Rp * Lb.G(beta - 1j * s) - 2 * Rm * Lb.G(beta + 1j * s)) / np.expm1(2 * np.pi * n * s)
    for s, Rp, Rm in zip(Lb.s, Lb.Rp, Lb.Rm):       # poles of Gb(a') anchored at beta (a = beta - a')
        tail = tail + (2j * np.pi) * (2 * La.G(beta - 1j * s) * Rp - 2 * La.G(beta + 1j * s) * Rm) / np.expm1(2 * np.pi * n * s)
    return I1 + I2 + tail

def inner_lattice(L, n, beta, npt=40):
    return inner_pair(L, L, n, beta, npt)

def inner_pair_beta0(La, Lb, n, npt=64, rad=1e-5, M=32):
    """continued (2/n) sum_k Ga(k/n) o Gb(-k/n): periodic main integral (trapezoid) + contour residues at every pole of
    F0(a) = 2 Ga(a) Gb(-a) (poles +-i s_a and -+i s_b; coincident ones merge into double poles)."""
    a = np.arange(npt) / npt
    I0 = sum(2 * La.G(ai) * Lb.G(-ai) for ai in a) / npt
    locs = []
    for s in list(La.s) + list(Lb.s):
        for p in (1j * s, -1j * s):
            if all(abs(p - q) > 1e-9 for q in locs): locs.append(p)
    tail = 0; th = 2 * np.pi * np.arange(M) / M
    for a0 in locs:
        up = a0.imag > 0; acc = 0
        for t in th:
            dz = rad * np.exp(1j * t); al = a0 + dz
            ker = 1.0 / np.expm1(-2j * np.pi * n * al) if up else -1.0 / np.expm1(2j * np.pi * n * al)
            acc = acc + 2 * La.G(al) * Lb.G(-al) * ker * dz
        tail = tail + (2j * np.pi) * acc / M
    return I0 + tail

def inner_lattice_beta0(L, n, npt=64, rad=1e-5, M=32):
    return inner_pair_beta0(L, L, n, npt, rad, M)

def logdet(M):
    s, ld = np.linalg.slogdet(M); return ld + np.log(s + 0j)

def honest_Q(L, n):
    """honest sector sum at integer n: sum_q logdet (2/n) sum_k G(k/n) o G((q-k)/n) - n logdet B1."""
    Gs = [L.G(k / n) for k in range(n)]; B1 = 2 * Gs[0] * Gs[0]; ld1 = logdet(B1)
    return sum(logdet((2.0 / n) * sum(Gs[k] * Gs[(q - k) % n] for k in range(n))) for q in range(n)) - n * ld1

def lattice_Qprime_route_i(L, h=1e-4, smax=10.0):
    """route (i): Tr(B1^{-1} d_n B_n^(0)|_1) + C[g_1]."""
    B1 = 2 * L.G(0.0) * L.G(0.0); ld1 = logdet(B1)
    dB0 = (inner_lattice_beta0(L, 1 + h) - inner_lattice_beta0(L, 1 - h)) / (2 * h)
    t0 = np.trace(np.linalg.solve(B1, dB0))
    g1 = lambda b: logdet(inner_lattice(L, 1.0, b)) - ld1
    return t0 + C_line(g1, smax=smax), t0

def lattice_Qcont_route_ii(L, n, Mx=36, Mt=64, tmax=6.0, drop_confluent=False):
    """route (ii): Q_cont(n) = [logdet B_n^(0) - logdet B1] + shifted Abel-Plana for sum_{q=1}^{n-1} g_n(q/n) at eps=1/(2n)."""
    B1 = 2 * L.G(0.0) * L.G(0.0); ld1 = logdet(B1)
    B0 = inner_lattice_beta0(L, n)
    if drop_confluent:                                  # planted break: replace B_n^(0) by its main integral only
        a = np.arange(64) / 64; B0 = sum(2 * L.G(ai) * L.G(-ai) for ai in a) / 64
    Q0 = logdet(B0) - ld1
    g = lambda b: logdet(inner_lattice(L, n, b)) - ld1
    eps = 1.0 / (2.0 * n); x, w = leggauss(Mx)
    Ireal = n * sum(0.5 * (1 - 2 * eps) * wi * g(0.5 * (1 - 2 * eps) * xi + 0.5) for xi, wi in zip(x, w))
    tg, wt = leggauss(Mt); t = 0.5 * tmax * (tg + 1); wt = 0.5 * tmax * wt
    Itail = sum(wi * (-2j * n) * (g(eps + 1j * ti) - g(eps - 1j * ti)) / (np.exp(2 * np.pi * n * ti) + 1.0) for ti, wi in zip(t, wt))
    return Q0 + Ireal + Itail
