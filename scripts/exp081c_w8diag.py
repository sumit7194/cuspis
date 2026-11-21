"""EXP-081c prerequisite: which G is accurate in the W8 P8 box8 geometry (EXP-081b nuisance; Woodbury vs direct disagree
6e-8 at s~0.94, 2e-4 at s~1.97)? G-level only -- no g, S or R is computed. For the checkpoint nodes beta = 1/2 + i s
(s = 0.937, 1.974; exactly the EXP-081b checkpoint nodes), over all tail ingredients alpha = beta -+ i s_j (s_j <= 3)
and beta itself, on the unique slices p <= Ny/2:
  Gw  = production stable Woodbury;  Gdp = production _G_direct (H0 = inv(G0), double inversion);
  Gde = direct inverse of the EXACT integer H0 + twist.
For the worst (p, alpha), the column holding the max |Gw - Gde| is refined to a reference by mixed-precision iterative
refinement (float64 solves, residual e - H x in mpmath at 40 digits). [model: Opus 5.5]"""
import time, numpy as np, mpmath as mp, sigma3d as S3
P, W, Wb = 8, 8, 8; Lx, Lt = 2 * P + Wb, 2 * P; x0 = P + (Wb - W) // 2; Ny = 4 * P
S = S3.Strip3D(Lx, Lt, Ny, list(range(x0, x0 + W)), P - 1, s_cut=3.0)
idx = lambda x, t: x * Lt + t; N = Lx * Lt
def H0_exact(m2):
    H = np.zeros((N, N))
    for x in range(Lx):
        for t in range(Lt):
            i = idx(x, t); H[i, i] = 4.0 + m2
            if x + 1 < Lx: j = idx(x + 1, t); H[i, j] = H[j, i] = -1.0
            if t + 1 < Lt: j = idx(x, t + 1); H[i, j] = H[j, i] = -1.0
    return H
def Htw(sl, H0, a):
    z = np.exp(2j * np.pi * a); H = H0.astype(complex)
    for (l, u) in sl.links: H[u, l] += -(z - 1); H[l, u] += -(1 / z - 1)
    return H
nodes = {0.937383295744266: None, 1.974126375751365: None}
H0s = {p: H0_exact(2 - 2 * np.cos(2 * np.pi * p / Ny)) for p in range(Ny // 2 + 1)}
for s in nodes:
    t0 = time.time(); beta = 0.5 + 1j * s; rows = []
    alphas = [beta] + sorted({beta + sg * 1j * sj for sp in S.sl for sj in sp.s if sj <= 3.0 for sg in (-1, 1)}, key=lambda a: a.imag)
    for a in alphas:
        for p in range(Ny // 2 + 1):
            sl = S.sl[p]; Gw = sl.G(a); Gdp = S3._G_direct(sl, a); H = Htw(sl, H0s[p], a); Gde = np.linalg.inv(H)
            sc = np.abs(Gde).max(); i, j = np.unravel_index(np.argmax(np.abs(Gw - Gde)), Gw.shape)
            rows.append((np.abs(Gw - Gde).max() / sc, np.abs(Gdp - Gde).max() / sc, p, a, j))
    rows.sort(key=lambda r: -r[0])
    print(f"node s={s:.3f}: {len(alphas)} alphas x {Ny//2+1} slices ({time.time()-t0:.0f}s). worst |Gw-Gde|/max: " +
          "; ".join(f"{r[0]:.1e} (p{r[2]} Im a {r[3].imag:+.3f}; |Gdp-Gde| {r[1]:.1e})" for r in rows[:3]) +
          f" | max over all |Gdp-Gde|/max {max(r[1] for r in rows):.1e}", flush=True)
    mp.mp.dps = 40
    for e_w, e_dp, p, a, j in rows[:3]:
        sl = S.sl[p]; H = Htw(sl, H0s[p], a); Hm = mp.matrix(H.tolist()); e = np.zeros(N, complex); e[j] = 1
        x = np.linalg.solve(H, e); xm = mp.matrix([mp.mpc(v) for v in x])
        for it in range(4):
            r = mp.matrix([mp.mpc(1 if k == j else 0) for k in range(N)]) - Hm * xm
            rn = np.array([complex(v) for v in r]); xm = xm + mp.matrix([mp.mpc(v) for v in np.linalg.solve(H, rn)])
        ref = np.array([complex(v) for v in xm]); rres = float(max(abs(v) for v in (mp.matrix([mp.mpc(1 if k == j else 0) for k in range(N)]) - Hm * xm)))
        col = lambda G: np.abs(G[:, j] - ref).max() / np.abs(ref).max()
        print(f"   ref column (p{p}, Im a {a.imag:+.3f}, col {j}; final residual {rres:.1e}): Woodbury {col(sl.G(a)):.1e} | "
              f"direct-prod {col(S3._G_direct(sl, a)):.1e} | direct-exactH0 {col(np.linalg.inv(H)):.1e}", flush=True)
