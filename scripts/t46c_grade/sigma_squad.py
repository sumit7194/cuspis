"""s-quadrature control for T46c eval_K at large z: production (n_s1, n_s2) = (8, 4) vs (16, 12) vs (24, 20); plus T1+Tsad vs T2 split."""
import sys, time; sys.path.insert(0, sys.argv[1]); import numpy as np, brief_p2_t46c as T
dq = 0.25; zs = [3.0, 4.0, 5.0, 6.0, 8.0]
for Nth in (16, 24):
    op = T.ConformalEllipticModel(N_th=Nth, mu_max=4.0); eng = T.CenteredQEngine(op, dq=dq, Q_max=16.0, K_max=16)
    for n1, n2 in [(8, 4), (16, 12), (24, 20)]:
        t0 = time.time(); rows = [eng.eval_K(int(round(z/(2*dq))), s_max=3.0, n_s1=n1, n_s2=n2) for z in zs]
        T0 = np.array([r[3] for r in rows]); T2 = np.array([r[4] for r in rows]); Qp = T0 + T2; lz = np.log(zs)
        print(f"N_th={Nth} n_s=({n1},{n2}): T1+Tsad " + " ".join(f"{v:+.5f}" for v in T0) + " | T2 " + " ".join(f"{v:+.5f}" for v in T2) +
              " | slope " + " ".join(f"{v:+.4f}" for v in np.diff(Qp)/np.diff(lz)) + f" ({time.time()-t0:.0f}s)", flush=True)
