"""EXP-081b referee diagnosis, part 3: refine production poles in the s variable with the scaled function
h(s) = z^W det(I + M C(z)), z = e^{-2 pi s} (a polynomial in z; removes the 1/z blow-up), and report s_mp - s_prod and the
smallest singular value ratio of (I + M C) at the refined pole. [model: Opus 5.5]"""
import os, sys, numpy as np, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3
mp.mp.dps = 40
W, P, Wbox, Ny = 4, 4, 4, 8; Lx, Lt = 2 * P + Wbox, 2 * P; x0 = P + (Wbox - W) // 2
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0)
for p in range(Ny // 2 + 1):
    sl = S.sl[p]; G0m = mp.inverse(mp.matrix(np.linalg.inv(sl.G0).round(12).tolist())); sites = [s for lu in sl.links for s in lu]
    M = mp.matrix([[G0m[i, j] for j in sites] for i in sites])
    def zC(z):                                                            # z * C(z): entries -(z-1) z and -(1 - z)
        Cm = mp.zeros(2 * W, 2 * W)
        for j in range(W): Cm[2 * j + 1, 2 * j] = -(z - 1) * z; Cm[2 * j, 2 * j + 1] = -(1 - z)
        return Cm
    h = lambda s: mp.det(mp.exp(-2 * mp.pi * s) * mp.eye(2 * W) + M * zC(mp.exp(-2 * mp.pi * s)))   # = z^{2W} det(I+MC)/z^W
    for sj in sl.s:
        sm = mp.findroot(h, mp.mpf(sj), tol=mp.mpf(10) ** -30)
        print(f"p={p} prod s_j {sj:.12f}  mp s_j {float(mp.re(sm)):.12f}  diff {float(mp.re(sm)) - sj:+.1e}  Im {float(mp.im(sm)):.0e}", flush=True)
