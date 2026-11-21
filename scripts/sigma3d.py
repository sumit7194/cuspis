"""sigma3d.py — Stage P1 slice layer for the sigma engine (EXP-079 accepted engine; this file adds 3D y-Fourier slices).
3D cubic lattice: 2D slice (x, t) of Lx x Lt sites (Dirichlet), y periodic with Ny sites -> slices p with mass^2
m_p^2 = 2 - 2 cos(2 pi p / Ny). Twist z = e^{2 pi i a} on the t-links (x, tcut) -> (x, tcut+1) for x in `cutx` (all y).
Per slice, Woodbury: H(z) = H0 + P C(z) P^T (P selects the 2W cut sites, C(z) block per link), so
    G(a) = G0 - A K(a) A^T,   A = G0 P,   K(a) = C(z) (I + M C(z))^{-1},   M = P^T G0 P,
poles from det(I + M C(z)) = 0 (2W x 2W), residues by small 2W x 2W contours.
Per-slice bubble k:  B_k = (2/Ny) sum_p G_p o G_{k-p}  (cyclic convolution over p, done by FFT along the slice index).
Continued inner sum per (k, beta): (1/Ny) sum_p inner_pair(p, k-p) with sigma_engine's anchored-residue tails.
[model: Opus 5.5]"""
import numpy as np
from numpy.polynomial.legendre import leggauss

class Slice:
    def __init__(self, Lx, Lt, m2, cutx, tcut, idx):
        self.N = Lx * Lt; N = self.N
        H0 = np.zeros((N, N))
        for x in range(Lx):
            for t in range(Lt):
                i = idx(x, t); H0[i, i] = 4.0 + m2
                if x + 1 < Lx: j = idx(x + 1, t); H0[i, j] = H0[j, i] = -1.0
                if t + 1 < Lt: j = idx(x, t + 1); H0[i, j] = H0[j, i] = -1.0
        self.G0 = np.linalg.inv(H0)
        self.links = [(idx(x, tcut), idx(x, tcut + 1)) for x in cutx]      # (lower l, upper u)
        sites = [s for lu in self.links for s in lu]
        self.P = sites; self.A = self.G0[:, sites]; self.M = self.G0[np.ix_(sites, sites)]
        self.W = len(self.links)
        self.s, self.Rp, self.Rm = ([], [], []) if self.W == 0 else self._poles()
    def C(self, z):
        W = self.W; Cm = np.zeros((2 * W, 2 * W), dtype=complex)
        for j in range(W):          # H[u,l] += -(z-1), H[l,u] += -(1/z-1)   (basis order: l_j, u_j)
            Cm[2 * j + 1, 2 * j] = -(z - 1); Cm[2 * j, 2 * j + 1] = -(1 / z - 1)
        return Cm
    def K(self, a):
        z = np.exp(2j * np.pi * a); Cm = self.C(z)
        return Cm @ np.linalg.inv(np.eye(2 * self.W) + self.M @ Cm)
    def G(self, a):
        if self.W == 0: return self.G0.astype(complex)
        return self.G0 - self.A @ self.K(a) @ self.A.T
    def _poles(self):
        """poles: det(I + M C(z)) = 0 with C(z) = z C1 + C0 + C-1/z  ->  quadratic eigenproblem
        z^2 (M C1) + z (I + M C0) + M C-1 = 0, linearised (4W x 4W generalised eig; rank deficiency -> infinite eigenvalues).
        Keep real positive z < 1 whose reciprocal is also an eigenvalue; merge clusters; contour radius from pole spacing."""
        import scipy.linalg as sla
        W = self.W; n2 = 2 * W
        C1 = np.zeros((n2, n2)); C0 = np.zeros((n2, n2)); Cm = np.zeros((n2, n2))
        for j in range(W):
            C1[2 * j + 1, 2 * j] = -1; C0[2 * j + 1, 2 * j] = 1      # -(z - 1)
            Cm[2 * j, 2 * j + 1] = -1; C0[2 * j, 2 * j + 1] = 1      # -(1/z - 1)
        A2, A1, A0 = self.M @ C1, np.eye(n2) + self.M @ C0, self.M @ Cm
        Z = np.zeros((n2, n2)); I = np.eye(n2)
        ev = sla.eig(np.block([[Z, I], [-A0, -A1]]), np.block([[I, Z], [Z, A2]]), right=False)
        ev = ev[np.isfinite(ev)]
        cand = [z.real for z in ev if abs(z.imag) < 1e-8 * abs(z) and 0 < z.real < 1 and np.min(np.abs(ev * z - 1)) < 1e-6]
        cand.sort(reverse=True); merged = []
        for z in cand:
            if not merged or abs(z - merged[-1]) > 1e-7 * z: merged.append(z)
        if not merged: return [], [], []                               # e.g. a wall-to-wall (pure-gauge) cut: no poles
        s = [-np.log(z) / (2 * np.pi) for z in merged]
        rads = [min(1e-6, 0.3 * min([abs(si - sj) for sj in s if sj != si] + [1.0])) for si in s]
        Rp = [self.residue_K(1j * sj, rad=r) for sj, r in zip(s, rads)]; Rm = [self.residue_K(-1j * sj, rad=r) for sj, r in zip(s, rads)]
        return s, Rp, Rm
    def Rfull(self, RK):
        return -(self.A @ RK @ self.A.T)
    def residue_K(self, a0, rad=1e-6, M=32):
        th = 2 * np.pi * np.arange(M) / M
        RK = sum(self.K(a0 + rad * np.exp(1j * t)) * (rad * np.exp(1j * t)) for t in th) / M
        return RK                                            # store Res K (2W x 2W); Res G = -A (Res K) A^T on demand

