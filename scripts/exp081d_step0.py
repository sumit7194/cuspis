"""EXP-081d Step 0 (parameterised copy of exp081c_step0.py; usage: W P Wbox; output exp081d_results/step0_W{W}P{P}b{Wb}.json). EXP-081c Step 0 (registered 8fcfb84, amendment B1; rerun under amendment R1 440b49f: adaptive refinement): refined G vs a 40-digit reference at every N1'''c checkpoint node of
W8P8 box8, at the node's largest |Im alpha| (= s + max pole <= s_cut), on the slice/column with the largest
|G_refined - G_unrefined|. Reference: mixed-precision iterative refinement (float64 solves, mpmath residual at 40 digits,
<= 6 steps, converged if max|residual| <= 1e-25), else mpmath LU at 60 digits. Tolerance 1e-12 (column max, relative).
Consequence: fail at s~0.94 or 1.97 -> STOP; at s~2.99/3.95/5.05 -> cap W8P8 s_max at the last passing node.
Also a unit test of the double-double residual against an mpmath residual. G level only: no g, S or R. [model: Opus 5.5]"""
import json, time, numpy as np, mpmath as mp, sigma3d as S3, exp081c_numerics as C
import sys as _s; W, P, Wb = (int(v) for v in _s.argv[1:4]); Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = 4 * P
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0)
U = {p: C.ExactSlice(S.sl[p], Lx, Lt, 2 - 2 * np.cos(2 * np.pi * p / Ny), -1.0) for p in range(Ny // 2 + 1)}   # s_cut -1: no residues
smaxp = max(s for p in U for s in U[p].s if s <= 3.0); N = Lx * Lt; out = {}
def mpref(H, j):
    mp.mp.dps = 40; Hm = mp.matrix(H.tolist()); e = mp.matrix(N, 1); e[j] = 1
    x = np.linalg.solve(H, np.eye(N)[:, j].astype(complex)); xm = mp.matrix([mp.mpc(v) for v in x])
    for it in range(6):
        r = e - Hm * xm; rmax = max(abs(v) for v in r)
        if rmax <= 1e-25: return np.array([complex(v) for v in xm]), f"mixed-precision, {it} steps, residual {float(rmax):.1e}"
        xm = xm + mp.matrix([mp.mpc(v) for v in np.linalg.solve(H, np.array([complex(v) for v in r]))])
    mp.mp.dps = 60; Hm = mp.matrix(H.tolist()); e = mp.matrix(N, 1); e[j] = 1; xm = mp.lu_solve(Hm, e)
    r = e - Hm * xm; return np.array([complex(v) for v in xm]), f"mpmath LU 60 digits (refinement did not converge), residual {float(max(abs(v) for v in r)):.1e}"
# unit test of the double-double residual
sl = U[3]; a = 0.5 + 1j * 1.2; H, z = sl.H(a); G = np.linalg.inv(H); Rdd = sl.residual(G, z)
mp.mp.dps = 40; Hm = mp.matrix(H.tolist()); cols = [0, N // 2, N - 1]
Rm = [np.array([complex(v) for v in (mp.matrix(N, 1).apply(lambda q: 0) + mp.matrix([[1 if i == j else 0] for i in range(N)]) - Hm * mp.matrix([mp.mpc(v) for v in G[:, j]]))]) for j in cols]
ut = max(np.abs(Rdd[:, j] - r).max() / max(np.abs(r).max(), 1e-300) for j, r in zip(cols, Rm))
print(f"double-double residual vs mpmath residual (3 columns, slice 3, Im a = 1.2): max rel diff {ut:.1e}", flush=True); out["dd_unit"] = ut
for s in (0.937383295744266, 1.974126375751365, 2.986170475685039, 3.94825275150273, 5.05174724849727):
    t0 = time.time(); a = 0.5 + 1j * (s + smaxp); best = (-1, None, None)
    for p, sl in U.items():
        G1 = sl.G_raw(a, refine="auto"); G0 = sl.G_raw(a, refine=0); d = np.abs(G1 - G0); j = int(np.argmax(d.max(axis=0)))
        if d[:, j].max() / np.abs(G1).max() > best[0]: best = (d[:, j].max() / np.abs(G1).max(), p, j)
    _, p, j = best; sl = U[p]; H, z = sl.H(a); ref, how = mpref(H, j)
    C.ExactSlice.reset_stats(); Ga = sl.G_raw(a, "auto"); stp = dict(C.ExactSlice.STATS)
    e1 = np.abs(Ga[:, j] - ref).max() / np.abs(ref).max(); e0 = np.abs(sl.G_raw(a, 0)[:, j] - ref).max() / np.abs(ref).max()
    ok = e1 <= 1e-12 and stp["unconverged"] == 0; out[f"{s:.3f}"] = dict(steps=stp["maxsteps"], converged=stp["unconverged"] == 0, im_alpha=s + smaxp, p=p, col=j, err_refined=e1, err_unrefined=e0, ref=how, pass_=bool(ok))
    print(f"node s={s:.3f}: Im a {s + smaxp:.3f}, slice {p}, col {j}: refined (auto, {stp['maxsteps']} steps, {'converged' if stp['unconverged'] == 0 else 'NOT CONVERGED'}) {e1:.1e} | unrefined {e0:.1e} | ref: {how} -> {'PASS' if ok else 'FAIL'}  ({time.time()-t0:.0f}s)", flush=True)
json.dump(out, open(f"exp081d_results/step0_W{W}P{P}b{Wb}.json", "w"), indent=1)
