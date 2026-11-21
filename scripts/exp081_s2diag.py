"""EXP-081a S2 diagnosis (S2 fired: lattice d*r = -0.0157 vs -1/32). (1) code check: continued single-factor average
(1/n) sum_k DeltaG^(k/n)(x,x) at integer n = 2, 3 (Poisson residue form) vs honest, on the S2 geometry (P=12, Ny=48), and the
derivative by finite difference vs coincident_dn. (2) physics: d*r vs box and r using SPARSE per-slice data at L = infinity
(continuous k), single edge, boxes P in {12, 24, 48}. [model: Opus 5.5]"""
import numpy as np, scipy.sparse as sp, scipy.sparse.linalg as spla, sigma3d as S3
from numpy.polynomial.legendre import leggauss
# ---- (1) code check on the S2 geometry
P = 12; Lx, Lt = 2 + 2 * P, 2 * P; tc = P - 1; S = S3.Strip3D(Lx, Lt, 48, list(range(P, Lx)), tc)
sites = [x * Lt + tc + 1 + m for m in (2, 3, 4) for x in (P - 1, P)]
def cont_avg(S, n):
    """(1/n) sum_k f(k/n), f(a) = DeltaG_3D^(a)(x,x): int_0^1 f + pole tails with kernels 1/(e^{-+2 pi i n a} - 1)."""
    a = np.arange(64) / 64; I0 = np.mean([np.mean([np.diag(s.G(ai) - s.G0) for s in S.sl], axis=0) for ai in a], axis=0)
    tail = np.zeros(S.N, dtype=complex)
    for sp_ in S.sl:
        for j, sj in enumerate(sp_.s):
            for RK, a0, up in ((sp_.Rp[j], 1j * sj, True), (sp_.Rm[j], -1j * sj, False)):
                dR = -np.sum((sp_.A @ RK) * sp_.A, axis=1)
                ker = 1.0 / np.expm1(-2j * np.pi * n * a0) if up else -1.0 / np.expm1(2j * np.pi * n * a0)
                tail += (2j * np.pi) * dR * ker
    return I0 + tail / S.Ny
for n in (2, 3):
    hon = np.mean([np.mean([np.diag(s.G(k / n) - s.G0) for s in S.sl], axis=0) for k in range(n)], axis=0)
    c = cont_avg(S, n); print(f"(1) n={n}: max |cont - honest| at window sites = {np.max(np.abs(c[sites]-hon[sites])):.1e} (values ~{np.abs(hon[sites]).max():.1e})", flush=True)
h = 1e-4; fd = (cont_avg(S, 1 + h) - cont_avg(S, 1 - h)) / (2 * h); d = S3.coincident_dn(S)
print(f"(1) d by FD of the continuation vs coincident_dn: max rel diff {np.max(np.abs(fd[sites]-d[sites]))/np.max(np.abs(d[sites])):.1e}", flush=True)
# ---- (2) sparse single-edge d(x) at L = infinity
def d_sparse(P, ms, nk=40):
    Lx, Lt = 2 + 2 * P, 2 * P; tc = P - 1; idx = lambda x, t: x * Lt + t; N = Lx * Lt
    cutx = list(range(P, Lx)); links = [(idx(x, tc), idx(x, tc + 1)) for x in cutx]; cs = [s for lu in links for s in lu]
    rows, cols, vals = [], [], []
    for x in range(Lx):
        for t in range(Lt):
            i = idx(x, t)
            if x + 1 < Lx: j = idx(x + 1, t); rows += [i, j]; cols += [j, i]; vals += [-1.0, -1.0]
            if t + 1 < Lt: j = idx(x, t + 1); rows += [i, j]; cols += [j, i]; vals += [-1.0, -1.0]
    Hoff = sp.csc_matrix((vals, (rows, cols)), shape=(N, N)); E = np.zeros((N, len(cs))); E[cs, np.arange(len(cs))] = 1
    obs = [(x, tc + 1 + m) for m in ms for x in (P - 1, P)]; oi = [idx(x, t) for x, t in obs]
    u, wu = leggauss(nk); u = 0.5 * (u + 1); wu = 0.5 * wu; dtot = np.zeros(len(oi), dtype=complex)
    class Sl: pass
    for ui, wi in zip(u, wu):
        k = np.pi * ui ** 3; w_k = 2 * 3 * np.pi * ui ** 2 * wi / (2 * np.pi)
        A = spla.splu((Hoff + sp.identity(N) * (6.0 - 2 * np.cos(k))).tocsc()).solve(E)
        s = Sl(); s.W = len(links); s.M = A[cs, :]; s.A = A
        s.C = S3.Slice.C.__get__(s); s.K = S3.Slice.K.__get__(s); s.residue_K = S3.Slice.residue_K.__get__(s)
        ss, Rp, Rm = S3.Slice._poles(s)
        dk = np.zeros(len(oi), dtype=complex)
        for j, sj in enumerate(ss):
            for RK, a0, up in ((Rp[j], 1j * sj, True), (Rm[j], -1j * sj, False)):
                dR = -np.sum((A[oi] @ RK) * A[oi], axis=1); dk += (2j * np.pi) * dR * S3._kdn(a0, up)
        dtot += w_k * dk
    rs = [np.sqrt(0.25 + (t - tc - 0.5) ** 2) for x, t in obs]
    return [(round(r, 2), round((dv * r).real, 5)) for r, dv in zip(rs, dtot)]
for P2, ms in ((12, (2, 3, 4)), (24, (2, 4, 6, 8)), (48, (2, 4, 8, 12, 16))):
    print(f"(2) single edge, box P={P2}, L=inf: (r, d*r) = {d_sparse(P2, ms)}", flush=True)
