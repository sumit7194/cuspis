"""EXP-081b t0 diagnosis step 2: per-transverse-slice t0[k] = Tr(B1[k]^-1 dB0[k]) and tsad is not split; production
inner_beta0(dn=True). A smooth F(kappa) gives sum_k F ~ Ny-proportional; an outlier k marks the defect. [model: Opus 5.5]"""
import sys, json, numpy as np, sigma3d as S3
out = {}
for W, P, c in [(4, 6, 2), (4, 6, 3), (2, 6, 2), (2, 6, 3)]:
    Lx, Lt = 2 * P + 4, 2 * P; x0 = P + (4 - W) // 2; Ny = int(c * 2 * P)
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0)
    B1 = S.B1(); dB0 = S.inner_beta0(1.0, dn=True)
    t = [float(np.trace(np.linalg.solve(B1[k], dB0[k])).real) for k in range(Ny)]
    cond = [float(np.linalg.cond(B1[k])) for k in range(Ny)]
    out[f"W{W}c{c}"] = dict(Ny=Ny, t=t, cond=cond)
    print(f"W{W} P{P} c{c} Ny {Ny}: sum t0 {sum(t):+.6f}", flush=True)
    for k in range(Ny // 2 + 1): print(f"   k={k:2d} kappa/pi={2*k/Ny:.4f} t0[k]={t[k]:+.6f} cond(B1)={cond[k]:.1e}", flush=True)
json.dump(out, open("exp081b_t0perk_results.json", "w"))
