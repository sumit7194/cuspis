"""EXP-080 memory probe (after residue-factoring): regression on the tiny lattice, then one beta at W=6 for Ny = 8, 16
(measured peak), extrapolate before trying Ny = 32. [model: Opus 5.5]"""
import time, resource, numpy as np, sigma3d as S3
S = S3.Strip3D(6, 4, 4, [2, 3], 1)
Gs = [[s.G(kk / 2) for kk in range(2)] for s in S.sl]
print("regression a2:", [round(S3.honest_slices(S, n).real - S3.honest_3d_replica(6, 4, 4, [2, 3], 1, n), 14) for n in (2, 3)], flush=True)
for Ny in (8, 16):
    t0 = time.time(); S2 = S3.Strip3D(30, 24, Ny, list(range(12, 18)), 11); tb = time.time() - t0
    m0 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9
    t0 = time.time(); B = S2.inner(1.0, 0.5 + 0.5j); del B
    print(f"W=6 Ny={Ny}: build {tb:.1f}s (rss {m0:.2f} GB), one beta {time.time()-t0:.1f}s, maxrss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB", flush=True)