class Strip3D:
    def __init__(self, Lx, Lt, Ny, cutx, tcut, s_cut=np.inf, drop_double=False):
        self.Lx, self.Lt, self.Ny, self.cutx, self.tcut = Lx, Lt, Ny, list(cutx), tcut
        self.s_cut, self.drop_double = s_cut, drop_double
        idx = lambda x, t: x * Lt + t
        self.sl = [Slice(Lx, Lt, 2 - 2 * np.cos(2 * np.pi * p / Ny), cutx, tcut, idx) for p in range(Ny)]
        self.N = Lx * Lt

    # ---- memory-lean helpers: (Ny, N, N) arrays, row-blocked FFT convolution over the slice index ----
    def Garr(self, a, out=None):
        out = np.empty((self.Ny, self.N, self.N), dtype=complex) if out is None else out
        for p, s in enumerate(self.sl): out[p] = s.G(a)
        return out
    def conv_into(self, acc, Fa, Fb, coef, rb=48):
        """acc[k] += coef * sum_p Fa[p] o Fb[(k-p) % Ny], in row blocks (small temporaries)."""
        for r0 in range(0, self.N, rb):
            r1 = min(self.N, r0 + rb)
            fa = np.fft.fft(Fa[:, r0:r1, :], axis=0); fa *= np.fft.fft(Fb[:, r0:r1, :], axis=0)
            acc[:, r0:r1, :] += coef * np.fft.ifft(fa, axis=0)
    def conv(self, Fa, Fb):                          # small-size convenience (pre-checks); list in, list out
        Fa = np.asarray(Fa); Fb = np.asarray(Fb); acc = np.zeros_like(Fa, dtype=complex)
        self.conv_into(acc, Fa, Fb, 1.0); return list(acc)
    def B1(self):
        G0 = np.array([s.G0 for s in self.sl], dtype=complex); acc = np.zeros_like(G0)
        self.conv_into(acc, G0, G0, 2.0 / self.Ny); return acc
    def inner(self, n, beta, npt=40):
        """continued B_{n,k}^(beta), all k, as an (Ny, N, N) array (0 < Re beta < 1)."""
        Ny = self.Ny; x, w = leggauss(npt); u = 0.5 * (x + 1); wu = 0.5 * w
        acc = np.zeros((Ny, self.N, self.N), dtype=complex)
        Fa = np.empty_like(acc); Fb = np.empty_like(acc)
        for ui, wi in zip(u, wu):
            for a1, a2, ww in ((ui * beta, (1 - ui) * beta, wi * beta), (beta + ui * (1 - beta), 1 - ui * (1 - beta), wi * (1 - beta))):
                self.Garr(a1, Fa); self.Garr(a2, Fb); self.conv_into(acc, Fa, Fb, 2 * ww)
        Gm, Gp = Fa, Fb                                   # reuse buffers for the tail partners
        for p, sp in enumerate(self.sl):
            for j, sj in enumerate(sp.s):
                if sj > self.s_cut: continue
                f = 2j * np.pi / np.expm1(2 * np.pi * n * sj)
                self.Garr(beta - 1j * sj, Gm); self.Garr(beta + 1j * sj, Gp)
                Rp_, Rm_ = sp.Rfull(sp.Rp[j]), sp.Rfull(sp.Rm[j])
                for k in range(Ny):                       # first-factor + anchored second-factor tails (equal): 2 x 2
                    q = (k - p) % Ny
                    acc[k] += 4 * f * (Rp_ * Gm[q] - Rm_ * Gp[q])
                del Rp_, Rm_
        acc /= Ny; return acc
    def inner_beta0(self, n, npt=64, rad=1e-5, M=32, dn=False):
        """continued B_{n,k}^(0) (or its n-derivative if dn), all k, as an (Ny, N, N) array."""
        Ny, N = self.Ny, self.N
        acc = np.zeros((Ny, N, N), dtype=complex)
        if not dn:
            Fa = np.empty_like(acc); Fb = np.empty_like(acc)
            for a in np.arange(npt) / npt:
                self.Garr(a, Fa); self.Garr(-a, Fb); self.conv_into(acc, Fa, Fb, 2.0 / npt)
            del Fa, Fb
        def ker(al, up):
            if not dn: return 1.0 / np.expm1(-2j * np.pi * n * al) if up else -1.0 / np.expm1(2j * np.pi * n * al)
            e = np.exp(-2j * np.pi * n * al) if up else np.exp(2j * np.pi * n * al)
            return 2j * np.pi * al * e / (e - 1) ** 2
        th = 2 * np.pi * np.arange(M) / M
        for k in range(Ny):
            for p in range(Ny):
                q = (k - p) % Ny; sa, sb = self.sl[p], self.sl[q]
                locs = [(a0, "a") for sj in sa.s if sj <= self.s_cut for a0 in (1j * sj, -1j * sj)] + \
                       [(a0, "b") for sj in sb.s if sj <= self.s_cut for a0 in (-1j * sj, 1j * sj)]
                merged = []
                for a0, tag in locs:
                    hit = [m for m in merged if abs(m[0] - a0) < 1e-9]
                    if hit: hit[0][1].add(tag)
                    else: merged.append([a0, {tag}])
                for a0, tags in merged:
                    up = a0.imag > 0
                    if len(tags) == 2:
                        if self.drop_double: continue            # planted break (EXP-081 must-fire)
                        tot = 0
                        for t in th:
                            dz = rad * np.exp(1j * t); al = a0 + dz
                            tot = tot + 2 * sa.G(al) * sb.G(-al) * ker(al, up) * dz
                        acc[k] += (2j * np.pi) * tot / M
                    elif "a" in tags:
                        j = int(np.argmin([abs(abs(a0.imag) - sj) for sj in sa.s]))
                        acc[k] += (2j * np.pi) * 2 * sa.Rfull(sa.Rp[j] if up else sa.Rm[j]) * sb.G(-a0) * ker(a0, up)
                    else:
                        j = int(np.argmin([abs(abs(a0.imag) - sj) for sj in sb.s]))
                        R = sb.Rfull(sb.Rp[j] if (-a0).imag > 0 else sb.Rm[j])
                        acc[k] += (2j * np.pi) * 2 * sa.G(a0) * (-R) * ker(a0, up)
        acc /= Ny; return acc

