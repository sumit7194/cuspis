"""(d) T0 local slopes vs box (mu_max) at N_th = 24, and N_th = 32 in a box comparable to 16/20/24 (mu_max 3.5); dq 0.5, Q 32."""
import sys, time; sys.path.insert(0, sys.argv[1]); import numpy as np, brief_p2_t46d as D
for Nth, mu in ((24, 2.5), (24, 3.5), (24, 4.5), (32, 3.5), (16, 4.5)):
    t0 = time.time(); op = D.ConformalEllipticModel(N_th=Nth, mu_max=mu); zs = [4.0, 6.0, 8.0, 10.0]
    eng = D.CenteredQEngine(op, dq=0.5, Q_max=32.0, K_max=10, act_tol=0.0); T0 = [eng.eval_K(int(z / 1.0), s_max=0.0)[3] for z in zs]
    sl = np.diff(T0) / np.diff(np.log(zs))
    print(f"  N_th={Nth} mu_max={mu} (r_max/w={op.r_max/2:.1f}, k*h at z=10: {5*op.h:.2f}): slopes [4,6] {sl[0]:+.4f} [6,8] {sl[1]:+.4f} [8,10] {sl[2]:+.4f} ({time.time()-t0:.0f}s)", flush=True)
