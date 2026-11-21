"""EXP-083 R3' arm (b) build (Bridge go 2026-11-22): the n-general (real n) sheet-symmetric replica saddle on the production
Strip3D lattice, from production's own per-slice poles/residues.
  Continued sheet average (single factor, Poisson):  A_n[G](x,x) = (1/M) sum_j G(j/M)(x,x) + sum_poles 2 pi i diag(Res G) [k_n - k_M],
      k_n(a0) = 1/expm1(-2 pi i n a0) (a0 = +i s),  -1/expm1(2 pi i n a0) (a0 = -i s);   d/dn k_n = production's _kdn.
  Gap (y-independent sigma on the N = Lx*Lt sites):  F(sigma; n) = (1/Ny) sum_p A_n[G_p^sigma](x,x) - target,
      target "direct" = (1/Ny) sum_p G_p^0(0)(x,x)  or  "self" = the same formula at sigma = 0, n = 1.
  Newton: Jacobian by central FD in sigma (rebuild all slices), then quasi-Newton (Broyden) steps.
Strip with sigma: production Slice with H0 -> H0 + diag(sigma); mirror slices aliased (m2_p = m2_{Ny-p}).
Independent pieces for the T_sad check live in exp083_honest (direct inverses, n-sheet saddle). [model: Opus 5.5]"""
import numpy as np
import sigma3d as S3

class SliceS(S3.Slice):
    def __init__(self, Lx, Lt, m2, cutx, tcut, idx, sigma):
        self.N = Lx * Lt; N = self.N
        H0 = np.zeros((N, N))
        for x in range(Lx):
            for t in range(Lt):
                i = idx(x, t); H0[i, i] = 4.0 + m2 + sigma[i]
                if x + 1 < Lx: j = idx(x + 1, t); H0[i, j] = H0[j, i] = -1.0
                if t + 1 < Lt: j = idx(x, t + 1); H0[i, j] = H0[j, i] = -1.0
        self.G0 = np.linalg.inv(H0)
        self.links = [(idx(x, tcut), idx(x, tcut + 1)) for x in cutx]
        sites = [s for lu in self.links for s in lu]
        self.P = sites; self.A = self.G0[:, sites]; self.M = self.G0[np.ix_(sites, sites)]
        self.W = len(self.links)
        self.s, self.Rp, self.Rm = ([], [], []) if self.W == 0 else self._poles()

def strip_sigma(g, sigma, s_cut=3.0):
    """Strip3D (production class) whose slices carry diag(sigma); sigma = None or zeros -> production slices exactly."""
    S = S3.Strip3D.__new__(S3.Strip3D)
    S.Lx, S.Lt, S.Ny, S.cutx, S.tcut, S.s_cut, S.drop_double, S.N = g.Lx, g.Lt, g.Ny, list(g.cutx), g.tcut, s_cut, False, g.N
    idx = lambda x, t: x * g.Lt + t; sig = np.zeros(g.N) if sigma is None else np.asarray(sigma, float)
    half = {p: SliceS(g.Lx, g.Lt, 2 - 2 * np.cos(2 * np.pi * p / g.Ny), g.cutx, g.tcut, idx, sig) for p in range(g.Ny // 2 + 1)}
    S.sl = [half[p if p <= g.Ny // 2 else g.Ny - p] for p in range(g.Ny)]
    return S

def kn(n, a0, up):
    """a0 = +-i s (s > 0): k = +1/expm1(2 pi n s) (up), -1/expm1(2 pi n s) (down). Real arithmetic: the complex expm1 of a large
    real argument returns inf + nan*i (Tier-1 run 1 at W = 4, M = 64: NaN)."""
    assert abs(a0.real) == 0.0
    with np.errstate(over="ignore"):
        v = 1.0 / np.expm1(2 * np.pi * n * abs(a0.imag))
    return v if up else -v

def avg_diag(sl, n, M=64, s_cut=np.inf):
    """continued (1/n) sum_j G(j/n)(x,x) for one slice (complex array; real for real n up to rounding)."""
    g0 = np.diag(sl.G0).astype(complex)
    out = sum(g0 - np.sum((sl.A @ sl.K(j / M)) * sl.A, axis=1) for j in range(M)) / M if sl.W else g0   # diag of G0 - A K A^T
    for j, sj in enumerate(sl.s):
        if sj > s_cut: continue
        for RK, a0, up in ((sl.Rp[j], 1j * sj, True), (sl.Rm[j], -1j * sj, False)):
            diagR = -np.sum((sl.A @ RK) * sl.A, axis=1)
            out = out + (2j * np.pi) * diagR * (kn(n, a0, up) - kn(M, a0, up))
    return out

def direct_avg_diag(sl, n):
    return sum(np.diag(S3._G_direct(sl, j / n)) for j in range(n)) / n

def ydiag(S, n, M=64, s_cut=np.inf):
    Ny = S.Ny; half = {p: avg_diag(S.sl[p], n, M, s_cut) for p in range(Ny // 2 + 1)}
    return sum(half[p if p <= Ny // 2 else Ny - p] for p in range(Ny)) / Ny

class Gap:
    def __init__(self, g, s_cut=np.inf, M=64, target="self"):
        self.g, self.s_cut, self.M = g, s_cut, M
        S0 = strip_sigma(g, None)
        if target == "self": self.target = ydiag(S0, 1.0, M, s_cut).real
        else: self.target = sum(np.diag(S0.sl[p if p <= g.Ny // 2 else g.Ny - p].G(0.0)).real for p in range(g.Ny)) / g.Ny
        self.nfev = 0
    def F(self, sig, n):
        self.nfev += 1; v = ydiag(strip_sigma(self.g, sig), n, self.M, self.s_cut)
        return v.real - self.target, float(np.abs(v.imag).max())
    def jac(self, sig, n, h=1e-6):
        N = self.g.N; J = np.zeros((N, N))
        for y in range(N):
            e = np.zeros(N); e[y] = h
            J[:, y] = (self.F(sig + e, n)[0] - self.F(sig - e, n)[0]) / (2 * h)
        return J
    def solve(self, n, sig0=None, tol=1e-13, itmax=40, J=None, noise_ceiling=1e-12):
        sig = np.zeros(self.g.N) if sig0 is None else np.array(sig0, float)
        F, im = self.F(sig, n); J = self.jac(sig, n) if J is None else J.copy(); hist = [float(np.abs(F).max())]
        best = (hist[0], sig.copy(), im)
        for it in range(itmax):
            if hist[-1] < tol: return sig, dict(it=it, F=hist[-1], hist=hist, imag=im, J=J)
            if hist[-1] < best[0]: best = (hist[-1], sig.copy(), im)
            # amendment (C1 run 1): |F| stagnates at the float64 noise floor 1e-14..3e-13 (sum of M = 64 O(0.3) diagonals);
            # stop on 6 non-improving steps and return the best iterate if it is below the noise ceiling 1e-12
            if it >= 6 and min(hist[-6:]) > best[0] and best[0] < noise_ceiling:
                return best[1], dict(it=it, F=best[0], hist=hist, imag=best[2], J=J, stagnated=True)
            ds = -np.linalg.solve(J, F); sig = sig + ds
            Fn, im = self.F(sig, n); J += np.outer(Fn - F - J @ ds, ds) / (ds @ ds); F = Fn; hist.append(float(np.abs(F).max()))
            if it in (8, 16, 24) and hist[-1] > 1e-3 * hist[-9]: J = self.jac(sig, n)            # stalled -> fresh FD Jacobian
        raise RuntimeError(f"continued gap not converged n={n}: |F| history {hist[-5:]}")