def logdet(Mx):
    s, ld = np.linalg.slogdet(Mx); return ld + np.log(s + 0j)

def C_line(g, nseg=(0.0, 0.5, 1.5, 3.0, 6.0), npt=16):
    x, w = leggauss(npt); tot = 0.0
    for lo, hi in zip(nseg[:-1], nseg[1:]):
        for xi, wi in zip(x, w):
            si = 0.5 * (hi - lo) * (xi + 1) + lo
            tot = tot + 0.5 * (hi - lo) * wi * np.pi / np.cosh(np.pi * si) ** 2 * g(0.5 + 1j * si)
    return tot

def route_i(S, npt=40, cpts=16, smax=6.0):
    npt = getattr(S, 'npt', npt)
    """Q'(1) = sum_k [ Tr(B1k^{-1} d_n B^(0)_{n,k}|_1) + C[ logdet B_{1,k}^(beta) - logdet B1k ] ]  (per-k pieces returned too)."""
    B1 = S.B1(); ld1 = [logdet(B1[k]) for k in range(S.Ny)]
    dB0 = S.inner_beta0(1.0, dn=True)
    t0 = [np.trace(np.linalg.solve(B1[k], dB0[k])) for k in range(S.Ny)]
    cache = {}
    def gk(beta):
        if beta not in cache:
            Bb = S.inner(1.0, beta, npt); cache[beta] = [logdet(Bb[k]) - ld1[k] for k in range(S.Ny)]; del Bb
        return np.array(cache[beta])
    segs = (0.0, 0.5, 1.5, 3.0, smax)
    Cg = C_line(gk, nseg=segs, npt=cpts)
    return np.sum(t0) + np.sum(Cg), np.array(t0), Cg

