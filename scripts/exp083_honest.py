"""EXP-083 (registered cd9e134): honest integer-n replica data for the 081b strip family, own poles, fits.
Lattice per sheet: Lx = 2P + 4, Lt = 2P, index x*Lt + t (as production); y-slices p = 0..Ny-1, m2_p = 2 - 2 cos(2 pi p/Ny),
H_p = (4 + m2_p) I - adjacency (Dirichlet box); cut links (x, tcut) -> (x, tcut + 1), x in [x0, x0 + W), tcut = P - 1.
n-sheet manifold: link l on sheet s joined to u on sheet s + 1 (mod n). B_n^(k) = (2/Ny) sum_p G_p o G_{k-p} (Hadamard, nN x nN).
Arm (a): Q(n) = sum_k [log det B_n^(k) - n log det B_1^(k)], sigma = 0.
Arm (b): the same at the honest replica saddle sigma_n (sheet-symmetric, y-independent): (1/Ny) sum_p G_p^(n)[sigma](x,x) =
         (1/Ny) sum_p G_p^(1)(x,x) on sheet 0, by Newton (Jacobian -(1/Ny) sum_p sum_s' G(x_0, y_s')^2).
Own poles (independent of production's QEP): per slice, sign changes of F(s) = z^W det H_p(alpha = i s), z = e^{-2 pi s},
on a 1e-3 grid over (0, s_scan], refined by brentq; near-touch minima rescanned at 1e-6. [model: Opus 5.5]"""
import numpy as np
from scipy.optimize import brentq

