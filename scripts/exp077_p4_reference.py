"""EXP-077 pre-check: independent reproduction of the integer-n replica-manifold reference values used as T37's P4 targets.
Lattice (T36's spec): per-sheet Lx=6 (x), Lt=4 (t), m^2 = 0.5, H = (4+m^2) - nearest-neighbour hopping, open boundaries;
cut on the t-links t=1 -> t=2 at x in {2,3}; n sheets glued cyclically across the cut (sheet s -> s+1 going up).
Q(n) = log det B_n - n log det B_1, B = 2 G o G (Hadamard) on the full n*N-site manifold. Written independently of
T36's script (own site ordering: index = sheet*N + t*Lx + x). [model: Opus 5.5]"""
import numpy as np
Lx, Lt, m2, tcut, cutx = 6, 4, 0.5, 1, (2, 3)
N = Lx * Lt
def H_Mn(n):
    H = np.zeros((n * N, n * N))
    idx = lambda s, x, t: s * N + t * Lx + x
    for s in range(n):
        for x in range(Lx):
            for t in range(Lt):
                i = idx(s, x, t); H[i, i] = 4 + m2
                if x + 1 < Lx:
                    j = idx(s, x + 1, t); H[i, j] = H[j, i] = -1
                if t + 1 < Lt:
                    s2 = (s + 1) % n if (t == tcut and x in cutx) else s
                    j = idx(s2, x, t + 1); H[i, j] = H[j, i] = -1
    return H
def logdetB(n):
    G = np.linalg.inv(H_Mn(n)); s, ld = np.linalg.slogdet(2 * G * G); return ld, s
ld1, s1 = logdetB(1)
for n in (2, 3, 4):
    ld, s = logdetB(n); print(f"n={n}: Q(n) = logdet B_n - n logdet B_1 = {ld - n*ld1:+.10f}  (sign {s:+.0f})")
