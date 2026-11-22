"""EXP-081d (DRAFT, unregistered) cost probe, Bridge OK 2026-11-22. TIMING ONLY: no physics value is printed or stored (081d
is not registered; no comparison number may exist before it is). Measures, with the 081c numerics:
  (a) k = 1.5 W2 geometry (W6 @ P6 box 6, N 216, Ny 24): residue install, one C-node (s = 1.974...), t0 -- wall and G-call counts;
  (b) single-G cost (inverse + adaptive refinement) at N = 96k^2 for k = 1, 1.5, 2, 2.5, 3 (W = 4k geometry, one slice, alpha
      at s = 2.5 on the beta = 1/2 line) -> the N^3 scaling assumption. [model: Opus 5.5]"""
import sys, os, time, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import sigma3d as S3, exp081c_numerics as C
out = {}
def strip(k):
    W, P, B = int(4 * k), int(4 * k), int(4 * k); Lx, Lt = 2 * P + B, 2 * P; x0 = P + (B - W) // 2
    return S3.Strip3D(Lx, Lt, 4 * P, list(range(x0, x0 + W)), P - 1, s_cut=3.0)
# (b) single-G cost
for k in (1, 1.5, 2, 2.5, 3):
    t = time.time(); S = strip(k); tb = time.time() - t
    # build only the H machinery (no residue install) by temporarily using s_cut = -1
    base = S.sl[1]; ex = C.ExactSlice(base, S.Lx, S.Lt, 2 - 2 * np.cos(2 * np.pi / S.Ny), -1.0, refine="auto")
    C.ExactSlice.reset_stats(); reps = 3 if k <= 2 else 2; t = time.time()
    for _ in range(reps): ex.G_raw(0.5 + 2.5j)
    tg = (time.time() - t) / reps; st = dict(C.ExactSlice.STATS)
    out[f"G_k{k}"] = dict(N=S.N, sec_per_G=tg, steps=st["maxsteps"], strip_build_sec=tb)
    print(f"k={k}: N={S.N}: {tg*1e3:.1f} ms per G (adaptive, steps {st['maxsteps']}); Strip3D build {tb:.0f} s", flush=True)
    del S, ex
# (a) k = 1.5 W2 geometry timings
S = strip(1.5); t = time.time(); C.ExactSlice.reset_stats(); U = C.install(S, refine="auto")
out["k1.5_install"] = dict(sec=time.time() - t, calls=C.ExactSlice.STATS["calls"], poles=sum(sum(1 for s in u.s if s <= 3) for u in U.values()), unique=len(U))
print(f"k=1.5 W6P6b6: install {out['k1.5_install']['sec']:.0f} s, {out['k1.5_install']['calls']} G, {out['k1.5_install']['poles']} poles <= 3 over {len(U)} unique slices", flush=True)
B1 = S.B1(); ld1 = [S3.logdet(B1[k]) for k in range(S.Ny)]
C.ExactSlice.reset_stats(); t = time.time(); _ = C.g_node(S, 1.974126375751365, ld1)
out["k1.5_node"] = dict(sec=time.time() - t, calls=C.ExactSlice.STATS["calls"]); del _
print(f"k=1.5: one C-node {out['k1.5_node']['sec']:.0f} s, {out['k1.5_node']['calls']} G", flush=True)
C.ExactSlice.reset_stats(); t = time.time(); _ = C.t0_term(S, B1)
out["k1.5_t0"] = dict(sec=time.time() - t, calls=C.ExactSlice.STATS["calls"]); del _
print(f"k=1.5: t0 {out['k1.5_t0']['sec']:.0f} s, {out['k1.5_t0']['calls']} G", flush=True)
json.dump(out, open(os.path.join(HERE, "exp081d_costprobe.json"), "w"), indent=1)
