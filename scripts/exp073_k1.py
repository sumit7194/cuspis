"""EXP-073(b): test of Neon T31's K1 claim (UNVERIFIED source): for the FREE twisted 2D Helmholtz operator (one transverse
slice, mass m = |k|), the two-edge connected log det
    D2 = log det H_can - log det H(1) - log det H(2) + log det H_1 = log det(I - K_free),
    K_free = G(1) T1 G(2) T2        (TGTG form; exact algebra for finite matrices, derived in report EXP-073(b) spec),
has nonzero spectrum equal to that of the CFH operator lam^2 R R^T (theta = 2a-1, lam^2 = sin^2(pi a)/pi^2, t = m w).
Instrument: square lattice, spacing 1, H = (4 + (m a)^2) - hopping; twist by link phases on vertical links between rows j0 and
j0+1. Canonical exterior gauge: phase e^{-2 pi i a} on rays (-inf, edge1] and [edge2, inf) (gauge-equivalent to e^{+2 pi i a}
on the interior segment, a control below). Dirichlet box. Strip width w = i2 - i1 - 1 lattice units.
Independent side: the continuum CFH Fredholm operator from exp044_det conventions (Nystrom, p-grid, weight h).
[model: Opus 5.5]"""
import sys, math, time, os
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

def lattice(W, t, pad_over_m, a, which, D=None):
    """Return dict with sparse H for which in {'flat','e1','e2','can','int'} plus geometry. m*a_lat = t/W. (vectorised build)"""
    ma = t / W
    pad = int(math.ceil(pad_over_m / ma))
    Nx = W + 1 + 2 * pad; Ny = 2 * pad
    j0 = pad - 1
    i1 = pad - 1; i2 = i1 + W + 1          # interior untwisted links i1 < i < i2 ; edges at i1+1/2, i2-1/2
    N = Nx * Ny
    idx = lambda i, j: i * Ny + j
    ph = np.exp(-2j * np.pi * a)           # exterior-gauge phase
    I, J = np.meshgrid(np.arange(Nx), np.arange(Ny), indexing="ij"); S = I * Ny + J
    rows = [S.ravel()]; cols = [S.ravel()]; vals = [np.full(N, 4.0 + ma * ma, complex)]
    a_ = S[:-1, :].ravel(); b_ = S[1:, :].ravel()                     # horizontal links
    rows += [a_, b_]; cols += [b_, a_]; vals += [np.full(a_.size, -1.0, complex)] * 2
    lo = S[:, :-1]; hi = S[:, 1:]; f = np.ones(lo.shape, complex)      # vertical links (j -> j+1)
    xi = np.arange(Nx); on1 = xi <= i1; on2 = xi >= i2; inside = (xi > i1) & (xi < i2)
    if which == 'can': f[on1 | on2, j0] = ph
    elif which == 'e1': f[on1, j0] = ph
    elif which == 'e2': f[on2, j0] = ph
    elif which == 'int': f[inside, j0] = np.exp(2j * np.pi * a)
    # hopping up (j -> j+1) carries f, down carries 1/f  (gauge map U H U^{-1}, valid for complex a)
    rows += [hi.ravel(), lo.ravel()]; cols += [lo.ravel(), hi.ravel()]; vals += [-f.ravel(), -1.0 / f.ravel()]
    H = sp.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(N, N))
    return dict(H=H, Nx=Nx, Ny=Ny, j0=j0, i1=i1, i2=i2, idx=idx, ma=ma, pad=pad)

def ray_support(g, ray, D):
    """sites touching twisted links of ray (1 or 2) within D lattice units of its edge; ordered list of indices."""
    idx, j0 = g['idx'], g['j0']
    if ray == 1:
        xs = [i for i in range(g['Nx']) if i <= g['i1'] and g['i1'] - i < D]
    else:
        xs = [i for i in range(g['Nx']) if i >= g['i2'] and i - g['i2'] < D]
    return np.array([idx(i, j) for i in xs for j in (j0, j0 + 1)])

def logdet_lu(H):
    lu = spla.splu(H.tocsc(), permc_spec="COLAMD")
    d = lu.U.diagonal()
    def parity(p):
        p = np.array(p); seen = np.zeros(len(p), bool); par = 0
        for k in range(len(p)):
            if not seen[k]:
                c = 0; q = k
                while not seen[q]:
                    seen[q] = True; q = p[q]; c += 1
                par += c - 1
        return par % 2
    sgn = (-1) ** (parity(lu.perm_r) + parity(lu.perm_c))
    return np.sum(np.log(d.astype(complex))) + (0j if sgn > 0 else 1j * np.pi), lu

