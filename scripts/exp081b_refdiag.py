"""EXP-081b: why did the N2 referee fire? One slice, one tail point, three evaluations: float64 stable Woodbury, float64
direct inverse, mpmath 40 digits (two ways: referee Woodbury and direct mp inverse of H). [model: Opus 5.5]"""
import os, sys, numpy as np, mpmath as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3
mp.mp.dps = 40
W, P, Wbox, Ny = 4, 4, 4, 8; Lx, Lt = 2 * P + Wbox, 2 * P; x0 = P + (Wbox - W) // 2
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); N = S.N
print("poles per slice:", [[round(x, 4) for x in sl.s] for sl in S.sl])
p = 0; sl = S.sl[p]; sj = sl.s[-1]
H0 = mp.matrix(np.linalg.inv(sl.G0).round(12).tolist())                  # integer stencil, exact after rounding
def mpG_direct(a):
    z = mp.exp(2j * mp.pi * a); H = H0.copy()
    for (l, u) in sl.links: H[u, l] += -(z - 1); H[l, u] += -(1 / z - 1)
    return mp.inverse(H)
G0m = mp.inverse(H0); sites = [s for lu in sl.links for s in lu]
A = mp.matrix([[G0m[i, j] for j in sites] for i in range(N)]); M = mp.matrix([[G0m[i, j] for j in sites] for i in sites])
def mpG_wood(a):
    z = mp.exp(2j * mp.pi * a); Cm = mp.zeros(2 * W, 2 * W)
    for j in range(W): Cm[2 * j + 1, 2 * j] = -(z - 1); Cm[2 * j, 2 * j + 1] = -(1 / z - 1)
    return G0m - A * (Cm * mp.inverse(mp.eye(2 * W) + M * Cm)) * A.T
npa = lambda X: np.array(X.tolist(), dtype=complex)
for s in (1.0, 2.0, 3.0):
    for sg in (-1, 1):
        a = 0.5 + 1j * s + sg * 1j * sj; am = mp.mpf("0.5") + 1j * mp.mpf(s) + sg * 1j * mp.mpf(sj)
        Gs, Gd, Gmd, Gmw = sl.G(a), S3._G_direct(sl, a), npa(mpG_direct(am)), npa(mpG_wood(am))
        r = lambda X, Y: np.abs(X - Y).max() / np.abs(Y).max()
        print(f"s={s} sg={sg:+d} Im a={a.imag:+.3f}: |G|max {np.abs(Gmd).max():.2e}  stable-vs-mpdirect {r(Gs, Gmd):.1e}  "
              f"direct-vs-mpdirect {r(Gd, Gmd):.1e}  mpWood-vs-mpdirect {r(Gmw, Gmd):.1e}", flush=True)
