"""EXP-081 timing for an edge configuration (W=2, r=4, Ny=32): one beta, s_cut in {inf, 2.5}, npt in {40, 24}; and the
pole counts. No S_conn value is formed. [model: Opus 5.5]"""
import time, resource, numpy as np, sigma3d as S3
W, r = 2, 4; P = r * W; Lx, Lt = W + 2 * P, 2 * P
for sc in (np.inf, 2.5):
    t0 = time.time(); S = S3.Strip3D(Lx, Lt, 4 * P, list(range(P, Lx)), P - 1, s_cut=sc); tb = time.time() - t0
    npol = [len([x for x in s.s if x <= sc]) for s in S.sl]
    for npt in (40, 24):
        t0 = time.time(); B = S.inner(1.0, 0.5 + 0.5j, npt=npt); el = time.time() - t0
        if sc == np.inf and npt == 40: Bref = B
        print(f"edge W={W} r={r} Ny={4*P} s_cut={sc} npt={npt}: poles used/slice min {min(npol)} max {max(npol)}; one beta {el:.0f}s; "
              f"max rel diff vs (inf,40) {np.abs(B - Bref).max()/np.abs(Bref).max():.1e}; maxrss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB", flush=True)