class Geom:
    def __init__(self, W, P, Wbox=4, c=2, cut="strip"):
        self.Lx, self.Lt, self.Ny, self.W, self.P = 2 * P + Wbox, 2 * P, int(c * 2 * P), W, P
        self.N = self.Lx * self.Lt; x0 = P + (Wbox - W) // 2; self.tcut = P - 1
        self.cutx = list(range(x0, x0 + W)) if cut == "strip" else list(range(self.Lx))     # "wall": pure gauge
        idx = lambda x, t: x * self.Lt + t
        self.links = [(idx(x, self.tcut), idx(x, self.tcut + 1)) for x in self.cutx]
        A = np.zeros((self.N, self.N))
        for x in range(self.Lx):
            for t in range(self.Lt):
                i = idx(x, t)
                if x + 1 < self.Lx: j = idx(x + 1, t); A[i, j] = A[j, i] = 1.0
                if t + 1 < self.Lt: j = idx(x, t + 1); A[i, j] = A[j, i] = 1.0
        self.A = A
    def m2(self, p): return 2 - 2 * np.cos(2 * np.pi * p / self.Ny)
    def Hn(self, p, n, sigma=None):
        N = self.N; base = np.diag(np.full(N, 4.0 + self.m2(p)) + (0 if sigma is None else sigma)) - self.A
        H = np.zeros((n * N, n * N))
        for s in range(n): H[s*N:(s+1)*N, s*N:(s+1)*N] = base
        for (l, u) in self.links:
            for s in range(n):
                H[s*N + l, s*N + u] = 0.0; H[s*N + u, s*N + l] = 0.0
            for s in range(n):
                a, b = s * N + l, ((s + 1) % n) * N + u; H[a, b] = -1.0; H[b, a] = -1.0
        return H
    def Gn(self, n, sigma=None):
        U = {}
        for p in range(self.Ny // 2 + 1): U[p] = np.linalg.inv(self.Hn(p, n, sigma))
        return [U[p if p <= self.Ny // 2 else self.Ny - p] for p in range(self.Ny)]
    def logdetB(self, G):
        Ny = self.Ny; tot = 0.0
        for k in range(Ny):
            B = sum(G[p] * G[(k - p) % Ny] for p in range(Ny)) * (2.0 / Ny); s, ld = np.linalg.slogdet(B)
            if s <= 0: raise RuntimeError(f"non-positive det at k={k}")
            tot += ld
        return tot
    def saddle(self, n, tol=1e-13, itmax=30):
        N, Ny = self.N, self.Ny; G1 = self.Gn(1); target = sum(np.diag(g) for g in G1) / Ny; sig = np.zeros(N)
        for it in range(itmax):
            G = self.Gn(n, sig); F = sum(np.diag(g)[:N] for g in G) / Ny - target
            if np.abs(F).max() < tol: return sig, it
            J = np.zeros((N, N))
            for g in G:
                for s in range(n): J -= g[:N, s*N:(s+1)*N] ** 2
            J /= Ny; sig = sig - np.linalg.solve(J, F)
        raise RuntimeError(f"saddle Newton did not converge (n={n}, |F|={np.abs(F).max():.1e})")
    def Q(self, n, saddle=False, ld1=None):
        sig = None
        if saddle and n > 1: sig, _ = self.saddle(n)
        ldn = self.logdetB(self.Gn(n, sig)); ld1 = self.logdetB(self.Gn(1)) if ld1 is None else ld1
        return ldn - n * ld1
    def own_poles(self, p, s_scan=4.5, step=1e-3):
        N, W = self.N, len(self.links); base = np.diag(np.full(N, 4.0 + self.m2(p))) - self.A
        def F(s):
            z = np.exp(-2 * np.pi * s); H = base.copy()
            for (l, u) in self.links: H[u, l] = -z; H[l, u] = -1.0 / z
            sg, ld = np.linalg.slogdet(H); return sg * np.exp(ld + W * np.log(z) - self._ref)
        self._ref = 0.0; self._ref = np.linalg.slogdet(base)[1]
        g = np.arange(1, int(s_scan / step) + 1) * step; v = np.array([F(x) for x in g]); roots = []
        for i in range(len(g) - 1):
            if v[i] == 0: roots.append(g[i])
            elif v[i] * v[i + 1] < 0: roots.append(brentq(F, g[i], g[i + 1], xtol=1e-14))
        av = np.abs(v)
        for i in range(1, len(g) - 1):                              # near-touch minima: rescan finely
            if av[i] < av[i - 1] and av[i] < av[i + 1] and not any(abs(r - g[i]) < 2 * step for r in roots):
                gg = np.linspace(g[i - 1], g[i + 1], 2001); vv = np.array([F(x) for x in gg])
                roots += [brentq(F, gg[j], gg[j + 1], xtol=1e-14) for j in range(len(gg) - 1) if vv[j] * vv[j + 1] < 0]
        return sorted(roots)

def fit_Qprime(ns, Qs, bases, conf=(), nhold=1):
    """Q(n) = A n + B + sum_b C_b b^n + sum_c D_c n c^n; fit on all but the last nhold points; returns Q'(1), rms, held-out err."""
    ns = np.asarray(ns, float); Qs = np.asarray(Qs); tr = slice(0, len(ns) - nhold)
    cols = [ns, np.ones_like(ns)] + [b ** ns for b in bases] + [ns * c ** ns for c in conf]
    X = np.column_stack(cols); coef, *_ = np.linalg.lstsq(X[tr], Qs[tr], rcond=None)
    A = coef[0]; Cb = coef[2:2 + len(bases)]; Dc = coef[2 + len(bases):]
    qp = A + sum(C * b * np.log(b) for C, b in zip(Cb, bases)) + sum(D * c * (1 + np.log(c)) for D, c in zip(Dc, conf))
    rms = np.sqrt(np.mean((X[tr] @ coef - Qs[tr]) ** 2)); ho = np.abs(X[len(ns) - nhold:] @ coef - Qs[len(ns) - nhold:]).max() if nhold else 0.0
    return qp, rms, ho

def free_base_fit(ns, Qs, nb, nhold=1):
    """Matrix-pencil (Prony) on the second differences of Q (removes A n + B), nb exponentials; then linear refit."""
    ns = np.asarray(ns, float); Qs = np.asarray(Qs); m = len(ns) - nhold
    d2 = Qs[2:m] - 2 * Qs[1:m - 1] + Qs[:m - 2]; L = len(d2) // 2
    if L < nb: return None
    Y = np.array([d2[i:i + L + 1] for i in range(len(d2) - L)]); U, s, Vt = np.linalg.svd(Y, full_matrices=False)
    V = Vt[:nb].T; V1, V2 = V[:-1], V[1:]; z = np.linalg.eigvals(np.linalg.pinv(V1) @ V2)
    z = np.real(z[(np.abs(z.imag) < 1e-8 * np.abs(z)) & (z.real > 0) & (z.real < 1)])
    if len(z) == 0: return None
    return fit_Qprime(ns, Qs, list(z), nhold=nhold), list(z)
