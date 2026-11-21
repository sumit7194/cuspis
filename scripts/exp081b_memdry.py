"""EXP-081b dry run at the largest geometry: W=4 strip in the P=12 pair box (28x24 = 672 sites), Ny=48: one beta of inner
+ node_reliability; measured peak and time. [model: Opus 5.5]"""
import time, resource, sigma3d as S3
P = 12; S = S3.Strip3D(2 * P + 4, 2 * P, 48, list(range(P, P + 4)), P - 1, s_cut=3.0)
t0 = time.time(); B = S.inner(1.0, 0.5 + 1.0j); t1 = time.time() - t0; del B
t0 = time.time(); rel = S3.node_reliability(S, 0.5 + 1.0j); t2 = time.time() - t0
print(f"P=12 W=4 Ny=48: one beta {t1:.0f}s, reliability {t2:.0f}s (rel {rel:.1e}), maxrss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB", flush=True)
