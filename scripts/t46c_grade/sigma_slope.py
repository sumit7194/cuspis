"""Sigma-side local log slopes dQ'/dln z from T46c's production eval_K, swept over Q_max (loop cutoff) and N_th.
If c_log were a converged continuum quantity, the large-z local slopes would be stable under both. [timing per row]"""
import sys, time; sys.path.insert(0, sys.argv[1]); import numpy as np, brief_p2_t46c as T
zs = [2.0, 3.0, 4.0, 5.0, 6.0, 8.0]; dq = 0.25
for Nth, Q in [(int(a), float(b)) for a, b in (x.split(':') for x in sys.argv[2:])]:
    t0 = time.time(); op = T.ConformalEllipticModel(N_th=Nth, mu_max=4.0)
    Ks = [int(round(z/(2*dq))) for z in zs]; eng = T.CenteredQEngine(op, dq=dq, Q_max=Q, K_max=max(Ks))
    Qp = np.array([eng.eval_K(K, s_max=3.0)[-1] for K in Ks]); lz = np.log(zs)
    sl = np.diff(Qp)/np.diff(lz)
    print(f"N_th={Nth} Q_max={Q:g}: Q'=" + " ".join(f"{z:g}:{v:+.5f}" for z, v in zip(zs, Qp)) +
          " | local slope " + " ".join(f"[{zs[i]:g},{zs[i+1]:g}]:{sl[i]:+.4f}" for i in range(len(sl))) + f"  ({time.time()-t0:.0f}s)", flush=True)
