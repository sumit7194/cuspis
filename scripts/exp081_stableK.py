"""EXP-081a: stable Woodbury K = (C^{-1}+M)^{-1} away from z=1 vs direct dense inverse, edge slice and g(s) at W=2 r=3.
[model: Opus 5.5]"""
import numpy as np, sigma3d as S3
P, W = 6, 2; Lx, Lt = W + 2 * P, 2 * P
S = S3.Strip3D(Lx, Lt, 4 * P, list(range(P, Lx)), P - 1); sl = S.sl[0]; H0 = np.linalg.inv(sl.G0)
def Gd(sl, a):
    z = np.exp(2j * np.pi * a); H = np.linalg.inv(sl.G0).astype(complex)
    for (l, u) in sl.links: H[u, l] += -(z - 1); H[l, u] += -(1 / z - 1)
    return np.linalg.inv(H)
for s in (0.25, 1, 2, 3, 4, 5):
    for a in (0.5 + 1j * s, 0.1 + 1j * s, 0.9 - 1j * s):
        print(f"alpha={a}: max|G_stable - G_direct|/max|G| = {np.abs(sl.G(a)-Gd(sl, a)).max()/np.abs(Gd(sl, a)).max():.1e}", flush=True)
print("edge poles s (slices 0,1):", [np.round(S.sl[p].s, 6).tolist() for p in (0, 1)])
B1 = S.B1(); ld1 = [np.linalg.slogdet(B1[k])[1] for k in range(S.Ny)]
for s in (1.5, 2.0, 2.5, 3.0, 3.5):
    B = S.inner(1.0, 0.5 + 1j * s); print(f"s={s}: edge g (stable Woodbury) = {sum(np.linalg.slogdet(B[k])[1]-ld1[k] for k in range(S.Ny)):+.6f}", flush=True)
