"""EXP-081 memory dry run: one beta at W=2 r=6 Ny=48 (declared ~2.0 GB). [model: Opus 5.5]"""
import time, resource, sigma3d as S3
P = 12; S = S3.Strip3D(2 + 2 * P, 2 * P, 48, list(range(P, P + 2)), P - 1)
t0 = time.time(); B = S.inner(1.0, 0.5 + 0.5j); del B
print(f"W=2 r=6 Ny=48: one beta {time.time()-t0:.0f}s, maxrss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB", flush=True)