def Kfree(W, t, a, pad_over_m=8.0, D_over_m=8.0, perm="MMD_AT_PLUS_A"):
    """small matrix whose spectrum = nonzero spectrum of K_free = G(1)T1 G(2)T2 (supports truncated at D).
    Memory-lean: one lattice / one LU alive at a time."""
    import gc
    g = lattice(W, t, pad_over_m, a, 'flat'); Hf = g['H']; D = int(math.ceil(D_over_m / g['ma']))
    P1 = ray_support(g, 1, D); P2 = ray_support(g, 2, D); N = Hf.shape[0]
    def block_solve(lu, src, keep, chunk=16):   # columns G[keep, src] in chunks (memory: N x chunk)
        out = np.empty((len(keep), len(src)), complex)
        for c0 in range(0, len(src), chunk):
            cs = src[c0:c0 + chunk]; E = np.zeros((N, len(cs)), complex); E[cs, np.arange(len(cs))] = 1
            out[:, c0:c0 + len(cs)] = lu.solve(E)[keep]
        return out
    H1 = lattice(W, t, pad_over_m, a, 'e1')['H']; T1 = (H1 - Hf)[P1][:, P1].toarray()
    lu = spla.splu(H1, permc_spec=perm); del H1; G1_P2P1 = block_solve(lu, P1, P2); del lu; gc.collect()
    H2 = lattice(W, t, pad_over_m, a, 'e2')['H']; T2 = (H2 - Hf)[P2][:, P2].toarray()
    lu = spla.splu(H2, permc_spec=perm); del H2; G2_P1P2 = block_solve(lu, P2, P1); del lu; gc.collect()
    Ks = T2 @ G1_P2P1 @ T1 @ G2_P1P2      # spectrum = nonzero spec of G(1)T1G(2)T2 (cyclic)
    return Ks, dict(N=N, P=len(P1), D=D, pad=g['pad'])

def D2_direct(W, t, a, pad_over_m=8.0):
    """two-edge connected log det from four LU determinants (no truncation), plus the interior-gauge value."""
    L = {k: logdet_lu(lattice(W, t, pad_over_m, a, k)['H'])[0] for k in ('flat', 'e1', 'e2', 'can', 'int')}
    return L['can'] - L['e1'] - L['e2'] + L['flat'], L['int'] - L['can']

def cfh_eigs(t, a, h=0.1, P=None, scale_t=1.0, scale_lam=1.0):
    t = t * scale_t
    if P is None:
        P = math.acosh(max(2.0, 90.0 / t))
    p = np.arange(-P, P + 0.5 * h, h); th = 2 * a - 1
    E = np.exp(-0.5 * t * np.cosh(p)); dp = p[:, None] - p[None, :]
    R = np.exp(0.5 * th * dp) * (E[:, None] * E[None, :]) / (2 * np.cosh(0.5 * dp))
    lam2 = scale_lam * np.sin(np.pi * a) ** 2 / np.pi ** 2
    ev = np.linalg.eigvals(lam2 * h * h * (R @ R.T))
    return ev[np.argsort(-np.abs(ev))]

def top(ev, k=3):
    ev = np.asarray(ev); return ev[np.argsort(-np.abs(ev))][:k]

def pressure_guard(min_free_pct=40, wait_s=60, max_wait_s=3600):
    """Fleet rule: before each heavy step, wait until macOS memory_pressure reports >= min_free_pct free. [model: Opus 5.5]"""
    import subprocess, re, time
    waited = 0
    while True:
        try:
            out = subprocess.run(["memory_pressure"], capture_output=True, text=True, timeout=30).stdout
            free = int(re.search(r"free percentage:\s*(\d+)%", out).group(1))
        except Exception:
            free = 100
        if free >= min_free_pct:
            return free
        if waited >= max_wait_s:
            raise SystemExit(f"pressure_guard: free {free}% < {min_free_pct}% for {waited}s; stopping (resume later)")
        print(f"pressure_guard: free {free}% < {min_free_pct}%, waiting {wait_s}s", flush=True)
        time.sleep(wait_s); waited += wait_s
