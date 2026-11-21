"""EXP-081c B2a (registered 8fcfb84): production 081c H(alpha) (exp081c_numerics.ExactSlice.H) vs the sub-agent's
code-blind build (exp081c_B2a_build.build_H), entrywise, at every distinct (slice, alpha) of the s ~ 1.974 node of W8P8
box8 (npt = 40 segment points of inner() plus all tail ingredients beta -+ i s_j, s_j <= 3). Pass: max relative entry
difference <= 1e-15. Must-fire: the same comparison against build_H(..., wrong_link=True) must fail, else B2a void.
[model: Opus 5.5]"""
import json, numpy as np, sigma3d as S3, exp081c_numerics as C
from exp081c_B2a_build import build_H
P, W, Wb = 8, 8, 8; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = 4 * P; tcut = P - 1; cutx = list(range(x0, x0 + W))
S = S3.Strip3D(Lx, Lt, Ny, cutx, tcut, s_cut=3.0)
U = {p: C.ExactSlice(S.sl[p], Lx, Lt, 2 - 2 * np.cos(2 * np.pi * p / Ny), -1.0) for p in range(Ny // 2 + 1)}
beta = 0.5 + 1j * 1.974126375751365; x, w = np.polynomial.legendre.leggauss(40); u = 0.5 * (x + 1)
alphas = set()
for ui in u: alphas |= {ui * beta, (1 - ui) * beta, beta + ui * (1 - beta), 1 - ui * (1 - beta)}
alphas |= {beta + sg * 1j * sj for p in U for sj in U[p].s if sj <= 3.0 for sg in (-1, 1)}
worst, worst_wrong, n = 0.0, 0.0, 0
for p, sl in U.items():
    m2 = 2 - 2 * np.cos(2 * np.pi * p / Ny)
    for a in alphas:
        Hp = sl.H(a)[0]; Hb = build_H(Lx, Lt, m2, cutx, tcut, a); sc = np.abs(Hp).max()
        worst = max(worst, np.abs(Hp - Hb).max() / sc); n += 1
        worst_wrong = max(worst_wrong, np.abs(Hp - build_H(Lx, Lt, m2, cutx, tcut, a, wrong_link=True)).max() / sc)
ok = worst <= 1e-15; mf = worst_wrong > 1e-15
print(f"B2a: {n} (slice, alpha) pairs ({len(alphas)} alphas x {len(U)} slices): max rel entry diff {worst:.1e} -> {'PASS' if ok else 'FAIL'}; "
      f"must-fire (wrong link) max rel diff {worst_wrong:.1e} -> {'FIRES' if mf else 'DOES NOT FIRE -> B2a VOID'}", flush=True)
json.dump(dict(n=n, max_rel=worst, pass_=bool(ok), mustfire_max=worst_wrong, mustfire_fires=bool(mf)), open("exp081c_b2a_results.json", "w"), indent=1)