def honest_slices(S, n):
    """honest integer-n: sum_k [ sum_q logdet (2/(n Ny)) sum_{p,k'} G_p(k'/n) o G_{k-p}((q-k')/n) - n logdet B1k ]."""
    Ny = S.Ny; B1 = S.B1(); tot = 0
    Gs = [[s.G(kk / n) for kk in range(n)] for s in S.sl]
    for q in range(n):
        F = {}
        for kk in range(n):
            c = S.conv([Gs[p][kk] for p in range(Ny)], [Gs[p][(q - kk) % n] for p in range(Ny)])
            for k in range(Ny): F[k] = F.get(k, 0) + c[k]
        for k in range(Ny): tot += logdet((2.0 / (n * Ny)) * F[k])
    return tot - n * sum(logdet(B1[k]) for k in range(Ny))

def honest_3d_replica(Lx, Lt, Ny, cutx, tcut, n):
    """direct: n sheets of the 3D lattice glued across the cut (all y); logdet(2 G o G) - n logdet at n=1."""
    N3 = Lx * Lt * Ny
    def H(nn):
        M = np.zeros((nn * N3, nn * N3)); I = lambda sh, x, t, y: sh * N3 + (x * Lt + t) * Ny + y
        for sh in range(nn):
            for x in range(Lx):
                for t in range(Lt):
                    for y in range(Ny):
                        i = I(sh, x, t, y); M[i, i] = 6.0
                        if x + 1 < Lx: j = I(sh, x + 1, t, y); M[i, j] = M[j, i] = -1.0
                        j = I(sh, x, t, (y + 1) % Ny); M[i, j] -= 1.0; M[j, i] -= 1.0
                        if t + 1 < Lt:
                            sh2 = (sh + 1) % nn if (t == tcut and x in cutx) else sh
                            j = I(sh2, x, t + 1, y); M[i, j] = M[j, i] = -1.0
        return M
    def ld(nn):
        G = np.linalg.inv(H(nn)); return logdet(2 * G * G)
    return (ld(n) - n * ld(1)).real

def free_gk(S, beta):
    """free twisted log det per slice: logdet H_k(z) - logdet H_k(1) = logdet(I + M_k C_k(z)), z = e^{2 pi i beta}."""
    z = np.exp(2j * np.pi * beta)
    return np.array([logdet(np.eye(2 * s.W) + s.M @ s.C(z)) if s.W else 0.0 for s in S.sl])

def free_S(S, cpts=16, smax=6.0):
    """free entropy per real scalar on the lattice strip: S = 1/2 C[ sum_k logdet H_k^(beta) - logdet H_k ] (no inner sum,
    q = 0 sector untwisted). Same outer continuation as the sigma side."""
    return 0.5 * np.sum(C_line(lambda b: free_gk(S, b), nseg=(0.0, 0.5, 1.5, 3.0, smax), npt=cpts))

