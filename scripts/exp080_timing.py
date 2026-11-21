"""EXP-080 timing/peak for the P1 grid decision: full route-(i) S^(0) for one configuration (strip) at W=4 (r=2, Ny=16),
and the free S for strip/edges at W=4..16 (cheap). [model: Opus 5.5]"""
import time, resource, numpy as np, sigma3d as S3
def geom(W, r, Ny, which):
    P = int(round(r * W)); Lx, Lt = W + 2 * P, 2 * P; tcut = P - 1
    cut = {"strip": list(range(P, P + W)), "e1": list(range(P, Lx)), "e2": list(range(0, P + W))}[which]
    return S3.Strip3D(Lx, Lt, Ny, cut, tcut)
t0 = time.time(); S = geom(4, 2, 16, "strip"); q, t0k, Cg = S3.route_i(S, cpts=12)
print(f"sigma route-(i) W=4 r=2 Ny=16 strip: Q'(1) = {q.real:.8f}  [{time.time()-t0:.0f}s, maxrss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB]", flush=True)
for W in (4, 8, 12, 16):
    t0 = time.time(); Sf = {w: S3.free_S(geom(W, 2, 4 * W, w)) for w in ("strip", "e1", "e2")}
    conn = (Sf["strip"] - Sf["e1"] - Sf["e2"]).real
    print(f"free W={W} r=2 Ny={4*W}: S_conn = {conn:.8f}; kappa_lat = -S_conn*W/Ny = {-conn*W/(4*W):.6f} (continuum 0.0396481)  [{time.time()-t0:.0f}s]", flush=True)
