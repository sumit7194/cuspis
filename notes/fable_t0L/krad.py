"""Fable side check (UNVERIFIED): radial breakdown of T_rho/Ny = Sum_x rho(x) K'(x,x) around the two branch points.  [model: Fable 5.2]"""
import sys, os, time, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(HERE, "..", "..", "scripts"))
import sigma3d as S3, exp081c_numerics as C
W, P = int(sys.argv[1]), int(sys.argv[2]); Lx, Lt = 3 * P, 2 * P; x0 = P + (P - W) // 2; Ny = 4 * P
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); C.install(S, refine="auto", lowrank=False, rank_drop=0)
N = S.N; B1 = S.B1(); dB0 = S.inner_beta0(1.0, dn=True); d = C.coincident_dn_c(S).real
G0 = np.array([sl.G0 for sl in S.sl]); gd = np.array([np.diag(g) for g in G0]).sum(axis=0) / Ny
K0 = 0.5 * np.array([np.diag(b).real for b in dB0]).sum(axis=0) / Ny - 2 * gd * d; rho = np.linalg.solve(B1[0], np.ones(N)).real
xs, ts = np.divmod(np.arange(N), Lt); bp = [(x0 - 0.5, P - 0.5), (x0 + W - 0.5, P - 0.5)]
r = np.minimum(*[np.hypot(xs - bx, ts - bt) for bx, bt in bp])
print(f"W{W}P{P}: Sum K' = {K0.sum():.6f}  Sum rho K' = {np.sum(rho*K0):.6f}  min K' = {K0.min():.2e}  rho at the 8 hot sites (r=0.707): {np.round(rho[r < 0.8], 3)}  K' there: {np.round(K0[r < 0.8], 6)}")
for lo, hi in ((0, 0.8), (0.8, 1.7), (1.7, 2.6), (2.6, 4.0), (4.0, 99)):
    m = (r >= lo) & (r < hi); print(f"   r in [{lo},{hi}): sites {m.sum():4d}  Sum K' {K0[m].sum():+.6f}  Sum rho K' {np.sum(rho[m]*K0[m]):+.6f}  mean rho {rho[m].mean():.3f}")
