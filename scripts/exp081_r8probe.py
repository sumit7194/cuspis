"""r=8 feasibility probe (Bridge/Sumit question; no S_conn value formed): W=2, r=8 slice (34x32 = 1088 sites), one beta
of the inner continuation at Ny = 8 and 16, strip and edge cuts; measured peak RSS and wall time, for extrapolation to
Ny = 64. [model: Opus 5.5]"""
import time, resource, gc, sigma3d as S3
W, P = 2, 16; Lx, Lt = W + 2 * P, 2 * P
for Ny in (8, 16):
    for name, cut in (("strip", list(range(P, P + W))), ("edge", list(range(P, Lx)))):
        t0 = time.time(); S = S3.Strip3D(Lx, Lt, Ny, cut, P - 1); tb = time.time() - t0
        t0 = time.time(); B = S.inner(1.0, 0.5 + 0.5j); tbeta = time.time() - t0; del B
        t0 = time.time(); dB = S.inner_beta0(1.0, dn=True); tq0 = time.time() - t0; del dB, S; gc.collect()
        print(f"Ny={Ny} {name}: build {tb:.0f}s, one beta {tbeta:.0f}s, q=0 derivative term {tq0:.0f}s, maxrss so far {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB", flush=True)