class FreeStrip:
    """memory-light free side: per slice only M = P^T G0 P via sparse LU (2W right-hand sides); same geometry/conventions."""
    def __init__(self, Lx, Lt, Ny, cutx, tcut):
        import scipy.sparse as sp, scipy.sparse.linalg as spla
        self.Ny = Ny; idx = lambda x, t: x * Lt + t; N = Lx * Lt
        links = [(idx(x, tcut), idx(x, tcut + 1)) for x in cutx]; sites = [s for lu in links for s in lu]
        self.W = len(links); self.Ms = []
        rows, cols, vals = [], [], []
        for x in range(Lx):
            for t in range(Lt):
                i = idx(x, t)
                if x + 1 < Lx: j = idx(x + 1, t); rows += [i, j]; cols += [j, i]; vals += [-1.0, -1.0]
                if t + 1 < Lt: j = idx(x, t + 1); rows += [i, j]; cols += [j, i]; vals += [-1.0, -1.0]
        Hoff = sp.csc_matrix((vals, (rows, cols)), shape=(N, N))
        E = np.zeros((N, len(sites))); E[sites, np.arange(len(sites))] = 1
        for p in range(Ny):
            m2 = 2 - 2 * np.cos(2 * np.pi * p / Ny)
            X = spla.splu((Hoff + sp.identity(N) * (4.0 + m2)).tocsc()).solve(E)
            self.Ms.append(X[sites, :])
    def C(self, z):
        W = self.W; Cm = np.zeros((2 * W, 2 * W), dtype=complex)
        for j in range(W): Cm[2 * j + 1, 2 * j] = -(z - 1); Cm[2 * j, 2 * j + 1] = -(1 / z - 1)
        return Cm
    def gk(self, beta):
        z = np.exp(2j * np.pi * beta); Cm = self.C(z)
        return np.array([logdet(np.eye(2 * self.W) + M @ Cm) for M in self.Ms])
    def S(self, cpts=16, smax=6.0):
        return 0.5 * np.sum(C_line(self.gk, nseg=(0.0, 0.5, 1.5, 3.0, smax), npt=cpts))

class FreeStripK(FreeStrip):
    """free side at L = infinity: per-slice masses at Gauss nodes k in (-pi, pi) (lattice dispersion 2 - 2 cos k),
    S/L = int dk/2pi s(k). Nodes clustered near k = 0 (substitution k = pi * u^3 on u in (-1, 1))."""
    def __init__(self, Lx, Lt, cutx, tcut, nk=48):
        import scipy.sparse as sp, scipy.sparse.linalg as spla
        idx = lambda x, t: x * Lt + t; N = Lx * Lt
        links = [(idx(x, tcut), idx(x, tcut + 1)) for x in cutx]; sites = [s for lu in links for s in lu]
        self.W = len(links); self.Ms = []
        rows, cols, vals = [], [], []
        for x in range(Lx):
            for t in range(Lt):
                i = idx(x, t)
                if x + 1 < Lx: j = idx(x + 1, t); rows += [i, j]; cols += [j, i]; vals += [-1.0, -1.0]
                if t + 1 < Lt: j = idx(x, t + 1); rows += [i, j]; cols += [j, i]; vals += [-1.0, -1.0]
        Hoff = sp.csc_matrix((vals, (rows, cols)), shape=(N, N))
        E = np.zeros((N, len(sites))); E[sites, np.arange(len(sites))] = 1
        u, wu = leggauss(nk); u = 0.5 * (u + 1); wu = 0.5 * wu          # u in (0,1); k = pi u^3, even in k -> x2
        self.kw = []
        for ui, wi in zip(u, wu):
            k = np.pi * ui ** 3; dk = 3 * np.pi * ui ** 2 * wi
            X = spla.splu((Hoff + sp.identity(N) * (4.0 + 2 - 2 * np.cos(k))).tocsc()).solve(E)
            self.Ms.append(X[sites, :]); self.kw.append(2 * dk / (2 * np.pi))
        self.kw = np.array(self.kw)
    def S_per_L(self, cpts=16, smax=6.0):
        return 0.5 * np.sum(self.kw * C_line(self.gk, nseg=(0.0, 0.5, 1.5, 3.0, smax), npt=cpts))

