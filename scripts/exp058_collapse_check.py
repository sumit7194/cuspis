"""EXP-058: collapse identity check on random Z_n-circulant kernels. [model: Opus 5.5]"""
import numpy as np
rng = np.random.default_rng(58)

def circ(blocks):                       # blocks[d] = s x s block for replica offset d = (j - i) mod n; symmetric overall
    n = len(blocks); s = blocks[0].shape[0]; M = np.zeros((n * s, n * s))
    for i in range(n):
        for j in range(n):
            M[i*s:(i+1)*s, j*s:(j+1)*s] = blocks[(j - i) % n]
    return M

def sym_circ_blocks(n, s, scale=1.0, zero_mode=False):
    A = [rng.normal(size=(s, s)) * scale for _ in range(n)]
    blocks = [0.5 * (A[d] + A[(-d) % n].T) for d in range(n)]          # block(-d) = block(d)^T  =>  M symmetric
    if zero_mode:                                                     # remove the k = 0 replica-Fourier component
        mean = sum(blocks) / n; blocks = [b - mean for b in blocks]
    return blocks

def fourier_trace(Sb, Gb):              # sum_k Tr(S^(k) G^(k)^T-orientation) for circulant block lists; equals Tr(S_full G_full)/... check vs direct
    n = len(Sb); tot = 0.0
    for k in range(n):
        Sk = sum(Sb[d] * np.exp(2j * np.pi * k * d / n) for d in range(n))
        Gk = sum(Gb[d] * np.exp(-2j * np.pi * k * d / n) for d in range(n))
        tot += np.trace(Sk @ Gk.T).real
    return tot

ok = True
for n in (2, 3, 5):
    s = 6
    base = sym_circ_blocks(n, s, 0.15); base[0] = base[0] + 3.0 * np.eye(s)
    G = circ(base); assert np.allclose(G, G.T)
    dB = sym_circ_blocks(n, s, 0.1, zero_mode=True); dG = circ(dB)
    F = lambda t, c=2.0: 0.5 * np.linalg.slogdet(c * (G + t * dG) ** 2)[1]
    h = 1e-5; lhs = (F(h) - F(-h)) / (2 * h)
    B = 2 * G ** 2; D = np.linalg.inv(B); Sig = D * G
    direct = 2 * np.sum(Sig * dG)                                    # 2 Tr(Sigma dG) with symmetric matrices
    # replica-sector form: Sigma and dG circulant; sum_k Tr(S^(k) dG^(k)) with Parseval normalisation n
    Sb = [Sig[0:s, d*s:(d+1)*s] for d in range(n)]
    sect = 2 * n * fourier_trace(Sb, dB) / n                          # n blocks rows x (1/n) Parseval
    k0 = 2 * n * (np.trace(sum(Sb) @ sum(dB).T)) / n / n              # k = 0 term alone (must vanish: dG has no k=0 part)
    r1 = abs(lhs / sect - 1); r2 = abs(direct / sect - 1)
    good = r1 <= 1e-7 and r2 <= 1e-12 and abs(k0) <= 1e-12 * abs(sect); ok &= good
    # must-fail: B without the factor 2 in log det but delta B with it
    Fbad = lambda t: 0.5 * np.linalg.slogdet((G + t * dG) ** 2)[1]
    bad = (Fbad(h) - Fbad(-h)) / (2 * h); mf = abs(bad / (sect / 2) - 1) < 1e-6 and abs(bad / sect - 1) > 0.1
    print(f"n={n}: d/dt (1/2) logdet B = {lhs:.12e}; 2 sum_k Tr(S^(k) dG^(k)) = {sect:.12e} (rel {r1:.1e}); direct 2Tr(S dG) rel {r2:.1e}; "
          f"k=0 term {k0:.1e} [{'PASS' if good else 'FAIL'}]  | must-fail (B without 2): {bad:.6e} vs sect {sect:.6e} [{'fires' if abs(bad/sect-1)>1e-3 else 'DOES NOT FIRE'}]")
print("R1", "PASS" if ok else "FAIL")
