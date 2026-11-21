"""EXP-081b referee diagnosis, part 2: do the referee's findroot-refined poles match production's? Also log-det of
det(I + M C(z)) at both. [model: Opus 5.5]"""
import os, sys, numpy as np, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3
mp.mp.dps = 40
W, P, Wbox, Ny = 4, 4, 4, 8; Lx, Lt = 2 * P + Wbox, 2 * P; x0 = P + (Wbox - W) // 2
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); N = S.N
for p in range(Ny // 2 + 1):
    sl = S.sl[p]; G0m = mp.inverse(mp.matrix(np.linalg.inv(sl.G0).round(12).tolist())); sites = [s for lu in sl.links for s in lu]
    M = mp.matrix([[G0m[i, j] for j in sites] for i in sites])
    def C(z):
        Cm = mp.zeros(2 * W, 2 * W)
        for j in range(W): Cm[2 * j + 1, 2 * j] = -(z - 1); Cm[2 * j, 2 * j + 1] = -(1 / z - 1)
        return Cm
    f = lambda z: mp.det(mp.eye(2 * W) + M * C(z))
    for sj in sl.s:
        z0 = mp.mpf(np.exp(-2 * np.pi * sj)); z = mp.findroot(f, z0, tol=mp.mpf(10) ** -35)
        sm = -mp.log(mp.re(z)) / (2 * mp.pi)
        print(f"p={p} prod s_j {sj:.10f}  |f(z_prod)| {float(abs(f(z0))):.1e}  referee s_j {float(sm):.10f}  Im z {float(mp.im(z)):.1e}  diff {float(sm) - sj:+.1e}", flush=True)
