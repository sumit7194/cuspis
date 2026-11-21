"""EXP-081b t0 diagnosis step 3: k = 0 slice of W4 P6 c3 (outlier t0[0] = -9.81 vs ~-5.8). Per-p contribution to
Tr(B1[0]^-1 dB0[0]) (linear in dB0), each slice's pole list (internal near-duplicates), and sensitivity of the confluent
contour (rad 1e-5 vs 1e-4, 1e-6; M 32 vs 64) through the PRODUCTION inner_beta0 with patched rad/M. [model: Opus 5.5]"""
import numpy as np, sigma3d as S3
W, P = 4, 6
for c in (2, 3):
    Lx, Lt = 2 * P + 4, 2 * P; x0 = P + (4 - W) // 2; Ny = int(c * 2 * P)
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); B1 = S.B1()
    inv0 = np.linalg.inv(B1[0])
    print(f"--- c{c} Ny {Ny}: slice pole lists (s <= 3.6) and min internal gap", flush=True)
    for p in range(Ny // 2 + 1):
        s = np.sort(S.sl[p].s); gap = np.min(np.diff(s)) if len(s) > 1 else np.inf
        print(f"   p={p:2d}: poles {np.round(s[s < 3.6], 6).tolist()}  min gap {gap:.1e}", flush=True)
    for rad, M in [(1e-5, 32), (1e-4, 32), (1e-6, 32), (1e-5, 64)]:
        dB = S.inner_beta0(1.0, dn=True, rad=rad, M=M)
        print(f"   rad {rad:.0e} M {M}: t0[0] = {np.trace(inv0 @ dB[0]).real:+.6f}  t0[1] = {np.trace(np.linalg.solve(B1[1], dB[1])).real:+.6f}", flush=True)
