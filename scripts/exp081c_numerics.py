"""EXP-081c numerics (registered 8fcfb84; draft d50f6de section 3). [model: Opus 5.5]

G(alpha) = direct inverse of the EXACT integer-stencil H(alpha) = (4 + m2) I - adjacency, with the cut links twisted
(H[u,l] = -z, H[l,u] = -1/z, z = exp(2 pi i alpha); same convention as EXP-081b production, here built directly rather than
as inv(G0) + correction). Then `refine` steps of iterative refinement (or "auto": until the relative correction <= 1e-15, max 8; registered fix after Step 0 run 1) G <- G + G R, R = I - H G, with the residual
evaluated in double-double arithmetic using the stencil structure (exact enough: every product is an error-free
TwoProd, every sum a TwoSum).
Residues: full N x N matrices, 32-point contour of the same G, radius min(1e-6, 0.3 x pole spacing) as in sigma3d._poles.
Slices p > Ny/2 are the same object as slice Ny - p (exact mirror symmetry).
Poles: production QEP (sigma3d.Slice._poles), census-gated separately.
"""
import numpy as np, sigma3d as S3

_SPLIT = 134217729.0                                          # 2^27 + 1 (Dekker)

def _two_sum(a, b):
    s = a + b; bb = s - a; return s, (a - (s - bb)) + (b - bb)

def _split(a):
    c = _SPLIT * a; h = c - (c - a); return h, a - h

def _two_prod(a, b):
    p = a * b; ah, al = _split(a); bh, bl = _split(b)
    return p, ((ah * bh - p) + ah * bl + al * bh) + al * bl

class _DD:
    """double-double accumulator on real arrays"""
    def __init__(self, shape): self.hi = np.zeros(shape); self.lo = np.zeros(shape)
    def add(self, p, e=None):
        self.hi, t = _two_sum(self.hi, p); self.lo = self.lo + t + (0.0 if e is None else e)

class ExactSlice:
    def __init__(self, base, Lx, Lt, m2, s_cut, refine=1, M=32):
        self.Lx, self.Lt, self.N, self.m2, self.d = Lx, Lt, Lx * Lt, m2, 4.0 + m2
        self.links, self.s, self.W, self.refine, self.M, self.scale = list(base.links), list(base.s), base.W, refine, M, 1.0
        self.G0 = base.G0                                      # B1 / saddle use G0 = inv(H0) (real, cond ~ 1e2)
        N = self.N; H0 = np.diag(np.full(N, self.d)); nb = []
        for x in range(Lx):
            for t in range(Lt):
                i = x * Lt + t
                for dx, dt in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if 0 <= x + dx < Lx and 0 <= t + dt < Lt: j = (x + dx) * Lt + (t + dt); H0[i, j] = -1.0; nb.append((i, j))
        self.H0 = H0; nb = np.array(nb); self.nb_i, self.nb_j = nb[:, 0], nb[:, 1]
        self.l = np.array([l for l, u in self.links]); self.u = np.array([u for l, u in self.links])
        tw = set(zip(self.u, self.l)) | set(zip(self.l, self.u))
        keep = np.array([(i, j) not in tw for i, j in zip(self.nb_i, self.nb_j)])
        self.ui_i, self.ui_j = self.nb_i[keep], self.nb_j[keep]    # untwisted hops (T = 1)
        self.s_cut = s_cut; self.Rp, self.Rm = [], []
        for j, sj in enumerate(self.s):
            if sj > s_cut: self.Rp.append(None); self.Rm.append(None); continue
            r = min(1e-6, 0.3 * min([abs(sj - sk) for sk in self.s if sk != sj] + [1.0]))
            self.Rp.append(self.residue(1j * sj, r)); self.Rm.append(self.residue(-1j * sj, r))

    def H(self, a):
        z = np.exp(2j * np.pi * a); H = self.H0.astype(complex)
        H[self.u, self.l] = -z; H[self.l, self.u] = -1.0 / z
        return H, z

    def residual(self, G, z):
        """R = I - H(alpha) G in double-double, from the stencil (rows of H G)."""
        N = self.N; out = []
        zu, zl = -z, -1.0 / z                                   # H[u,l], H[l,u]
        for part in ("re", "im"):
            acc = _DD((N, N)); Gr, Gi = G.real, G.imag
            # diagonal: d * G
            p, e = _two_prod(np.full((N, 1), self.d), Gr if part == "re" else Gi); acc.add(p, e)
            # untwisted hops: -G[j, :] added to row i (exact negation); accumulate row-wise
            src = Gr if part == "re" else Gi
            order = np.argsort(self.ui_i, kind="stable"); ii, jj = self.ui_i[order], self.ui_j[order]
            # each row has <= 4 untwisted neighbours: process neighbour slot k = 0..3
            starts = np.searchsorted(ii, np.arange(N)); counts = np.bincount(ii, minlength=N)
            for k in range(4):
                rows = np.nonzero(counts > k)[0]; js = jj[starts[rows] + k]
                term = np.zeros((N, N)); term[rows] = -src[js]
                acc.add(term)
            # twisted hops: row u gets zu * G[l], row l gets zl * G[u]  (complex products, error-free)
            for rows, srcrows, c in ((self.u, self.l, zu), (self.l, self.u, zl)):
                ar, ai = c.real, c.imag; br, bi = Gr[srcrows], Gi[srcrows]
                if part == "re": terms = [(_two_prod(np.full((len(rows), 1), ar), br), 1.0), (_two_prod(np.full((len(rows), 1), ai), bi), -1.0)]
                else: terms = [(_two_prod(np.full((len(rows), 1), ar), bi), 1.0), (_two_prod(np.full((len(rows), 1), ai), br), 1.0)]
                for (p, e), sg in terms:
                    P = np.zeros((N, N)); E = np.zeros((N, N)); P[rows] = sg * p; E[rows] = sg * e; acc.add(P, E)
            eye = np.eye(N) if part == "re" else np.zeros((N, N))
            s, e = _two_sum(eye, -acc.hi); out.append(s + (e - acc.lo))
        return out[0] + 1j * out[1]

    STATS = {"calls": 0, "steps": 0, "maxsteps": 0, "unconverged": 0}
    @staticmethod
    def reset_stats():
        ExactSlice.STATS.clear(); ExactSlice.STATS.update(calls=0, steps=0, maxsteps=0, unconverged=0, hist={}, bad=[])
    def G_raw(self, a, refine=None, extra=None):
        """refine: int = fixed number of steps; "auto" = iterate until max|G R|/max|G| <= 1e-15 (at most 8 steps), then
        `extra` further steps (default self.extra, 0)."""
        H, z = self.H(a); G = np.linalg.inv(H); mode = self.refine if refine is None else refine
        if mode != "auto":
            for _ in range(mode): G = G + G @ self.residual(G, z)
            return G
        st = ExactSlice.STATS; st["calls"] += 1; k = 0; prev = np.inf; conv = False
        for k in range(1, 9):
            dG = G @ self.residual(G, z); G = G + dG; c = np.abs(dG).max()
            if c <= 1e-15 * np.abs(G).max(): conv = True; break
            if c >= prev: break                                   # divergence guard (amendment R1)
            prev = c
        if not conv: st["unconverged"] += 1; st.setdefault("bad", []).append(complex(a))
        st["steps"] += k; st["maxsteps"] = max(st["maxsteps"], k); st.setdefault("hist", {}); st["hist"][k] = st["hist"].get(k, 0) + 1
        for _ in range(getattr(self, "extra", 0) if extra is None else extra): G = G + G @ self.residual(G, z)
        return G

    def G(self, a):
        # one-entry cache: mirror-aliased slices p and Ny-p are the same object and are called with the same alpha in one
        # Garr loop; the cached value is the identical computation (no numerical change)
        if getattr(self, "_ck", None) != a: self._ck, self._cv = a, self.G_raw(a)
        return self.scale * self._cv

    def residue(self, a0, r):
        th = 2 * np.pi * np.arange(self.M) / self.M
        return sum(self.G_raw(a0 + r * np.exp(1j * t)) * (r * np.exp(1j * t)) for t in th) / self.M

    def Rfull(self, R):
        return self.scale * R

