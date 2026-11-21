"""EXP-081c resource dry run (the Bridge's item 6), W8 P8 box8 with direct-inverse G. NO g, S or R is computed:
(1) G-call counts of the production inner(beta) and inner_beta0(dn) with a dummy G (constant matrix, results discarded);
(2) wall time of one direct inverse of the exact integer H(alpha) (N = 384) and of a matmul-size refinement step;
(3) peak memory from the watchdog. [model: Opus 5.5]"""
import time, resource, numpy as np, sigma3d as S3
P, W, Wb = 8, 8, 8; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = 4 * P
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0); N = S.N
cnt = {"n": 0}; dummy = S.sl[0].G0.astype(complex)
for sl in S.sl:
    sl.G = (lambda a: (cnt.__setitem__("n", cnt["n"] + 1), dummy)[1])
t0 = time.time(); S.inner(1.0, 0.5 + 1.0j, 40); c_in = cnt["n"]; t_in = time.time() - t0
cnt["n"] = 0; t0 = time.time(); S.inner_beta0(1.0, dn=True); c_b0 = cnt["n"]; t_b0 = time.time() - t0
print(f"G calls: inner(beta) {c_in} (overhead {t_in:.0f}s), inner_beta0(dn) {c_b0} (overhead {t_b0:.0f}s); poles<=3 per unique slice: "
      f"{[sum(1 for s in S.sl[p].s if s <= 3) for p in range(Ny // 2 + 1)]}", flush=True)
H = np.linalg.inv(S.sl[3].G0).astype(complex); H[5, 6] += 1e6; reps = 20
t0 = time.time()
for _ in range(reps): G = np.linalg.inv(H)
ti = (time.time() - t0) / reps; t0 = time.time()
for _ in range(reps): X = G @ (np.eye(N) - H @ G)
tr = (time.time() - t0) / reps
print(f"N={N}: one complex inverse {ti*1e3:.1f} ms; one refinement-size step (2 matmuls) {tr*1e3:.1f} ms", flush=True)
nodes = 48 + 5
est_in = c_in * nodes * (ti + tr) + nodes * t_in; est_b0 = c_b0 * (ti + tr) + t_b0
print(f"estimate W8P8 direct+refined: C-nodes+checks {est_in/3600:.1f} h, t0 {est_b0/3600:.1f} h, total {(est_in+est_b0)/3600:.1f} h "
      f"(+ the same again for the Woodbury-vs-direct t0 comparison: already done in production); maxrss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB", flush=True)
