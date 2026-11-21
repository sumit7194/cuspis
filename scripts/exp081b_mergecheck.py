"""EXP-081b: replay inner_beta0's pole-merge decisions for every (k, p) of every driver geometry at tol 1e-9 (as run)
and 1e-7 (fix, = rad/100). Any geometry whose decisions differ is affected by the fix; all others are computed
identically by construction. [model: Opus 5.5]"""
import numpy as np, sigma3d as S3
def decisions(S, tol):
    Ny = S.Ny; out = []
    for k in range(Ny):
        for p in range(Ny):
            q = (k - p) % Ny; sa, sb = S.sl[p], S.sl[q]
            locs = [(a0, "a") for sj in sa.s if sj <= S.s_cut for a0 in (1j * sj, -1j * sj)] + \
                   [(a0, "b") for sj in sb.s if sj <= S.s_cut for a0 in (-1j * sj, 1j * sj)]
            merged = []
            for a0, tag in locs:
                hit = [m for m in merged if abs(m[0] - a0) < tol]
                if hit: hit[0][1].add(tag)
                else: merged.append([a0, {tag}])
            out.append(tuple(sorted(len(t) for _, t in merged)))
    return out
G = [(W, P, 4, 2, 3.0) for P in (4, 6, 8, 10, 12) for W in (2, 4)] + [(W, 6, 4, 3, 3.0) for W in (2, 4)] + \
    [(W, 6, 4, 2, 2.5) for W in (2, 4)] + [(4, 8, 8, 2, 3.0), (8, 8, 8, 2, 3.0)]   # cp16 and dd1 share the cp12/dd0 merge logic & poles
for W, P, Wb, c, sc in G:
    Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = int(c * 2 * P)
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=sc)
    a, b = decisions(S, 1e-9), decisions(S, 1e-7); nd = sum(x != y for x, y in zip(a, b))
    print(f"W{W} P{P} box{Wb} c{c} s_cut{sc}: (k,p) pairs {len(a)}, decisions differing 1e-9 vs 1e-7: {nd}", flush=True)
