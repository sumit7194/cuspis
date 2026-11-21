"""EXP-083 R2 (f5b9e71): honest Q(n) via the exact replica-sector decomposition (integer n, no continuation).
G_p(alpha): DIRECT inverse of the single-sheet twisted operator, H[u,l] = -e^{2 pi i alpha}, H[l,u] = -e^{-2 pi i alpha} on the cut
links (l = (x, tcut), u = (x, tcut + 1)); diag 4 + m2_p (+ sigma). Sector bubble B^(Q,k) = (2/(n Ny)) sum_{p,q} G_p(q/n) o G_{k-p}((Q-q)/n);
Q(n) = sum_{Q,k} log det B^(Q,k) - n sum_k log det B_1^(k). Saddle (arm b): sheet-symmetric sigma solving the gap equation with the
sheet-diagonal block (1/n) sum_q G(q/n) and Jacobian from the replica blocks G_(0,d) = (1/n) sum_q e^{-2 pi i q d/n} G(q/n).
Backend: numpy (float64) here; the high-precision backend is separate. [model: Opus 5.5]"""
import numpy as np
from exp083_honest import Geom

def Gtw(g, p, alpha, sigma=None):
    H = (np.diag(np.full(g.N, 4.0 + g.m2(p)) + (0 if sigma is None else sigma)) - g.A).astype(complex)
    z = np.exp(2j * np.pi * alpha)
    for (l, u) in g.links: H[u, l] = -z; H[l, u] = -1.0 / z
    return np.linalg.inv(H)

def sector_G(g, n, sigma=None):
    """G[p][q] for p <= Ny/2 (mirror-aliased later), q = 0..n-1."""
    return {p: [Gtw(g, p, q / n, sigma) for q in range(n)] for p in range(g.Ny // 2 + 1)}

def sector_logdet(g, n, Gs):
    Ny = g.Ny; get = lambda p: Gs[p if p <= Ny // 2 else Ny - p]; tot = 0.0
    for Qs in range(n):
        for k in range(Ny):
            B = sum(get(p)[q] * get((k - p) % Ny)[(Qs - q) % n] for p in range(Ny) for q in range(n)) * (2.0 / (n * Ny))
            s, ld = np.linalg.slogdet(B); tot += ld; PHASE[0] = max(PHASE[0], abs(np.angle(s)))
    return float(tot)
PHASE = [0.0]

def sector_saddle(g, n, tol=1e-13, itmax=40, sig0=None):
    N, Ny = g.N, g.Ny; G1 = sector_G(g, 1); get1 = lambda p: G1[p if p <= Ny // 2 else Ny - p][0]
    target = sum(np.diag(get1(p)).real for p in range(Ny)) / Ny; sig = np.zeros(N) if sig0 is None else sig0.copy()
    for it in range(itmax):
        Gs = sector_G(g, n, sig); get = lambda p: Gs[p if p <= Ny // 2 else Ny - p]
        F = sum(np.diag(sum(get(p)) / n).real for p in range(Ny)) / Ny - target
        if np.abs(F).max() < tol: return sig, Gs, it
        J = np.zeros((N, N))
        for p in range(Ny):
            for d in range(n):
                Gd = sum(np.exp(-2j * np.pi * q * d / n) * get(p)[q] for q in range(n)) / n
                J -= np.real(Gd) ** 2
        sig = sig - np.linalg.solve(J / Ny, F)
    raise RuntimeError("sector saddle not converged")

def sector_Q(g, n, saddle=False, ld1=None):
    if saddle and n > 1: _, Gs, _ = sector_saddle(g, n)
    else: Gs = sector_G(g, n)
    ld1 = sector_logdet(g, 1, sector_G(g, 1)) if ld1 is None else ld1
    return sector_logdet(g, n, Gs) - n * ld1
