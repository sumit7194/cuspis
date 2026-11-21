"""EXP-083 R3 build (Tier-1, no verdict): route (ii) Q_cont(n) for the production Strip3D, ported from sigma_engine
(lattice_Qcont_route_ii, EXP-079) with y-slices summed over k:
  Q_cont(n) = sum_k [logdet B_{n,k}^(0) - logdet B1_k] + n int_eps^{1-eps} g_n(b) db
              - 2 i n int_0^inf [g_n(eps + i t) - g_n(eps - i t)] / (e^{2 pi n t} + 1) dt,   eps = 1/(2n),
  g_n(b) = sum_k [logdet B_{n,k}^(b) - logdet B1_k]  (Strip3D.inner(n, b), inner_beta0(n)).
Branch: log det = log|det| + i arg det, with arg unwrapped along each path (t-path sampled densely, then Gauss quadrature on
the unwrapped interpolant is replaced by a dense trapezoid-free Gauss-on-segments scheme with unwrapping per segment).
[model: Opus 5.5]"""
import numpy as np
import sigma3d as S3
from numpy.polynomial.legendre import leggauss

def ldet(M):
    s, l = np.linalg.slogdet(M); return l + 1j * np.angle(s)

class QCont:
    def __init__(self, S, npt=40, npt0=64):
        self.S, self.npt, self.npt0 = S, npt, npt0; B1 = S.B1(); self.ld1 = np.array([ldet(B1[k]) for k in range(S.Ny)])
    def gk(self, n, b):
        B = self.S.inner(n, b, self.npt); return np.array([ldet(B[k]) for k in range(self.S.Ny)]) - self.ld1
    def q0(self, n):
        B = self.S.inner_beta0(n, npt=self.npt0); return np.array([ldet(B[k]) for k in range(self.S.Ny)]) - self.ld1
    @staticmethod
    def unwrap_path(vals):
        """vals: (npoints, Ny) complex log dets along a path; unwrap imaginary parts per k along the path."""
        v = np.array(vals); im = np.unwrap(v.imag, axis=0); return v.real + 1j * im
    def Q(self, n, Mx=24, Mt=48, tmax=4.0, nseg=8):
        eps = 1.0 / (2.0 * n); x, w = leggauss(Mx)
        # real (beta) path: eps -> 1 - eps, ordered, unwrapped
        bs = [0.5 * (1 - 2 * eps) * xi + 0.5 for xi in x]
        order = np.argsort(np.real(bs)); gb = self.unwrap_path([self.gk(n, bs[i]) for i in order])
        Ireal = n * sum(0.5 * (1 - 2 * eps) * w[order[j]] * gb[j].sum() for j in range(len(order)))
        # tail paths eps +- i t, t in [0, tmax], Gauss on nseg segments, unwrapped from t = 0
        tg, wg = leggauss(Mt // nseg); ts, ws = [], []
        for s in range(nseg):
            a, b = s * tmax / nseg, (s + 1) * tmax / nseg; ts += list(0.5 * (b - a) * (tg + 1) + a); ws += list(0.5 * (b - a) * wg)
        ts, ws = np.array(ts), np.array(ws)
        gp = self.unwrap_path([self.gk(n, eps)] + [self.gk(n, eps + 1j * t) for t in ts])[1:]
        gm = self.unwrap_path([self.gk(n, eps)] + [self.gk(n, eps - 1j * t) for t in ts])[1:]
        Itail = sum(wi * (-2j * n) * (gp[i].sum() - gm[i].sum()) / (np.exp(2 * np.pi * n * ti) + 1.0) for i, (ti, wi) in enumerate(zip(ts, ws)))
        return self.q0(n).sum() + Ireal + Itail
