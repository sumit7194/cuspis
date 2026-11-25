"""Fable side check (UNVERIFIED): nuisance sweep of inner_beta0's contour radius `rad` on a SMALL geometry that has
near-degenerate intra-slice pole doublets (cut width W = 8).  Production path: Strip3D + exp081c_numerics.install + S.inner_beta0(dn=True).
If t0 moves when rad drops below the smallest doublet gap, the default rad = 1e-5 is not safe for such doublets.  [model: Fable 5.2]"""
import sys, os, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import sigma3d as S3, exp081c_numerics as C
W, P, Wb, Ny = [int(v) for v in sys.argv[1:5]]; rads = [float(v) for v in sys.argv[5:]]
Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); C.install(S, refine="auto", lowrank=False, rank_drop=0)
gaps = sorted((float(g), float(s), p) for p in range(Ny // 2 + 1) for s, g in zip(sorted(v for v in S.sl[p].s if v <= 3)[:-1], np.diff(sorted(v for v in S.sl[p].s if v <= 3))) if g < 1e-4)
print(f"W{W} P{P} Wb{Wb} Ny{Ny} (Lx {Lx}, Lt {Lt}, N {S.N}); intra-slice gaps < 1e-4: {[(f'{g:.1e}', round(s,3), p) for g, s, p in gaps]}", flush=True)
B1 = S.B1(); A = [np.linalg.inv(B1[k]) for k in range(Ny)]
for rad in rads:
    t = time.time(); dB0 = S.inner_beta0(1.0, rad=rad, dn=True)
    tk = np.array([np.trace(A[k] @ dB0[k]).real for k in range(Ny)])
    print(f"  rad {rad:.0e}: t0 = {tk.sum():.9f}   per-k (k=0, then even k): {np.round(tk[[0] + list(range(2, Ny // 2 + 1, 2))], 6)}   ({time.time()-t:.0f}s)", flush=True)