# ------------------------------------------------------------------ saddle term (EXP-081a) ------------------------------
def _kdn(al, up, n=1.0):
    e = np.exp(-2j * np.pi * n * al) if up else np.exp(2j * np.pi * n * al)
    return 2j * np.pi * al * e / (e - 1) ** 2

def coincident_dn(S):
    """d(x) = d/dn [ (1/n) sum_k DeltaG_3D^(k/n)(x,x) ] at n=1, DeltaG_3D(x,x) = (1/Ny) sum_q [G_q^(a) - G0_q](x,x).
    Single-factor Poisson continuation: only the pole tails depend on n; residue diagonals from the 2W x 2W Res K."""
    d = np.zeros(S.N, dtype=complex)
    for sp in S.sl:
        for j, sj in enumerate(sp.s):
            if sj > S.s_cut: continue
            for RK, a0, up in ((sp.Rp[j], 1j * sj, True), (sp.Rm[j], -1j * sj, False)):
                diagR = -np.sum((sp.A @ RK) * sp.A, axis=1)                  # diag(-A RK A^T)
                d += (2j * np.pi) * diagR * (_kdn(a0, up) if up else _kdn(a0, up))
    return d / S.Ny

def saddle_term(S, B1=None, return_checks=False):
    """T_saddle = sum_k Tr(B1k^{-1} dB_k^sad),  dB_k^sad = -(4/Ny) sum_q G0_q o (G0_{k-q} D G0_{k-q}),  D = diag(sigdot),
    sigdot = 2 B1_{k=0}^{-1} d  (gap equation at O(n-1), y-independent saddle)."""
    B1 = S.B1() if B1 is None else B1
    d = coincident_dn(S); sig = np.linalg.solve(B1[0], 2 * d)
    G0 = np.array([s.G0 for s in S.sl], dtype=complex)
    H = np.array([g @ (sig[:, None] * g) for g in G0])                          # G0_q D G0_q
    gapcheck = np.max(np.abs(np.mean([np.diag(h) for h in H], axis=0) - d)) / max(np.max(np.abs(d)), 1e-300)
    acc = np.zeros_like(G0); S.conv_into(acc, G0, H, -4.0 / S.Ny); del H, G0
    T = sum(np.trace(np.linalg.solve(B1[k], acc[k])) for k in range(S.Ny))
    return (T, d, sig, gapcheck) if return_checks else T

def route_i_ckpt(S, ckpt, cpts=12, smax=6.0, npt=40, with_saddle=True):
    """route (i) with the saddle term and per-beta checkpointing (json at `ckpt`): Q'(1) = sum_k t0_k + T_saddle + C[g]."""
    import json, os
    st = json.load(open(ckpt)) if os.path.exists(ckpt) else {}
    def put(k, v):
        st[k] = v; tmp = ckpt + ".tmp"; json.dump(st, open(tmp, "w")); os.replace(tmp, ckpt)
    B1 = S.B1(); ld1 = [logdet(B1[k]) for k in range(S.Ny)]
    if "t0" not in st:
        dB0 = S.inner_beta0(1.0, dn=True)
        put("t0", float(sum(np.trace(np.linalg.solve(B1[k], dB0[k])) for k in range(S.Ny)).real)); del dB0
    if with_saddle and "tsad" not in st:
        put("tsad", float(saddle_term(S, B1).real))
    x, w = leggauss(cpts); tot = 0.0
    for lo, hi in zip((0.0, 0.5, 1.5, 3.0), (0.5, 1.5, 3.0, smax)):
        for xi, wi in zip(x, w):
            si = 0.5 * (hi - lo) * (xi + 1) + lo; key = f"g|{si:.15f}"
            if key not in st:
                Bb = S.inner(1.0, 0.5 + 1j * si, npt)
                put(key, float(sum((logdet(Bb[k]) - ld1[k]).real for k in range(S.Ny)))); del Bb
            tot += 0.5 * (hi - lo) * wi * np.pi / np.cosh(np.pi * si) ** 2 * st[key]
    return st["t0"] + (st.get("tsad", 0.0) if with_saddle else 0.0) + tot, st
