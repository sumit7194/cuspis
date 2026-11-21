"""EXP-081b referee diagnosis, part 4: F(s) = z^W det(I + M C(z)), z = e^{-2 pi s}, which is O(1) as z -> 0. Sign-change scan on
a fine s grid (counts real roots independently of any root finder) plus findroot from each production pole. [model: Opus 5.5]"""
import os, sys, numpy as np, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3
mp.mp.dps = 50
W, P, Wbox, Ny = 4, 4, 4, 8; Lx, Lt = 2 * P + Wbox, 2 * P; x0 = P + (Wbox - W) // 2
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0)
for p in range(Ny // 2 + 1):
    sl = S.sl[p]; G0m = mp.inverse(mp.matrix(np.linalg.inv(sl.G0).round(12).tolist())); sites = [s for lu in sl.links for s in lu]
    M = mp.matrix([[G0m[i, j] for j in sites] for i in sites])
    def F(s):
        z = mp.exp(-2 * mp.pi * s); Cm = mp.zeros(2 * W, 2 * W)
        for j in range(W): Cm[2 * j + 1, 2 * j] = -(z - 1); Cm[2 * j, 2 * j + 1] = -(1 / z - 1)
        return mp.re(z ** W * mp.det(mp.eye(2 * W) + M * Cm))
    grid = [mp.mpf(k) / 400 for k in range(40, 2401)]; vals = [F(s) for s in grid]
    roots = [mp.findroot(F, (grid[i], grid[i + 1]), solver="anderson") for i in range(len(grid) - 1) if vals[i] * vals[i + 1] < 0]
    print(f"p={p}: sign-change roots in s in [0.1, 6]: {[round(float(r), 10) for r in roots]}", flush=True)
    print(f"      production poles:                {[round(x, 10) for x in sl.s]}", flush=True)
    print(f"      |F(prod s_j)|: {[f'{float(abs(F(mp.mpf(x)))):.1e}' for x in sl.s]};  F scale on grid: {float(max(abs(v) for v in vals)):.1e}", flush=True)
