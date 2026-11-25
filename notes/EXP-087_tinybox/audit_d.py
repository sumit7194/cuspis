"""EXP-087 residue-path audit (numerical): on a tiny box with near-degenerate doublets, (1) per-member vs summed doublet contributions to d
(cancellation ratio), (2) d's radius-variation spread (residue radius x2, x0.5, as 085 phase C), (3) same for a W6 control. [model: Opus 5.5]"""
import sys, numpy as np
sys.path.insert(0, "/Users/sumit/Github/corner_function/scripts")
import sigma3d as S3, exp081c_numerics as C
def run(W, P, Wb, Ny):
    Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); U = C.install(S, refine="auto", lowrank=False, rank_drop=0)
    d = C.coincident_dn_c(S)
    def d_rad(f):
        out = np.zeros(S.N, dtype=complex)
        for sp in S.sl:
            for j, sj in enumerate(sp.s):
                if sj > S.s_cut: continue
                r = f * min(1e-6, 0.3 * min([abs(sj - sk) for sk in sp.s if sk != sj] + [1.0]))
                for a0, up in ((1j * sj, True), (-1j * sj, False)): out += (2j * np.pi) * sp.scale * np.diag(sp.residue(a0, r)) * S3._kdn(a0, up)
        return out / S.Ny
    spread = max(float(np.abs(d_rad(f) - d).max()) for f in (2.0, 0.5))
    print(f"W{W}P{P}Wb{Wb}Ny{Ny}: max|d| {np.abs(d).max():.3e}; radius-variation spread {spread:.2e} (rel {spread/np.abs(d).max():.1e})")
    for p in range(Ny // 2 + 1):
        sp = S.sl[p]; s = sorted((v, j) for j, v in enumerate(sp.s) if v <= 3.0)
        for (s1, j1), (s2, j2) in zip(s[:-1], s[1:]):
            if s2 - s1 >= 1e-4: continue
            c = [np.diag(sp.Rfull(sp.Rp[j])) * S3._kdn(1j * v, True) + np.diag(sp.Rfull(sp.Rm[j])) * S3._kdn(-1j * v, False) for v, j in ((s1, j1), (s2, j2))]
            m1, m2, ms = np.abs(c[0]).max(), np.abs(c[1]).max(), np.abs(c[0] + c[1]).max()
            print(f"   slice {p:2d} gap {s2-s1:.1e}: |member1| {m1:.2e} |member2| {m2:.2e} |sum| {ms:.2e}  cancellation x{max(m1,m2)/max(ms,1e-300):.1e}")
for g in ((10, 3, 10, 16), (8, 3, 8, 16), (6, 3, 6, 16)): run(*g)
