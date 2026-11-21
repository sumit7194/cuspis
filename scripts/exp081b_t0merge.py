"""EXP-081b t0 diagnosis step 4: slices p and Ny-p are the same physical slice but their QEP poles are computed
separately; inner_beta0 merges poles only if |ds| < 1e-9. Report max |ds| between the pole lists of p and Ny-p for each
geometry (production pole lists, s <= s_cut), and which pairs miss the merge. [model: Opus 5.5]"""
import numpy as np, sigma3d as S3
geoms = [(W, P, 2, 4) for P in (4, 6, 8, 10, 12) for W in (2, 4)] + [(2, 6, 3, 4), (4, 6, 3, 4), (4, 8, 2, 8), (8, 8, 2, 8)]
for W, P, c, Wb in geoms:
    Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = int(c * 2 * P)
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); worst = []
    for p in range(1, (Ny + 1) // 2):
        a = np.sort([s for s in S.sl[p].s if s <= 3.0]); b = np.sort([s for s in S.sl[Ny - p].s if s <= 3.0])
        if len(a) != len(b): worst.append((np.inf, p, len(a), len(b))); continue
        if len(a): d = np.max(np.abs(a - b)); worst.append((d, p, a[np.argmax(np.abs(a - b))], None))
        dm2 = abs(S.sl[p].m2 - S.sl[Ny - p].m2) if hasattr(S.sl[p], "m2") else float("nan")
    worst.sort(reverse=True); miss = [w for w in worst if w[0] >= 1e-9]
    print(f"W{W} P{P} c{c} box{Wb} Ny {Ny}: max |ds(p) - ds(Ny-p)| = {worst[0][0]:.1e} at p={worst[0][1]} (s={worst[0][2]}); "
          f"pairs missing the 1e-9 merge: {len(miss)}" + (f" -> {[(w[1], round(float(w[2]), 6), f'{w[0]:.1e}') for w in miss[:4]]}" if miss else ""), flush=True)
