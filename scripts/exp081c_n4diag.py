"""EXP-081c prerequisite (the Bridge's item 5): root cause of the EXP-081b N4 failure (s_cut 2.5 vs 3: 1.6e-4 relative on
delta_kappa_lat(6)). Measures the beta=0 part X(s_cut) = t0 + T_saddle of W4 geometries (W2 has no poles above 1.3) as
s_cut is raised 2.0 -> 3.5, with the production code; pole completeness up to 3.5 by the EXP-081b grid census.
No W8P8 quantity is computed. [model: Opus 5.5]"""
import numpy as np, sigma3d as S3
from exp081b_census import census
for W, P in [(4, 4), (4, 6)]:
    Lx, Lt = 2 * P + 4, 2 * P; x0 = P + (4 - W) // 2; Ny = 4 * P
    S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.5)
    cen = census(S, 3.5); bad = [(c["p"], c["prod"], c["own"], c["touch"]) for c in cen if not c["match"] or c["touch"]]
    print(f"W{W} P{P}: census to s<=3.5 -> {bad if bad else 'production pole lists complete'}", flush=True)
    B1 = S.B1(); prev = None
    for sc in (2.0, 2.5, 2.75, 3.0, 3.25, 3.5):
        S.s_cut = sc
        dB0 = S.inner_beta0(1.0, dn=True); t0 = float(sum(np.trace(np.linalg.solve(B1[k], dB0[k])) for k in range(Ny)).real); del dB0
        ts = float(S3.saddle_term(S, B1).real); X = t0 + ts
        npol = sum(1 for p in range(Ny) for s in S.sl[p].s if 2.0 < s <= sc)
        print(f"   s_cut {sc:4.2f}: t0 {t0:+.9f} tsad {ts:+.9f} X {X:+.9f}" + (f"  dX vs prev {X - prev:+.2e}" if prev is not None else "") + f"  (poles in (2, s_cut]: {npol})", flush=True)
        prev = X