def install(S, refine=1):
    """Replace S.sl by ExactSlice wrappers (mirror-aliased). Returns the list of unique wrappers (p <= Ny/2)."""
    Ny = S.Ny; uniq = {}
    for p in range(Ny // 2 + 1):
        uniq[p] = ExactSlice(S.sl[p], S.Lx, S.Lt, 2 - 2 * np.cos(2 * np.pi * p / Ny), S.s_cut, refine=refine)
    S.sl = [uniq[p if p <= Ny // 2 else Ny - p] for p in range(Ny)]
    return uniq

def coincident_dn_c(S):
    d = np.zeros(S.N, dtype=complex)
    for sp in S.sl:
        for j, sj in enumerate(sp.s):
            if sj > S.s_cut: continue
            for R, a0, up in ((sp.Rp[j], 1j * sj, True), (sp.Rm[j], -1j * sj, False)):
                d += (2j * np.pi) * np.diag(sp.Rfull(R)) * S3._kdn(a0, up)
    return d / S.Ny

def saddle_term_c(S, B1):
    d = coincident_dn_c(S); sig = np.linalg.solve(B1[0], 2 * d)
    G0 = np.array([s.G0 for s in S.sl], dtype=complex)
    H = np.array([g @ (sig[:, None] * g) for g in G0])
    acc = np.zeros_like(G0); S.conv_into(acc, G0, H, -4.0 / S.Ny); del H, G0
    return float(sum(np.trace(np.linalg.solve(B1[k], acc[k])) for k in range(S.Ny)).real)

def g_node(S, s, ld1, npt=40):
    Bb = S.inner(1.0, 0.5 + 1j * s, npt)
    return float(sum((S3.logdet(Bb[k]) - ld1[k]).real for k in range(S.Ny)))

def t0_term(S, B1):
    dB0 = S.inner_beta0(1.0, dn=True)
    return float(sum(np.trace(np.linalg.solve(B1[k], dB0[k])) for k in range(S.Ny)).real)
